# 🎙️ Vaani Offline
**Private, multilingual (Hindi / English / Hinglish) AI note-taker that runs 100% on-device on the Snapdragon NPU.**
Built for the Snapdragon AI Lab – Build & Present Challenge (Qualcomm x Unstop).

> Record a lecture or meeting → get transcript, summary, action items, and a chat to ask questions about it.
> **No internet. No cloud. No subscription. Your audio never leaves your laptop.**

## Why
Cloud note-takers need connectivity, cost money, and upload private audio. Millions of students and
teachers in India learn in a Hindi-English mix, often with unreliable internet. On-device AI fixes all three.

## Features
- 🗣️ Speech-to-text: Hindi, English, Hinglish (Whisper)
- 📝 Summary, key points, action items (local LLM via Ollama)
- 💬 "Ask my lecture" – Q&A grounded only in the transcript
- ⚡ CPU vs NPU benchmark dashboard (latency, real-time factor, memory)
- ✈️ Airplane-mode ready – zero network calls at runtime

## Architecture
```
Mic/Audio ─► Whisper (ONNX Runtime + QNN ─► Hexagon NPU) ─► Transcript
                                                              │
                          Local LLM (Ollama, llama3.2:3b) ◄───┘
                                   │
                    Summary · Action items · Q&A  ─► Streamlit UI
```

## Setup (Snapdragon X laptop, Windows on ARM)
1. Install ARM64 Python 3.11+ and create a venv: `python -m venv .venv && .venv\Scripts\activate`
2. `pip install -r requirements.txt`, then install the QNN-enabled ONNX Runtime
   (`pip install onnxruntime-qnn`, or the build from the Qualcomm AI Engine Direct / AI Hub docs).
3. Install [Ollama](https://ollama.com) (ARM64) and run `ollama pull llama3.2:3b`.
4. **NPU Whisper:** export Whisper from [Qualcomm AI Hub](https://aihub.qualcomm.com) (`qai_hub_models`),
   place the encoder/decoder `.onnx` files in `models/`, and connect them in `NPUWhisper.transcribe()`
   (`engine/asr.py`). Until then the app automatically falls back to the CPU backend.
5. Run: `streamlit run app.py`
6. Benchmark: `python benchmark.py samples/lecture.wav`

## Demo script (airplane mode)
1. Turn Wi-Fi off on camera. 2. Record 30 s of Hinglish. 3. Show transcript + summary.
4. Ask a question. 5. Show CPU vs NPU panel.

## Roadmap
Live streaming captions · speaker diarisation · more Indian languages · export to PDF/Notion · exam-revision flashcards

## Author
Safiullah
