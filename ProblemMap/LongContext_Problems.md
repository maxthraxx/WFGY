# 📒 Long‑Context Stress Problem Map

Mega‑prompts—>100 k tokens, entire book dumps, OCR‑noisy PDFs—overwhelm ordinary LLM pipelines.  
WFGY keeps reasoning stable with adaptive ΔS, chunk‑mapping, and sliding Tree windows.

---

## 🤔 Typical Long‑Context Crashes

| Stressor | What Standard Systems Do |
|----------|--------------------------|
| 100 k+ tokens | Memory wipe or truncated output |
| Mixed domains | Topic bleed, incoherent jumps |
| Duplicate sections | Infinite loops / “as mentioned above” spam |
| OCR noise | Hallucination or garbage sentences |

---

## 🛡️ WFGY Countermeasures

| Stressor | WFGY Module | Remedy | Status |
|----------|-------------|--------|--------|
| 100 k+ tokens | **Chunk‑Mapper** + Sliding Tree | Splits doc into ΔS‑balanced chunks, streams into window | 🛠 Beta |
| Mixed domains | Per‑domain ΔS fork | Separate Tree branch per domain; no bleed | ✅ |
| Duplicate sections | **BBMC** dedupe scan | Detects near‑identical residue, collapses | ✅ |
| PDF OCR noise | BBMC noise filter | Drops >80 % low‑entropy lines | ✅ |

---

## ✍️ Demo — 150 k‑Token PDF Dump

```txt
1️⃣  Start
> Start

2️⃣  Upload huge PDF text
> [paste or stream]

WFGY process:
• Chunk‑Mapper splits into 8 k‑token slices  
• For each slice: ΔS calc → Tree node → sliding window  
• Duplicate residue removed (413 sections merged)  
• OCR noise filtered (ΔS noise gate at 0.8)  
• Final summary or Q&A runs with stable context
````

---

## 🛠 Module Cheat‑Sheet

| Module                  | Role                               |
| ----------------------- | ---------------------------------- |
| **Chunk‑Mapper**        | Adaptive split by semantic tension |
| **Sliding Tree Window** | Keeps only relevant slices active  |
| **ΔS Metric**           | Guides chunk size & window hop     |
| **BBMC**                | Dedupe + noise filter              |
| **BBPF**                | Forks domain branches if needed    |

---

## 📊 Implementation Status

| Feature             | State                 |
| ------------------- | --------------------- |
| Chunk‑Mapper        | 🛠 Beta (public soon) |
| Sliding Tree window | ✅ Stable              |
| Cross‑domain fork   | ✅ Stable              |
| OCR noise filter    | ✅ Stable              |
| GUI chunk viewer    | 🔜 Planned            |

---

## 📝 Tips & Limits

* For >150 k tokens, set `chunk_max = 6k` for faster pass.
* Use `tree pause` to inspect each domain branch before auto‑merge.
* Share monster PDFs in **Discussions**—they stress‑test Chunk‑Mapper.

---

### 🔗 Quick‑Start Downloads (60 sec)

| Tool                       | Link                                                | 3‑Step Setup                                                                             |
| -------------------------- | --------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| **WFGY 1.0 PDF**           | [Engine Paper](https://zenodo.org/records/15630969) | 1️⃣ Download · 2️⃣ Upload to LLM · 3️⃣ Ask “Summarize using WFGY + \<doc>”               |
| **TXT OS (plain‑text OS)** | [TXTOS.txt](https://zenodo.org/records/15788557)    | 1️⃣ Download · 2️⃣ Paste into any LLM chat · 3️⃣ Type “hello world” — OS boots instantly |

---

> Survived a 100k‑token dump? ⭐ the repo so Chunk‑Mapper hits v1.0 faster.
> ↩︎ [Back to Problem Index](../README.md)

