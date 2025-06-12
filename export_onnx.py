"""
export_onnx.py  ·  Generate tiny ONNX graphs for all four WFGY modules
Will auto-install `onnx` if missing (Colab-friendly).
"""

import subprocess, sys, importlib.util, os
import numpy as np

# ── ensure onnx is available ────────────────────────────────────────────
if importlib.util.find_spec("onnx") is None:
    print("🔄  Installing onnx …")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "onnx", "-q"])

import onnx
from onnx import helper, TensorProto

os.makedirs("specs/onnx", exist_ok=True)

def tiny_graph(name, dim=128):
    X = helper.make_tensor_value_info("X", TensorProto.FLOAT, [None, dim])
    Y = helper.make_tensor_value_info("Y", TensorProto.FLOAT, [None, dim])
    node = helper.make_node("Identity", ["X"], ["Y"], name=f"{name}_pass")
    graph = helper.make_graph([node], f"{name}_graph", [X], [Y])
    return helper.make_model(graph, producer_name="wfgy-dummy")

for mod in ["bbmc", "bbpf", "bbcr", "bbam"]:
    onnx.save(tiny_graph(mod.upper()), f"specs/onnx/{mod}.onnx")

print("✅ ONNX graphs saved to specs/onnx/")
