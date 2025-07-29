# 🆕 Beginner Guide — How to Identify & Fix Your AI Failure  
*A zero‑to‑hero crash‑course for anyone new to WFGY, RAG pipelines, or “why is my model hallucinating?”*

---

## 0. 🎯 Why This Guide Exists

If you landed on the **Problem Map** and felt overwhelmed by 16 exotic failure modes (ΔS? BBCR? bootstrap race?!), start here.

1. **Rapid Symptom Check** → pinpoint which problem table row matches your bug.  
2. **Concept Primer** → learn the minimum theory (RAG, embeddings, reasoning chains).  
3. **Tool Setup** → grab the open‑source files (all MIT‑licensed) and reproduce the fix.  

Total reading time: **≈ 10 min**. After that, jump back to the [Problem Map](./README.md) and dive deep.

---

## 1. 🔍 “Which Symptom Matches My Bug?”

Below is a *mini* decision tree. Start at the top, follow the **first “Yes”** branch you hit, then look up the **Problem ID** in the main table.

| Question | Yes → Go To | No → Next Check |
|----------|-------------|-----------------|
| Are you **retrieving** chunks that look correct **but answer is wrong**? | #1 Hallucination & Chunk Drift | ↓ |
| Does the model reach the chunk **but fails logically** (e.g. wrong reasoning)? | #2 Interpretation Collapse | ↓ |
| Do multi‑step tasks **derail after a few hops**? | #3 Long Reasoning Chains | ↓ |
| Does the model **invent confident nonsense**? | #4 Bluffing / Overconfidence | ↓ |
| High cosine similarity **yet semantic meaning off**? | #5 Semantic ≠ Embedding | ↓ |
| Pipeline **dead‑ends / loops** logic? | #6 Logic Collapse & Recovery | ↓ |
| Long chat (> 50 turns) **forgets context**? | #7 Memory Breaks Across Sessions | ↓ |
| Failure path **invisible / no logs**? | #8 Debugging is a Black Box | ↓ |
| Output suddenly **incoherent / repetitive**? | #9 Entropy Collapse | ↓ |
| Replies **flat & literal**, creativity gone? | #10 Creative Freeze | ↓ |
| Formal math / symbolic prompts **crash**? | #11 Symbolic Collapse | ↓ |
| Self‑reference / paradox **freezes** model? | #12 Philosophical Recursion | ↓ |
| Multiple agents **overwrite** each other? | #13 Multi‑Agent Chaos | ↓ |
| Deployment starts **before index ready**? | #14 Bootstrap Ordering | ↓ |
| Services **wait on each other forever**? | #15 Deployment Deadlock | ↓ |
| First LLM call **crashes after deploy**? | #16 Pre‑Deploy Collapse | File an Issue → unknown |

> **Tip:** Not sure? Capture a failing trace (input → retrieval → output) and open a GitHub Discussion — we’ll help classify it.

---

## 2. 🧠 Core Concepts in < 5 Minutes

### 2.1 What Is RAG?  
**Retrieval‑Augmented Generation** feeds external knowledge (your PDFs, DB, wiki) into a language model *during* inference.

```

User ➜  Query           ─┐
├─> \[ Retriever ] —> top‑k chunks ➜  prompt ➜  \[ LLM ] ➜  answer
Vector DB / Search  ────┘

```

Why it breaks:
* Wrong chunk (vector drift) → hallucination.  
* Correct chunk + broken prompt → interpretation collapse.  
* Long chain of tools → hidden state loss.

### 2.2 Embeddings vs Semantics  
Cosine similarity (dense vectors) ≠ human meaning. WFGY’s ΔS metric spots gaps in *semantic* resonance, not just distance.

### 2.3 Reasoning Chains  
LLM ≠ database. Complex tasks span multiple calls: *parse → retrieve → reason → act*. Losing state mid‑chain is #3.

### 2.4 WFGY Modules (30‑sec cheat‑sheet)

| Module | Purpose |
|--------|---------|
| **BBMC** | Boundary‑Bounded Memory Chunks — safe semantic units |
| **BBPF** | Branch‑Bounded Prompt Frames — stable context windows |
| **BBCR** | Break‑Before Crash Reset — aborts / resets logic loops |
| **ΔS Metric** | Measures semantic tension (unknown topic, drift) |

You don’t need to rebuild them — TXT OS hands you ready‑to‑paste text files.

---

## 3. 🛠️ Quick Tool Setup

| Step | What to Do | Time |
|------|------------|------|
| 1️⃣  | Download **WFGY 1.0 PDF** and **TXT OS** (links below) | 30 s |
| 2️⃣  | Paste TXT OS into any LLM chat (Claude, GPT‑4, local llama‑cpp) | 15 s |
| 3️⃣  | Ask: `“Diagnose my RAG: {describe bug}”` | Go |

*The OS auto‑loads Problem Map indexes; you can also open Markdown files locally.*

### Download Links

| Asset | Link |
|-------|------|
| **WFGY 1.0 PDF** | https://zenodo.org/records/15630969 |
| **TXT OS** | https://zenodo.org/records/15788557 |

> **Everything is MIT‑licensed** — free for commercial & research use.

---

## 4. 🗂️ Problem Categories (cheat‑label)

| Category | IDs | Typical Stage |
|----------|-----|---------------|
| **Prompting** | #4 | Prompt crafting / safety |
| **Retrieval** | #1 #5 #8 | Vector DB, search, RAG |
| **Reasoning** | #2 #6 #11 | Mid‑chain logic |
| **Infra / Deploy** | #14 #15 #16 | DevOps, orchestration |

*(The table also appears under the main Problem Map for quick visual filter.)*

---

## 5. 🏃 Next Steps

1. **Identify** your bug via the quick decision tree above.  
2. **Open** the corresponding `.md` file in the Problem Map.  
3. **Apply** the patch (many include code snippets, BBPF prompt frames, or Docker diff).  
4. **Share** results! Open a PR if you found a variant or edge‑case — the map keeps growing.

---

## 6. 🙋 FAQ (Super Short)

| Question | Answer |
|----------|--------|
| *Do I need all modules?* | No. Start with the module named in the problem page. |
| *Does WFGY replace LangChain / LlamaIndex?* | It layers **above** them (reasoning firewall). |
| *Will it work on GPT‑3.5?* | Yes, but complex fixes (#11, #12) need ≥ GPT‑4 or good local models. |

---

### ⭐ Help Us Expand the Map

- 🐛 Got a new failure trace? [Open an Issue](https://github.com/onestardao/WFGY/issues).  
- 🧩 Have a fix? PRs welcome — credit in the Hall of Fame.  
- 🚀 Star the repo to unlock Engine 2.0 once we hit **10 k** stars.

---

> **Citation:** If you use WFGY in research or production, cite the Zenodo DOI in the PDF.

<br>


↩︎ [Back to Problem Index](./README.md)

<br>

> <img src="https://img.shields.io/github/stars/onestardao/WFGY?style=social" alt="GitHub stars"> ⭐ Help reach 10,000 stars by 2025-09-01 to unlock Engine 2.0 for everyone  ⭐ <strong><a href="https://github.com/onestardao/WFGY">Star WFGY on GitHub</a></strong>

> 👑 **Early Stargazers: [See the Hall of Fame](https://github.com/onestardao/WFGY/tree/main/stargazers)** —  
> Engineers, hackers, and open source builders who supported WFGY from day one.


