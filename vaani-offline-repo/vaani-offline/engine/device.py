"""Detect which hardware accelerators ONNX Runtime can see on this machine."""
import platform
import onnxruntime as ort


def available_providers():
    return ort.get_available_providers()


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
