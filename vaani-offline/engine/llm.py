"""Local LLM for summaries and Q&A, served by Ollama on localhost (fully offline).

Install Ollama for Windows (ARM64 build), then:  ollama pull llama3.2:3b
If Ollama is not running, we fall back to a simple extractive summary so the
demo never crashes.
"""
import re
import requests
import config


def _chat(prompt: str, system: str) -> str:
    r = requests.post(
        f"{config.OLLAMA_URL}/api/chat",
        json={"model": config.LLM_MODEL, "stream": False,
              "messages": [{"role": "system", "content": system},
                           {"role": "user", "content": prompt}]},
        timeout=180,
    )
    r.raise_for_status()
    return r.json()["message"]["content"].strip()


def llm_available() -> bool:
    try:
        return requests.get(f"{config.OLLAMA_URL}/api/tags", timeout=2).ok
    except requests.RequestException:
        return False


def summarize(transcript: str, out_language: str = "English") -> str:
    system = ("You are a careful note-taker. The transcript may mix Hindi and English. "
              f"Reply in {out_language}. Never invent facts that are not in the transcript.")
    prompt = ("Produce:\n1) A 3-sentence summary\n2) Key points (bullets)\n"
              "3) Action items / homework (bullets, or 'None')\n\nTranscript:\n" + transcript)
    if llm_available():
        return _chat(prompt, system)
    return _extractive_fallback(transcript)


def ask(transcript: str, question: str) -> str:
    system = ("Answer ONLY from the transcript. If the answer is not in it, say so. "
              "Answer in the same language as the question.")
    prompt = f"Transcript:\n{transcript}\n\nQuestion: {question}"
    if llm_available():
        return _chat(prompt, system)
    return "Local LLM (Ollama) is not running - start it to enable Q&A."


def _extractive_fallback(text: str, n: int = 4) -> str:
    sents = [s.strip() for s in re.split(r"(?<=[.!?।])\s+", text) if len(s.split()) > 4]
    return "Summary (extractive fallback):\n- " + "\n- ".join(sents[:n]) if sents else text[:400]
