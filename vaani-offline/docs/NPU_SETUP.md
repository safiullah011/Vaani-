# Running Whisper on the Snapdragon NPU

The app works out of the box on CPU. This guide moves speech-to-text onto the Hexagon NPU.
Verify each step on your own Snapdragon X laptop; tool versions change often.

## 1. Requirements
- Snapdragon X Series laptop, Windows 11 on ARM
- ARM64 (or x64 emulated) Python 3.11
- A free [Qualcomm AI Hub](https://aihub.qualcomm.com) account

## 2. Install the QNN-enabled ONNX Runtime
```powershell
pip install onnxruntime-qnn
python -c "import onnxruntime as ort; print(ort.get_available_providers())"
```
You should see `QNNExecutionProvider` in the list. If you do, the app's header will show
**Accelerator: Snapdragon NPU ✅**.

## 3. Get Whisper models for the NPU
Whisper-Base (multilingual, includes Hindi) is listed on Qualcomm AI Hub with Snapdragon X Elite / X Plus support.
Qualcomm also publishes a **"Whisper Windows"** sample app (Python + ONNX Runtime + NPU) on AI Hub, which is
the best reference for the exact model files, feature extraction and decode loop.

Two ways to get the model files:
- Download the precompiled ONNX/QNN package from the model page (choose your Snapdragon X device and ONNX Runtime).
- Or export with `qai-hub-models` (`pip install "qai-hub-models[whisper-base]"`, then `qai-hub configure --api_token <TOKEN>`
  and run the model's `export` module with the Snapdragon X Elite target).

Place the encoder/decoder files in `models/` and set the paths in `config.py`.

## 4. Connect the decode loop
`NPUWhisper.transcribe()` in `engine/asr.py` is the integration point. The two ONNX sessions
(encoder, decoder) are already created with the QNN execution provider. Port the log-mel feature extraction
and greedy decode loop from Qualcomm's Whisper Windows sample into that method and return an `ASRResult`.
Until then the app logs a message and transparently uses the CPU backend, so nothing breaks.

## 5. Benchmark
```powershell
python benchmark.py samples\lecture.wav
streamlit run app.py    # open the "CPU vs NPU" tab
```
Put the numbers you measure into your pitch deck. Do not quote numbers you did not measure.
