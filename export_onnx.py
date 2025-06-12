# export_onnx.py

import os, onnx, numpy as np
from onnx import helper, TensorProto

os.makedirs("specs/onnx", exist_ok=True)

def tiny_graph(name, in_dim=128, out_dim=128):
    X = helper.make_tensor_value_info("X", TensorProto.FLOAT, [None, in_dim])
    Y = helper.make_tensor_value_info("Y", TensorProto.FLOAT, [None, out_dim])
    node = helper.make_node("Identity", ["X"], ["Y"], name=f"{name}_pass")
    graph = helper.make_graph([node], f"{name}_graph", [X], [Y])
    return helper.make_model(graph, producer_name="wfgy-dummy")

for mod in ["bbmc", "bbpf", "bbcr", "bbam"]:
    model = tiny_graph(mod.upper())
    onnx.save(model, f"specs/onnx/{mod}.onnx")
print("✅ ONNX graphs saved in specs/onnx/")
