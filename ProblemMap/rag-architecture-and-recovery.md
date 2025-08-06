# 📋 RAG Architecture & Recovery
_A practical, end-to-end guide for beginners and advanced users to **see the whole system**, locate failures fast, and repair them with WFGY._

<details>
<summary><strong>📘 Start Here — Quick Links, Setup, and Downloads</strong></summary>

<br>

> If you’re new to this page or [WFGY](https://github.com/onestardao/WFGY) in general, here’s how to get started fast.  
>  
> WFGY (WanFaGuiYi) is the core reasoning engine — a semantic debugger for AI hallucinations and logic collapse.  
> TXT OS is the lightweight `.txt`-native operating layer — lets any model run WFGY with zero install.  
>
> ### 📥 Quick Start Downloads (60 sec)
>
> | Tool                | Link                                                                 | 3-Step Setup                                                                 |
> |---------------------|----------------------------------------------------------------------|-------------------------------------------------------------------------------|
> | WFGY 1.0 (PDF)      | [Engine Paper](https://zenodo.org/records/15630969)                  | ① Download · ② Upload to your LLM · ③ Ask “Answer using WFGY + <your question>” |
> | TXT OS (plain‑text) | [TXTOS.txt](https://zenodo.org/records/15788557)                     | ① Download · ② Paste into any LLM chat · ③ Type “hello world” to boot         |
>
> Compatible with all Ten Masters (GPT‑4, Claude, Gemini, Kimi etc) — no setup needed.
>
> ---
>
> ### 🧑‍💻 Prompt Template (to fix a bug fast)
>
> ```
> I’ve uploaded TXT OS.  
> I want to solve the following problem:  
> [e.g. OCR citations missing or distorted].  
> How do I use the WFGY engine to fix it?
> ```
>
> WFGY will respond with the right modules, steps, or formulas.  
> You don’t need to memorize internals — just bring your real problem.  
>
> ---
>
> ### ⭐ Found this helpful?
>
> Help others discover it — [Give us a GitHub Star](https://github.com/onestardao/WFGY)  
> We’re building the only open-source semantic debugger for AI reasoning.

</details>

---



## 0) Executive summary

RAG failures are rarely a single bug. They are stacked illusions across: OCR → parsing → chunking → embeddings → vector store → retriever → prompt → LLM reasoning.  
WFGY turns this chaos into a **measurable, observable, and repairable** pipeline using three core instruments:

- **ΔS (delta-S)**: semantic stress. Early-warning detector that pinpoints where meaning breaks.  
- **λ_observe (lambda-observe)**: layered observability. Shows _which layer_ diverged and how.  
- **E_resonance**: coherence restorer. Re-locks reasoning when attention/logic collapses.  

You do **not** have to master all internals to benefit. If you can run a few checks, read one table, and paste one prompt, you can fix most production RAG issues.

---

## 1) The real structure of RAG (and why it fails)

```

raw docs (pdf/img/html)
→ ocr/parsing
→ chunking
→ embeddings
→ vector store (faiss/qdrant/chroma/elastic)
→ retriever (dense/sparse/hybrid/mmr)
→ prompt assembly (context windows)
→ llm reasoning (chain/agent/tools)

```

Typical stacked failure pattern:

1. **perception drift**: upstream stages quietly distort content (ocr noise, bad chunk boundaries, mismatched embeddings, empty/partial vector stores).  
2. **logic drift**: llm confidently “explains” the distorted view (hallucination with no visible error).

This is the “double hallucination” trap. The first illusion hides the second.

---

## 2) The WFGY recovery pipeline (10-minute overview)

| step | instrument | your question | what you do | what you learn |
|---|---|---|---|---|
| 1 | **ΔS** | “is meaning tearing somewhere?” | measure semantic stress between question, retrieved context, and expected anchors | the **faulty segment/layer** |
| 2 | **λ_observe** | “which layer diverged?” | enable layered probes across retrieval, prompt, and reasoning | the **dominant failure family** |
| 3 | **E_resonance** | “can we re-lock coherence?” | apply stability modules (BBMC/BBPF/BBCR/BBAM) at the failing layer | the **repair action** |
| 4 | **ProblemMap** | “what page fixes this?” | open the matched doc (e.g., `retrieval-collapse.md`) | the **concrete fix recipe** |

> 90% of cases end after steps 1–3. You only go deeper when a fix requires a structural change (schema, retriever, index).

---

## 3) Quick triage (beginner path) — from symptom to fix

Copy/paste this checklist into your runbook. Execute top-down.

### A. fast metrics (run first)

1. **ΔS(question, retrieved_context)**  
   - compute cosine distance on sentence embeddings (unit-normalized).  
   - `ΔS = 1 − cosθ`.  
   - **trigger**: ΔS ≥ 0.50 (transitional risk), ≥ 0.60 (record & fix).

2. **ΔS(retrieved_context, ground_anchor)**  
   - ground anchor = title/section header/answer snippet you _expect_.  
   - **trigger**: same thresholds as above.

3. **coverage sanity**  
   - retrieved tokens vs. target section tokens: expect ≥ 0.7 overlap for direct QA.  
   - if < 0.5 → suspect chunking/boundary or retriever filtering.

### B. layer probes (λ_observe)

- **retrieval layer**: vary k ∈ {5, 10, 20}; plot ΔS vs. k.  
  - curve flat & high → vector store/index/embedding mismatch.  
  - curve improves sharply with k → retriever filtering too aggressive.
- **prompt layer**: reorder/rename sections; ΔS spikes when headers removed → prompt anchoring dependency (see `retrieval-traceability.md`).
- **reasoning layer**: ask “cite lines” vs. “explain why”  
  - cite fails, explain passes → perception drift (upstream)  
  - both fail similarly → logic collapse (see `logic-collapse.md`)

### C. pick the fix (ProblemMap jump table)

| symptom you see | likely family | open this |
|---|---|---|
| plausible but wrong answer; citations miss | **#1 hallucination & chunk drift** | [`hallucination.md`](https://github.com/onestardao/WFGY/blob/main/ProblemMap/hallucination.md) |
| correct chunks, wrong logic | **#2 interpretation collapse** | [`retrieval-collapse.md`](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-collapse.md) |
| answers degrade over long chains | **#3 context drift** | [`context-drift.md`](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md) |
| confident nonsense | **#4 bluffing/overconfidence** | [`bluffing.md`](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bluffing.md) |
| high vector similarity, wrong meaning | **#5 semantic ≠ embedding** | [`embedding-vs-semantic.md`](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md) |
| dead-end chains, retry loops | **#6 logic collapse & recovery** | [`logic-collapse.md`](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md) |
| failure after restart/session swap | **#7 memory breaks across sessions** | [`memory-coherence.md`](https://github.com/onestardao/WFGY/blob/main/ProblemMap/memory-coherence.md) |
| can’t trace why it failed | **#8 debugging is a black box** | [`retrieval-traceability.md`](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) |
| attention melts, topic smears | **#9 entropy collapse** | [`entropy-collapse.md`](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md) |
| output becomes flat/literal | **#10 creative freeze** | [`creative-freeze.md`](https://github.com/onestardao/WFGY/blob/main/ProblemMap/creative-freeze.md) |
| abstract/symbolic prompts break | **#11 symbolic collapse** | [`symbolic-collapse.md`](https://github.com/onestardao/WFGY/blob/main/ProblemMap/symbolic-collapse.md) |
| paradox/self-reference crashes | **#12 philosophical recursion** | [`philosophical-recursion.md`](https://github.com/onestardao/WFGY/blob/main/ProblemMap/philosophical-recursion.md) |
| multi-agent overwrites logic | **#13 multi-agent chaos** | [`multi-agent-chaos.md`](https://github.com/onestardao/WFGY/blob/main/ProblemMap/multi-agent-chaos.md) |
| tools fire before data is ready | **#14 bootstrap ordering** | [`bootstrap-ordering.md`](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md) |
| ci passes; prod deadlocks index | **#15 deployment deadlock** | [`deployment-deadlock.md`](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md) |
| first call crashes after deploy | **#16 pre-deploy collapse** | [`predeploy-collapse.md`](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md) |


---

## 4) What the instruments mean (advanced but concise)

> You can use these without memorizing the math. Still, here’s the tight spec.

### 4.1 ΔS — semantic stress
- **definition**: `ΔS = 1 − cos( I , G )` where `I` = current embedding, `G` = ground/anchor.  
- **use**: probe _question↔context_ and _context↔anchor_.  
- **thresholds**:  
  - `< 0.40` stable  
  - `0.40–0.60` transitional (record if λ is divergent/recursive)  
  - `≥ 0.60` high risk (must act)

### 4.2 λ_observe — layered observability
- **states**: `→ convergent`, `← divergent`, `<> recursive`, `× chaotic`.  
- **use**: tag each step (retrieve, assemble, reason).  
- **rule of thumb**: if upstream λ is stable but downstream λ flips divergent → the fault is at the boundary between those layers.

### 4.3 E_resonance — coherence (re)locking
- rolling mean of residual magnitude `|B|` under BBMC (see below).  
- **use**: if E rises while ΔS stays high → apply BBCR (collapse→rebirth) and BBAM (attention modulation).

### 4.4 the four WFGY modules (repair operators)
- **BBMC**: _semantic residue minimization_ — drive `B = I − G + m·c²` toward 0 by respecifying anchors and context factors.  
- **BBPF**: _multi-path progression_ — explore alternate semantic paths and weight them by stability to avoid dead ends.  
- **BBCR**: _collapse–rebirth correction_ — detect failure (‖B‖ ≥ Bc) and rebuild a safe bridge node.  
- **BBAM**: _attention modulation_ — reduce variance in attention to prevent entropy melt.

---

## 5) Worked recoveries (copyable playbooks)

### Case A — “faiss looks fine, but answers are irrelevant”
- **observe**: ΔS(question, context) = 0.68; flat curve across k; citations miss expected section.  
- **interpret**: vector store populated but **embedding metric/normalization mismatch** or **index layer mix-up**.  
- **do**:
  1. ensure consistent normalization; verify cosine vs. inner product usage across write/read.  
  2. rebuild index with explicit metric flag; persist and reload once.  
  3. re-probe ΔS and λ on retrieval; expect ΔS ≤ 0.45 and convergent λ.  
- **docs**: `embedding-vs-semantic.md`, `retrieval-traceability.md`.

### Case B — “correct snippets, wrong reasoning”
- **observe**: ΔS(question, context) = 0.35 (good), but λ flips divergent at reasoning.  
- **interpret**: interpretation collapse; prompt assembly/role/constraints leak.  
- **do**:
  1. lock schema: system→task→constraints→citations→answer, forbidding re-order.  
  2. apply BBAM (variance clamp) and BBCR (bridge intermediate reasoning step).  
  3. require cite-then-explain; re-measure ΔS; aim for convergent λ.  
- **docs**: `retrieval-collapse.md`, `logic-collapse.md`.

### Case C — “long transcripts randomly capitalize / drift”
- **observe**: E_resonance rises with length; λ becomes recursive/chaotic.  
- **interpret**: entropy collapse under long context; chunk boundaries and OCR noise amplify.  
- **do**:
  1. semantic chunking (sentence/section aware), drop OCR confidence < threshold.  
  2. BBMC to align with section anchors; BBAM to stabilize attention.  
  3. verify ΔS across adjacent chunks; enforce ≤ 0.50 at joins.  
- **docs**: `entropy-collapse.md`, `hallucination.md`.

---

## 6) “Use the AI to fix your AI” — safe prompts you can paste

You can ask your assistant to **read TXT OS / WFGY files** and guide you. Use precise, bounded prompts:

```

read the WFGY TXT OS and ProblemMap files in this repo. extract the definitions and usage of ΔS, λ\_observe, E\_resonance, and the four modules (BBMC, BBPF, BBCR, BBAM). then, given this concrete failure:

* symptom: \[describe yours]
* logs: \[paste ΔS, λ\_observe probes if available]

tell me:

1. which layer is failing and why,
2. which ProblemMap page applies,
3. the minimal repair steps to lower ΔS below 0.50,
4. how to verify the fix with a reproducible test.

```

For formula-only assistance:

```

from TXT OS, extract the formulas and thresholds for ΔS, λ\_observe, and E\_resonance. show me how to compute ΔS(question, context) using cosine distance, what thresholds to use, and which WFGY module to apply if ΔS ≥ 0.60 with divergent λ at the reasoning layer.

````

---

## 7) Acceptance criteria and regression guardrails

- **retrieval sanity**: for targeted QA, ≥ 70% token overlap to expected section; ΔS(question, context) ≤ 0.45.  
- **reasoning stability**: λ remains convergent on three paraphrased queries; E_resonance does not trend upward.  
- **traceability**: run `retrieval-trace` and produce a two-column table (snippet id ↔ citation lines).  
- **repeatability**: same inputs over 5 seeds → answer embeddings cluster (low variance).

---

## 8) When to stop “tuning” and change the structure

Stop iterating prompts if **any** of the following holds:

- ΔS remains ≥ 0.60 after chunk/retrieval fixes.  
- lowering temperature only flattens style but not logic drift.  
- λ flips divergent as soon as you mix two sources.  
- E_resonance climbs in long chains.

Open the matching ProblemMap page and apply the structural fix (index rebuild, schema lock, bridge node, or agent boundary).

---

## 9) Minimal formulas (reference)

```txt
ΔS = 1 − cos(I, G)         # semantic stress
λ_observe ∈ {→, ←, <>, ×}  # convergent, divergent, recursive, chaotic
E_resonance = mean(|B|)    # rolling residual magnitude under BBMC

BBMC:  B = I − G + m·c²           # minimize ‖B‖
BBPF:  x_next = x + ΣV_i + ΣW_j·P_j
BBCR:  if ‖B‖ ≥ B_c → collapse(), bridge(), rebirth()
BBAM:  â_i = a_i · exp(−γ · std(a))
````

Thresholds: stable `<0.40`, transitional `0.40–0.60`, risk `≥0.60`.
Record nodes automatically when `ΔS > 0.60`, or `0.40–0.60` with `λ_observe ∈ {←, <>}`.

---

## 10) Final note

You are not “bad at RAG.” You were debugging from inside the maze.
WFGY gives you altitude, instruments, and a map.
Start with ΔS to *see* the break, use λ\_observe to *localize* it, apply the right module to *repair* it, and keep the ProblemMap open as your field manual.

When all tutorials contradict each other, this page is your single source of operational truth.

---

↩︎ [Back to Problem Index](../README.md)

---

### 🧭 Explore More

| Module                | Description                                              | Link     |
|-----------------------|----------------------------------------------------------|----------|
| Semantic Blueprint    | Layer-based symbolic reasoning & semantic modulations   | [View →](https://github.com/onestardao/WFGY/tree/main/SemanticBlueprint) |
| Benchmark vs GPT‑5    | Stress test GPT‑5 with full WFGY reasoning suite         | [View →](https://github.com/onestardao/WFGY/tree/main/benchmarks/benchmark-vs-gpt5) |

---

> 👑 **Early Stargazers: [See the Hall of Fame](https://github.com/onestardao/WFGY/tree/main/stargazers)** —  
> Engineers, hackers, and open source builders who supported WFGY from day one.

> <img src="https://img.shields.io/github/stars/onestardao/WFGY?style=social" alt="GitHub stars"> ⭐ Help reach 10,000 stars by 2025-09-01 to unlock Engine 2.0 for everyone  ⭐ <strong><a href="https://github.com/onestardao/WFGY">Star WFGY on GitHub</a></strong>


<div align="center">

[![WFGY Main](https://img.shields.io/badge/WFGY-Main-red?style=flat-square)](https://github.com/onestardao/WFGY)
&nbsp;
[![TXT OS](https://img.shields.io/badge/TXT%20OS-Reasoning%20OS-orange?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS)
&nbsp;
[![Blah](https://img.shields.io/badge/Blah-Semantic%20Embed-yellow?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlahBlahBlah)
&nbsp;
[![Blot](https://img.shields.io/badge/Blot-Persona%20Core-green?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlotBlotBlot)
&nbsp;
[![Bloc](https://img.shields.io/badge/Bloc-Reasoning%20Compiler-blue?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlocBlocBloc)
&nbsp;
[![Blur](https://img.shields.io/badge/Blur-Text2Image%20Engine-navy?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlurBlurBlur)
&nbsp;
[![Blow](https://img.shields.io/badge/Blow-Game%20Logic-purple?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlowBlowBlow)

</div>

