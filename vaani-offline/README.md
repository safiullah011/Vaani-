# 🎙️ Vaani Offline

**A private Hindi / English / Hinglish AI note-taker that runs on your Snapdragon laptop, with no cloud and no internet.**

Built for the **Snapdragon AI Lab – Build & Present Challenge** (Qualcomm x Unstop).

![python](https://img.shields.io/badge/python-3.11-blue) ![license](https://img.shields.io/badge/license-MIT-green) ![offline](https://img.shields.io/badge/runs-100%25%20offline-red)

> Record a lecture or meeting and get a transcript, summary, action items, and a chat to ask questions about it.
> Your audio never leaves your laptop.

<!-- Add your demo GIF or screenshot here: ![demo](docs/demo.gif) -->

## Why this exists
Cloud note-takers need internet, charge subscriptions, and upload private audio. Many students and teachers in India
learn in a Hindi–English mix, often with unreliable connectivity. On-device AI solves all three problems.

## Features
- 🗣️ **Speech-to-text** in Hindi, English and Hinglish (Whisper)
- 📝 **Summary, key points and action items** from a local LLM (Ollama, Llama 3.2 3B)
- 💬 **Ask my lecture:** answers grounded only in your transcript
- ⚡ **CPU vs NPU benchmark** (latency, real-time factor, memory)
- ✈️ **Airplane-mode ready:** no network calls at runtime

## Project status
| Component | Status |
|---|---|
| Streamlit UI, record/upload, transcript view | Working |
| CPU speech-to-text (faster-whisper) | Working |
| Local LLM summary and Q&A (Ollama) with offline fallback | Working |
| Benchmark script and dashboard | Working (CPU); NPU column appears once the NPU backend is connected |
| **NPU Whisper decode loop** | Integration point ready in `engine/asr.py`; see [docs/NPU_SETUP.md](docs/NPU_SETUP.md) |

## Architecture
```
Mic / audio ─► Whisper (CPU today, ONNX Runtime + QNN on the Hexagon NPU) ─► Transcript
                                                                              │
                              Local LLM (Ollama) ◄────────────────────────────┘
                                     │
                     Summary · Action items · Q&A ─► Streamlit UI
```

## Quick start
```powershell
git clone https://github.com/YOUR-GITHUB-USERNAME/vaani-offline.git
cd vaani-offline
powershell -ExecutionPolicy Bypass -File scripts\setup_windows.ps1
ollama pull llama3.2:3b
streamlit run app.py
```
Then follow [docs/NPU_SETUP.md](docs/NPU_SETUP.md) to enable the Snapdragon NPU.

## Benchmark
```powershell
python benchmark.py samples\lecture.wav
```
Results are saved to `results.json` and shown in the app's **CPU vs NPU** tab.

## Project layout
```
app.py            Streamlit UI
benchmark.py      CPU vs NPU benchmark
config.py         Model names and paths
engine/           asr.py (Whisper backends), llm.py (Ollama), device.py (NPU detection)
docs/             NPU_SETUP.md, DEMO_SCRIPT.md
tests/            pytest unit tests (run in CI)
```

## Tests
```
pip install pytest requests psutil
pytest -q
```

## Roadmap
Live streaming captions · speaker identification · more Indian languages · revision flashcards · export to PDF

## License
MIT. See [LICENSE](LICENSE).

## Author
Safiullah
