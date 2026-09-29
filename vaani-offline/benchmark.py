"""CPU vs NPU benchmark. Usage:  python benchmark.py samples/lecture.wav

Prints latency, real-time factor and peak memory for each available backend,
and writes results.json which the Streamlit dashboard displays.
"""
import json, sys, time
import psutil

from engine import asr, device


def bench(backend, path, runs=3):
    proc = psutil.Process()
    peak, times, res = 0, [], None
    for _ in range(runs):
        res = backend.transcribe(path)
        times.append(res.seconds)
        peak = max(peak, proc.memory_info().rss / 1e6)
    return {"backend": backend.name, "avg_seconds": sum(times) / len(times),
            "rtf": res.rtf, "peak_mem_mb": round(peak, 1), "audio_seconds": res.audio_seconds}


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "samples/lecture.wav"
    out = {"device": device.describe(), "results": []}
    out["results"].append(bench(asr.CPUWhisper(), path))
    if device.has_npu():
        try:
            out["results"].append(bench(asr.NPUWhisper(), path))
        except Exception as e:  # noqa: BLE001
            print("NPU benchmark skipped:", e)
    json.dump(out, open("results.json", "w"), indent=2)
    print(json.dumps(out, indent=2))
