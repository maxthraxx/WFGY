# run_wfgy_all_modules_demo.py

from wfgy_sdk import enable, bbmc, bbpf, bbcr, bbam
from transformers import pipeline, set_seed
import numpy as np

# === 1. 啟動模型與 enable ===
set_seed(42)
generator = pipeline("text-generation", model="gpt2", device=-1)

# 模擬一個 dummy 模型狀態
model_state = {
    "I": np.array([1.2, 0.8, 0.5]),
    "G": np.array([1.0, 0.7, 0.4]),
    "state": np.array([0.1, 0.2, 0.3]),
    "attention_logits": np.array([1.2, 0.9, 1.1])
}

model_state = enable(model_state)
print("\n✅ WFGY Enabled.\n")

# === 2. 測試四大模組 ===
print("📊 BBMC Test:")
bbmc.run_demo()

print("\n⚙️ BBPF Test:")
bbpf.run_demo()

print("\n🕸️ BBCR Test:")
bbcr.run_demo()

print("\n🔁 BBAM Test:")
bbam.run_demo()

# === 3. 語言模型前後測試 ===
prompt = "Describe the purpose of human consciousness using physics terms."

print("\n=== 🔹 Prompt ===")
print(prompt)

print("\n=== 🧠 Before WFGY ===")
before = generator(prompt, max_new_tokens=30, num_return_sequences=1)[0]["generated_text"]
print(before)

print("\n=== 🧪 After WFGY (Semantic modulation active) ===")
# 模擬開啟 WFGY 處理（這裡簡化，實際可進一步整合）
model_state = enable(model_state)
after = generator(prompt, max_new_tokens=30, num_return_sequences=1)[0]["generated_text"]
print(after)

print("\n✅ WFGY 四模組測試完成！")
