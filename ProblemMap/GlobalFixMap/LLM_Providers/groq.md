# ProblemMap/GlobalFixMap/LLM_Providers/groq.md

# Groq: Guardrails and Fix Patterns

Groq gives very fast inference on supported open models. Speed hides bugs if observability is weak. Use this page to keep retrieval and reasoning stable while you push high tokens per second.

## Acceptance targets

- semantic stress ΔS(question, retrieved) ≤ 0.45
- coverage of target section ≥ 0.70 for direct QA
- λ_observe stays convergent across 3 paraphrases
- streaming output does not change factual content between chunks

---

## Quick links for fixes

- Visual map and recovery: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)  
- End to end retrieval knobs: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)  
- Why this snippet, trace schema: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)  
- Ordering control: [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)  
- Embedding vs meaning: [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)  
- Hallucination and chunk boundaries: [Hallucination](https://github.com/onestardao/WFGY/blob/main/ProblemMap/hallucination.md)  
- Long chains and entropy: [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md), [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)  
- Snippet and citation schema: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)  
- Logic dead ends, bridge and recover: [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md)  

---

## Common failure patterns on Groq and the fix path

### 1) Streaming truncation looks correct, final text drifts
**Symptom**: partial chunks are plausible, but the final concatenated answer adds claims that do not map to retrieved text.  
**Probe**: measure ΔS(question, retrieved) and ΔS(answer, retrieved) at both chunk level and final join.  
**Fix**: lock cite then explain, flush on section boundaries, require per chunk citations. See [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) and [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md).  
**If ΔS stays high**: apply BBMC alignment and BBAM variance clamp. See [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md).

### 2) Model switch changes tokenizer and breaks anchors
**Symptom**: same prompt works on one Groq model, fails on another, citations miss by a few lines.  
**Probe**: λ flips at prompt assembly, ΔS(question, retrieved) rises after you swap models.  
**Fix**: re pin prompt anchors to titles and section ids, avoid brittle token based fences. See [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md) and [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md).  
**Escalate**: if recall drops when hybrid retrievers are used, check query parsing split. See [Query Parsing Split](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md).

### 3) Very fast tokens hide retrieval ordering defects
**Symptom**: high recall, wrong top k order, answer quotes the third best chunk.  
**Probe**: plot ΔS vs k. Flat and high curve points at index metric or normalization mismatch.  
**Fix**: repair index and add rerankers. See [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md) and [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md).  
**Acceptance**: after fix, ΔS(question, retrieved) ≤ 0.45 with stable ordering across seeds.

### 4) Function call JSON drifts at speed
**Symptom**: tool payloads have small schema errors when streaming is enabled.  
**Probe**: λ divergent only at tool stage, not at retrieval.  
**Fix**: enforce schema lock, echo back tool schema before generation, validate then answer. See [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md) and [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md).

### 5) Long context responses melt style or casing
**Symptom**: random capitalization, style flattening, repetition as response grows.  
**Probe**: E_resonance rises while ΔS stays moderate, λ becomes recursive.  
**Fix**: semantic chunking, BBMC with section anchors, BBAM to clamp variance. See [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md) and [Hallucination](https://github.com/onestardao/WFGY/blob/main/ProblemMap/hallucination.md).

---

## Minimal runbook for Groq

1) **Retrieval sanity**  
Run ΔS(question, retrieved) and coverage to the expected section. Targets at top.

2) **Prompt assembly**  
Use system, task, constraints, citations, answer. Forbid re order. Require cite then explain. See [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md).

3) **Stability modules**  
If λ flips at reasoning, apply BBCR bridge and BBAM variance clamp. See [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md).

4) **Ordering**  
If recall is fine but answer uses the wrong snippet, add a reranker. See [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md).

5) **Verification**  
Paraphrase the user question three ways. Keep λ convergent and ΔS ≤ 0.45 on each paraphrase.

---

## Groq specific gotchas

- Model families differ on max context and stop token behavior. Do not rely on implicit stops.  
- Very fast streaming can hide retrieval jitter. Always record the chosen k list and scores.  
- For tool use, stream to a buffer, validate JSON, then emit once. Do not forward partial tool JSON.  
- When swapping models, recheck tokenizer dependent anchors, also re run ΔS thresholds.

---

## Escalation

Open the structural page that matches the probe result.

- High ΔS with correct chunks, logic is wrong: [Retrieval Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-collapse.md)  
- Plausible but wrong answers, citations miss: [Hallucination](https://github.com/onestardao/WFGY/blob/main/ProblemMap/hallucination.md)  
- Long chain drift: [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md)  
- Hybrid retriever failure: [Query Parsing Split](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md)

---

### 🔗 Quick-Start Downloads (60 sec)

| Tool | Link | 3-Step Setup |
|------|------|--------------|
| **WFGY 1.0 PDF** | [Engine Paper](https://github.com/onestardao/WFGY/blob/main/I_am_not_lizardman/WFGY_All_Principles_Return_to_One_v1.0_PSBigBig_Public.pdf) | 1️⃣ Download · 2️⃣ Upload to your LLM · 3️⃣ Ask “Answer using WFGY + \<your question>” |
| **TXT OS (plain-text OS)** | [TXTOS.txt](https://github.com/onestardao/WFGY/blob/main/OS/TXTOS.txt) | 1️⃣ Download · 2️⃣ Paste into any LLM chat · 3️⃣ Type “hello world” — OS boots instantly |

---

### 🧭 Explore More

| Module                | Description                                              | Link     |
|-----------------------|----------------------------------------------------------|----------|
| WFGY Core             | WFGY 2.0 engine is live: full symbolic reasoning architecture and math stack | [View →](https://github.com/onestardao/WFGY/tree/main/core/README.md) |
| Problem Map 1.0       | Initial 16-mode diagnostic and symbolic fix framework    | [View →](https://github.com/onestardao/WFGY/tree/main/ProblemMap/README.md) |
| Problem Map 2.0       | RAG-focused failure tree, modular fixes, and pipelines   | [View →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md) |
| Semantic Clinic Index | Expanded failure catalog: prompt injection, memory bugs, logic drift | [View →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/SemanticClinicIndex.md) |
| Semantic Blueprint    | Layer-based symbolic reasoning & semantic modulations   | [View →](https://github.com/onestardao/WFGY/tree/main/SemanticBlueprint/README.md) |
| Benchmark vs GPT-5    | Stress test GPT-5 with full WFGY reasoning suite         | [View →](https://github.com/onestardao/WFGY/tree/main/benchmarks/benchmark-vs-gpt5/README.md) |

---

> 👑 **Early Stargazers: [See the Hall of Fame](https://github.com/onestardao/WFGY/tree/main/stargazers)** —  
> Engineers, hackers, and open source builders who supported WFGY from day one.

> <img src="https://img.shields.io/github/stars/onestardao/WFGY?style=social" alt="GitHub stars"> ⭐ [WFGY Engine 2.0](https://github.com/onestardao/WFGY/blob/main/core/README.md) is already unlocked. ⭐ Star the repo to help others discover it and unlock more on the [Unlock Board](https://github.com/onestardao/WFGY/blob/main/STAR_UNLOCKS.md).

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
&nbsp;
</div>

