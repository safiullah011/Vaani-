"""Detect which hardware accelerators ONNX Runtime can see on this machine."""
import platform

try:
    import onnxruntime as ort
except ImportError:  # keeps the UI/tests usable on machines without ORT
    ort = None


def available_providers() -> list[str]:
    return ort.get_available_providers() if ort else []


def has_npu() -> bool:
    """True when the Qualcomm QNN execution provider (Hexagon NPU) is available."""
    return "QNNExecutionProvider" in available_providers()


def describe() -> dict:
    return {
        "machine": platform.machine(),
        "processor": platform.processor(),
        "os": f"{platform.system()} {platform.release()}",
        "providers": available_providers(),
        "npu_available": has_npu(),
    }
