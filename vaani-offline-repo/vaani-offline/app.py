import json, os, tempfile
import streamlit as st

from engine import asr, device, llm

st.set_page_config(page_title="Vaani Offline", page_icon="🎙️", layout="wide")
st.title("🎙️ Vaani Offline")
st.caption("Private, multilingual AI note-taker - runs 100% on your Snapdragon laptop. No internet needed.")

info = device.describe()
c1, c2, c3 = st.columns(3)
c1.metric("Accelerator", "Snapdragon NPU ✅" if info["npu_available"] else "CPU fallback")
c2.metric("Local LLM", "Ready ✅" if llm.llm_available() else "Start Ollama")
c3.metric("Cloud calls", "0")

@st.cache_resource
def get_asr():
    return asr.load_best()

tab_notes, tab_bench = st.tabs(["📝 Notes", "⚡ CPU vs NPU"])

with tab_notes:
    left, right = st.columns([1, 1])
    with left:
        audio = st.audio_input("Record a lecture / meeting") or st.file_uploader(
            "...or upload audio", type=["wav", "mp3", "m4a"])
        lang = st.selectbox("Spoken language", ["Auto-detect", "Hindi", "English"])
        out_lang = st.selectbox("Summary language", ["English", "Hindi"])
        if audio and st.button("Transcribe & summarise", type="primary"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
                f.write(audio.getvalue()); path = f.name
            code = {"Auto-detect": None, "Hindi": "hi", "English": "en"}[lang]
            with st.spinner("Transcribing on-device..."):
                res = get_asr().transcribe(path, code)
            st.session_state.update(res=res, transcript=res.text)
            with st.spinner("Summarising with local LLM..."):
                st.session_state["summary"] = llm.summarize(res.text, out_lang)
            os.unlink(path)
    with right:
        if "res" in st.session_state:
            r = st.session_state["res"]
            st.success(f"{r.backend} | {r.seconds:.1f}s for {r.audio_seconds:.0f}s audio "
                       f"(RTF {r.rtf:.2f}) | detected: {r.language}")
            st.subheader("Transcript"); st.write(st.session_state["transcript"])
            st.subheader("Summary"); st.write(st.session_state["summary"])
    if "transcript" in st.session_state:
        st.divider(); st.subheader("Ask my lecture")
        q = st.text_input("Ask anything about what was said (Hindi or English)")
        if q:
            st.write(llm.ask(st.session_state["transcript"], q))

with tab_bench:
    st.write("Run `python benchmark.py samples/lecture.wav`, then reload this tab.")
    if os.path.exists("results.json"):
        data = json.load(open("results.json"))
        st.json(data["device"])
        st.dataframe(data["results"], use_container_width=True)
        st.bar_chart({r["backend"]: r["avg_seconds"] for r in data["results"]})
