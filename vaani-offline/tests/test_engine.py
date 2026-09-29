import engine.llm as llm
from engine import device
from engine.asr import ASRResult


def test_extractive_fallback_returns_summary(monkeypatch):
    monkeypatch.setattr(llm, "llm_available", lambda: False)
    text = ("Today we learned about photosynthesis in plants. Chlorophyll absorbs sunlight. "
            "The homework is to read chapter five. Bring your notebooks tomorrow please.")
    out = llm.summarize(text)
    assert "Summary" in out and "photosynthesis" in out


def test_ask_without_llm_is_graceful(monkeypatch):
    monkeypatch.setattr(llm, "llm_available", lambda: False)
    assert "Ollama" in llm.ask("some transcript", "what happened?")


def test_device_describe_shape():
    info = device.describe()
    assert {"machine", "os", "providers", "npu_available"} <= info.keys()
    assert isinstance(info["npu_available"], bool)


def test_rtf_calculation():
    r = ASRResult("hi", "en", seconds=5.0, audio_seconds=10.0, backend="x")
    assert r.rtf == 0.5
