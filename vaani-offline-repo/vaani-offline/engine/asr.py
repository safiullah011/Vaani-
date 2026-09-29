"""Speech-to-text (Hindi / English / Hinglish).

Two interchangeable backends behind one interface:
  * CPUWhisper - faster-whisper, runs anywhere (baseline + fallback)
  * NPUWhisper - Whisper encoder/decoder exported through Qualcomm AI Hub and
                 executed with ONNX Runtime's QNN execution provider (Hexagon NPU)

Set NPU model paths in config.py once you have exported them from AI Hub.
"""
import time
from dataclasses import dataclass

import config
from engine import device


@dataclass
class ASRResult:
    text: str
    language: str
    seconds: float          # wall-clock time spent transcribing
    audio_seconds: float
    backend: str

    @property
    def rtf(self) -> float:
        """Real-time factor: <1 means faster than real time."""
        return self.seconds / max(self.audio_seconds, 1e-6)


class CPUWhisper:
    name = "CPU (faster-whisper)"

    def __init__(self, model_size: str = config.WHISPER_MODEL):
        from faster_whisper import WhisperModel
        self.model = WhisperModel(model_size, device="cpu", compute_type="int8")

    def transcribe(self, audio_path: str, language: str | None = None) -> ASRResult:
        t0 = time.perf_counter()
        segments, info = self.model.transcribe(audio_path, language=language, vad_filter=True)
        text = " ".join(s.text.strip() for s in segments)
        return ASRResult(text, info.language, time.perf_counter() - t0, info.duration, self.name)


class NPUWhisper:
    """Runs the AI Hub-exported Whisper on the Snapdragon NPU via QNN EP.

    Implementation note: AI Hub ships Whisper as separate encoder/decoder ONNX
    graphs. `qai_hub_models.models.whisper_base` provides the pre/post-processing
    (log-mel features, tokenizer, decode loop) - we only swap the session
    providers so the graphs execute on the NPU.
    """
    name = "NPU (Snapdragon / QNN)"

    def __init__(self):
        if not device.has_npu():
            raise RuntimeError("QNNExecutionProvider not available on this machine")
        import onnxruntime as ort
        opts = ort.SessionOptions()
        providers = [("QNNExecutionProvider", {"backend_path": "QnnHtp.dll"}),
                     "CPUExecutionProvider"]
        self.encoder = ort.InferenceSession(config.NPU_ENCODER_PATH, opts, providers=providers)
        self.decoder = ort.InferenceSession(config.NPU_DECODER_PATH, opts, providers=providers)

    def transcribe(self, audio_path: str, language: str | None = None) -> ASRResult:
        # Wire this to qai_hub_models' WhisperApp (see README, step 4).
        raise NotImplementedError("Hook up the AI Hub Whisper app here (README step 4)")


def load_best():
    """Prefer the NPU; fall back to CPU so the app always works."""
    if device.has_npu():
        try:
            return NPUWhisper()
        except Exception as e:  # noqa: BLE001
            print(f"[asr] NPU backend unavailable ({e}); using CPU")
    return CPUWhisper()
