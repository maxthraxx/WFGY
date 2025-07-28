# 📒 Problem · Long QA Chains Drift Off‑Topic

Even when each turn is “correct,” long conversations tend to slide off course—goals fade, topics morph, answers contradict earlier context. WFGY stops that drift by measuring semantic shifts and anchoring memory in a Tree.

---

## 🤔 Why Classic RAG Loses the Thread

| Weakness | Practical Effect |
|----------|------------------|
| **No Persistent Memory** | Each turn is a fresh prompt; earlier goals vanish |
| **Fragile Overlap** | Token/embedding overlap ≠ true topic continuity |
| **Zero Topic Flow Tracking** | System can’t see where or when it jumped topics |

---

## 🛡️ WFGY Three‑Step Fix

| Layer | What It Does | Trigger |
|-------|--------------|---------|
| **Semantic Tree** | Logs each major concept shift as a node | ΔS check every turn |
| **ΔS Drift Meter** | Flags semantic jump > 0.6 | Logs new branch |
| **λ_observe Vector** | Marks divergent (←) or chaotic (×) flow | Alerts or re‑anchor |

---

## ✍️ Hands‑On Demo (2 min)

```txt
1️⃣ Start TXT OS
> Start

2️⃣ Ask loosely connected questions
> "Return policy?"  
> "What if it's a gift?"  
> "How about shipping zones?"  
> "What if I'm abroad?"

3️⃣ Inspect the Tree
> view
````

You’ll see nodes with ΔS + λ flags showing each topic jump.

---

## 🔬 Sample Tree Output

```txt
• Topic: Gift Return Policy   | ΔS 0.22 | λ → | Module BBMC
• Topic: International Ship   | ΔS 0.74 | λ ← | Module BBPF, BBCR
```

WFGY detected a new conceptual frame and branched the logic instead of blending topics.

---

## 🛠 Module Cheat‑Sheet

| Module            | Role                            |
| ----------------- | ------------------------------- |
| **BBMC**          | Detects anchor shifts           |
| **BBPF**          | Maintains divergent branches    |
| **BBCR**          | Resets if drift collapses logic |
| **Semantic Tree** | Stores and replays reasoning    |

---

## 📊 Implementation Status

| Feature               | State                      |
| --------------------- | -------------------------- |
| Tree node logging     | ✅ Stable                   |
| ΔS‑based branch split | ✅ Stable                   |
| λ\_observe drift flag | ✅ Stable                   |
| Auto recall / warn    | ⚠️ Partial (manual `view`) |

---

## 📝 Tips & Limits

* Run `tree detail on` for verbose node logs.
* If you ignore the drift warnings and keep piling topics, WFGY will branch, but human review (`view`) is still best practice.
* Extreme domain shifts (> 0.9 ΔS) may prompt BBCR to ask for clarification.

---

### 🔗 Quick‑Start Downloads (60 sec)

| Tool                       | Link                                                | 3‑Step Setup                                                                             |
| -------------------------- | --------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| **WFGY 1.0 PDF**           | [Engine Paper](https://zenodo.org/records/15630969) | 1️⃣ Download · 2️⃣ Upload to LLM · 3️⃣ Ask “Answer using WFGY + \<your question>”        |
| **TXT OS (plain‑text OS)** | [TXTOS.txt](https://zenodo.org/records/15788557)    | 1️⃣ Download · 2️⃣ Paste into any LLM chat · 3️⃣ Type “hello world” — OS boots instantly |

---

> **Found this useful?** A ⭐ on GitHub keeps new fixes coming.
> ↩︎ [Back to Problem Index](./README.md)


