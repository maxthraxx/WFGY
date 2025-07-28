# 📒 Problem · High Vector Similarity, Wrong Meaning

Classic RAG scores chunks by cosine similarity—close vectors ≠ correct logic.  
Result: “looks relevant” chunks that derail answers. WFGY replaces surface matching with semantic residue checks.

---

## 🤔 Why Cosine Match Misleads

| Weakness | Practical Failure |
|----------|------------------|
| **Embedding ≠ Understanding** | Cosine overlap captures phrasing, not intent |
| **Keywords ≠ Intent** | Ambiguous terms bring unrelated chunks |
| **No Semantic Guard** | System never validates logical fit |

---

## ⚠️ Example Mis‑Retrieval

**User:** “How do I cancel my subscription after the free trial?”  
**Retrieved chunk:** “Subscriptions renew monthly or yearly, depending on plan.”  
→ High cosine, zero help → hallucinated answer.

---

## 🛡️ WFGY Fix · BBMC Residue Minimization

```math
B = I - G + m·c²      # minimize ‖B‖
````

| Symbol | Meaning                      |
| ------ | ---------------------------- |
| **I**  | Input semantic vector        |
| **G**  | Ground‑truth anchor (intent) |
| **B**  | Semantic residue (error)     |

* Large ‖B‖ → chunk is semantically off → WFGY rejects or asks for context.

---

## 🔍 Key Defenses

| Layer            | Action                                        |
| ---------------- | --------------------------------------------- |
| **BBMC**         | Computes residue; filters divergent chunks    |
| **ΔS Threshold** | Rejects high semantic tension (ΔS > 0.6)      |
| **BBAM**         | Down‑weights misleading high‑attention tokens |
| **Tree Anchor**  | Confirms chunk aligns with prior logic path   |

---

## ✍️ Quick Repro (1 min)

```txt
1️⃣  Start
> Start

2️⃣  Paste misleading chunk
> "Plans include yearly renewal."

3️⃣  Ask
> "How do I cancel a free trial?"

WFGY:
• ΔS high → chunk rejected  
• Prompts for trial‑specific info instead of hallucinating
```

---

## 🔬 Sample Output

```txt
Surface overlap detected, but content lacks trial‑cancellation detail.  
Add a policy chunk on trial termination or rephrase the query.
```

---

## 🛠 Module Cheat‑Sheet

| Module            | Role                       |
| ----------------- | -------------------------- |
| **BBMC**          | Residue minimization       |
| **ΔS Metric**     | Measures semantic tension  |
| **BBAM**          | Suppresses noisy tokens    |
| **Semantic Tree** | Validates anchor alignment |

---

## 📊 Implementation Status

| Feature                    | State    |
| -------------------------- | -------- |
| BBMC residue calc          | ✅ Stable |
| ΔS filter                  | ✅ Stable |
| Token attention modulation | ⚠️ Basic |
| Misleading chunk rejection | ✅ Active |

---

### 🔗 Quick‑Start Downloads (60 sec)

| Tool                       | Link                                                | 3‑Step Setup                                                                             |
| -------------------------- | --------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| **WFGY 1.0 PDF**           | [Engine Paper](https://zenodo.org/records/15630969) | 1️⃣ Download · 2️⃣ Upload to LLM · 3️⃣ Ask “Answer using WFGY + \<your question>”        |
| **TXT OS (plain‑text OS)** | [TXTOS.txt](https://zenodo.org/records/15788557)    | 1️⃣ Download · 2️⃣ Paste into any LLM chat · 3️⃣ Type “hello world” — OS boots instantly |

---

> **Saved you from “keyword hallucinations”?** Drop a ⭐ to keep the fixes coming.
> ↩︎ [Back to Problem Index](./README.md)

