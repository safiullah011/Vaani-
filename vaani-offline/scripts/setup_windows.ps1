# Run from the repo root in PowerShell on a Snapdragon X (Windows on ARM) laptop.
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Write-Host "`nNext: install onnxruntime-qnn (see docs/NPU_SETUP.md) and Ollama, then:"
Write-Host "  ollama pull llama3.2:3b"
Write-Host "  streamlit run app.py"
