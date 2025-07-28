# 📒 Problem · Hallucination from Irrelevant Chunks

Even with pricey embeddings and top‑k retrieval, RAG systems still hallucinate—**LLMs answer confidently with facts nowhere in the source.**  
This page shows why that happens and how WFGY’s semantic firewall stops it.

---

## 🤔 Why Do Classic RAG Pipelines Hallucinate?

| Failure Mode | What Really Happens |
|--------------|---------------------|
| **Vector ≠ Meaning** | Cosine similarity says “close” but the chunk adds no logical value |
| **No Tension Check** | Model never measures how far it drifts from the user question |
| **Zero Fallback** | When the answer is unstable, the system keeps talking instead of pausing |

---

## 🛡️ WFGY Three‑Layer Fix

| Layer | What It Does | Trigger |
|-------|--------------|---------|
| **ΔS Measure** | Quantifies semantic jump between question & chunk | `ΔS > 0.6` |
| **λ_observe** | Flags divergent or chaotic logic flow | Divergent + high ΔS |
| **BBCR Reset** | Re‑anchor, request clarity, or halt output | Instability detected |

---

## ✍️ Hands‑On: Reproduce in 60 sec

```txt
Start  ▸  Paste chunk  ▸  Ask question

Step 1  Start TXT OS
> Start

Step 2  Paste a misleading chunk
> "Company handbook covers refunds through retail partners…"

Step 3  Ask unrelated question
> "What is the international warranty for direct purchases?"

WFGY:
• Calculates ΔS → high  
• Flags λ_observe → divergent  
• Replies with a clarification request instead of guessing
````

---

## 🔬 Before vs. After

> **Typical RAG:**
> “Yes, we offer a 5‑year international warranty on all items.”

> **WFGY Response:**
> “The provided content doesn’t mention international warranty.
> Would you like to add a direct‑purchase policy chunk or clarify?”

Semantic integrity, not polite hallucination.

---

## 🛠 Module Quick Chart

| Module            | Role                           |
| ----------------- | ------------------------------ |
| **BBMC**          | Minimizes semantic residue     |
| **BBCR**          | Collapse–Rebirth logic reset   |
| **λ\_observe**    | Monitors logic direction       |
| **ΔS Metric**     | Measures semantic jump         |
| **Semantic Tree** | Records & backtracks reasoning |

---

## 📊 Implementation Status

| Item                  | State      |
| --------------------- | ---------- |
| ΔS detection          | ✅ Stable   |
| λ\_observe            | ✅ Stable   |
| BBCR reset            | ✅ Stable   |
| Auto fallback prompt  | ✅ Basic    |
| Retriever auto‑filter | 🛠 Planned |

---

## 📝 Tips & Limits

* Works even with manual paste—no retriever required.
* If your retriever feeds garbage, WFGY blocks hallucination but **can’t auto‑retokenize**—that’s coming with the Chunk‑Mapper firewall release.
* Share tricky traces in **Discussions**; we add real cases to the map.

---

## 🚀 Quick‑Start Downloads

| Tool                       | Link                                                | 3‑Step Setup                                                                             |
| -------------------------- | --------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| **WFGY 1.0 PDF**           | [Engine Paper](https://zenodo.org/records/15630969) | 1️⃣ Download · 2️⃣ Upload to LLM · 3️⃣ Ask “Answer using WFGY + \<your question>”        |
| **TXT OS (plain‑text OS)** | [TXTOS.txt](https://zenodo.org/records/15788557)    | 1️⃣ Download · 2️⃣ Paste into any LLM chat · 3️⃣ Type “hello world” — OS boots instantly |

---

> **Help the project grow:** if this solved your hallucination headache, please drop a ⭐
> 📚 [Back to Problem Index](./README.md)


