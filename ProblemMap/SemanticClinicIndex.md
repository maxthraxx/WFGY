<!-- ============================================================= -->
<!--  SemanticClinicIndex.md · Complete triage hub · v2025-08-14   -->
<!--  All key sub-pages cross-linked; thresholds unified.          -->
<!-- ============================================================= -->

# 🏥 Semantic Clinic Index
**A complete triage hub for AI failures — beyond the core 16 — powered by WFGY.**  
Use this page when you don’t yet know *which thing is breaking*. Start from symptoms, jump to a failure family, then open the exact fix page. All fixes are driven by WFGY instruments: `ΔS` (semantic stress), `λ_observe` (layered observability), and `E_resonance` (coherence control).

> If this page saves you time, a ⭐ helps others find it.

---

## Quick Nav
[Getting Started](./getting-started.md) ·
[RAG Problem Map 2.0](./rag-architecture-and-recovery.md) ·
[Patterns Index](./patterns/README.md) ·
[Examples](./examples/README.md) ·
[Eval](./eval/README.md) ·
[Ops](./ops/README.md) ·
[Multi-Agent Problems](./Multi-Agent_Problems.md)

---

## How to use this page
1. **Identify the symptom** in the table below.  
2. **Open the family** (Prompting / Retrieval / Reasoning / Memory / Agents / Infra / Eval).  
3. **Follow the fix page**, then verify with **ΔS ≤ 0.45** and **convergent λ**.

Prefer a pipeline-first view (OCR → chunk → embed → store → retrieve → prompt → LLM)?  
Read **[`RAG Architecture & Recovery`](./rag-architecture-and-recovery.md)**.

Want the full catalog instead? See **[Problem Map Index](./README.md)**.  
🧩 Or, **jump straight to MVP Demos**: [Run minimal WFGY examples →](./mvp_demo/README.md)


---

## Quick triage by symptom

| Symptom you see | Likely family | Open this |
|---|---|---|
| Answers cite wrong snippet / mismatch with ground truth | Retrieval → RAG | [`hallucination.md`](./hallucination.md) |
| Chunks look right but reasoning is wrong | Reasoning | [`retrieval-collapse.md`](./retrieval-collapse.md) |
| High similarity, wrong meaning | Retrieval / Embeddings | [`embedding-vs-semantic.md`](./embedding-vs-semantic.md) |
| Model can’t explain *why* (no trace) | Observability | [`retrieval-traceability.md`](./retrieval-traceability.md) |
| Output degrades over 100k-token dialogs | Memory / Long-context | [`entropy-collapse.md`](./entropy-collapse.md) · [`context-drift.md`](./context-drift.md) |
| OCR PDFs **look** correct yet answers drift | Data / OCR | [`ocr-parsing-checklist.md`](./ocr-parsing-checklist.md) |
| Hybrid (HyDE + BM25) gets worse than single retriever | Retrieval / Querying | [`patterns/pattern_query_parsing_split.md`](./patterns/pattern_query_parsing_split.md) |
| Corrections don’t stick; model re-asserts old claim | Reasoning / Prompting | [`patterns/pattern_hallucination_reentry.md`](./patterns/pattern_hallucination_reentry.md) |
| “Who said what” merges across sources | Prompting / Constraints | [`patterns/pattern_symbolic_constraint_unlock.md`](./patterns/pattern_symbolic_constraint_unlock.md) |
| Some facts can’t be retrieved though indexed | Retrieval / Index | [`patterns/pattern_vectorstore_fragmentation.md`](./patterns/pattern_vectorstore_fragmentation.md) |
| Answers flip between sessions / tabs | Memory / State | [`patterns/pattern_memory_desync.md`](./patterns/pattern_memory_desync.md) |
| Multi-agent tools fight each other | Agents | [`Multi-Agent_Problems.md`](./Multi-Agent_Problems.md) |
| First prod call crashes after deploy | Infra / Boot | [`predeploy-collapse.md`](./predeploy-collapse.md) |
| Tools fire before data is ready (RAG boot fence) | Infra / Boot | [`patterns/pattern_bootstrap_deadlock.md`](./patterns/pattern_bootstrap_deadlock.md) |

> Still lost? Open the **Beginner Guide** symptom checklist first.

---

## Families & maps (with exact fixes)

### A) Prompting & Safety
Guard against injections, role drift, and schema leakage.

- **Citation-first, schema-locked prompting** — [`retrieval-traceability.md`](./retrieval-traceability.md)  
- **Overconfidence / Bluffing Controls** — [`bluffing.md`](./bluffing.md)  
- **Symbolic Constraint Unlock (SCU) / source mixing** — [`patterns/pattern_symbolic_constraint_unlock.md`](./patterns/pattern_symbolic_constraint_unlock.md)

**Verification**: ΔS(question, context) ≤ 0.45; λ remains convergent across paraphrases; constraint probes do not flip λ.

---

### B) Retrieval, Data & Vector Stores
Make the index correct, measured, and explainable.

- **Hallucination & Chunk Drift** — [`hallucination.md`](./hallucination.md)  
- **Interpretation vs Retrieval Collapse** — [`retrieval-collapse.md`](./retrieval-collapse.md)  
- **Embedding ≠ Semantic Meaning** — [`embedding-vs-semantic.md`](./embedding-vs-semantic.md)  
- **Traceability (why this snippet?)** — [`retrieval-traceability.md`](./retrieval-traceability.md)  
- **Vectorstore Fragmentation** — [`patterns/pattern_vectorstore_fragmentation.md`](./patterns/pattern_vectorstore_fragmentation.md)  
- **Query Parsing Split (HyDE/BM25)** — [`patterns/pattern_query_parsing_split.md`](./patterns/pattern_query_parsing_split.md)  
- **Semantic Chunking Checklist** — [`chunking-checklist.md`](./chunking-checklist.md)  
- **OCR / Parsing Quality Gate** — [`ocr-parsing-checklist.md`](./ocr-parsing-checklist.md)

**Verification**: coverage ≥ 0.70 to target section; ΔS(question, retrieved) ≤ 0.45; flat-high ΔS vs k ⇒ index/metric mismatch.

---

### C) Reasoning & Logic Control
Detect and repair logic collapse, dead ends, and abstraction failures.

- **Logic Collapse & Recovery** — [`logic-collapse.md`](./logic-collapse.md)  
- **Long Reasoning Chains** — [`context-drift.md`](./context-drift.md)  
- **Symbolic Collapse** — [`symbolic-collapse.md`](./symbolic-collapse.md)  
- **Philosophical Recursion** — [`philosophical-recursion.md`](./philosophical-recursion.md)  
- **Hallucination Re-entry** — [`patterns/pattern_hallucination_reentry.md`](./patterns/pattern_hallucination_reentry.md)

**Verification**: fix point when λ stays convergent after BBCR (bridge) + BBAM (variance clamp).

---

### D) Memory & Long-Context
Keep threads coherent across sessions and very long windows.

- **Memory Breaks Across Sessions** — [`memory-coherence.md`](./memory-coherence.md)  
- **Entropy Collapse** — [`entropy-collapse.md`](./entropy-collapse.md)  
- **Memory Desync** — [`patterns/pattern_memory_desync.md`](./patterns/pattern_memory_desync.md)

**Verification**: E_resonance flat; ΔS stable at window joins.

---

### E) Multi-Agent & Orchestration
Coordinate tools, roles, and shared memory without conflict.

- **Multi-Agent Chaos (overview map)** — [`Multi-Agent_Problems.md`](./Multi-Agent_Problems.md)  
- **Role Drift (Deep Dive)** — [`multi-agent-chaos/role-drift.md`](./multi-agent-chaos/role-drift.md)  
- **Cross-Agent Memory Overwrite (Deep Dive)** — [`multi-agent-chaos/memory-overwrite.md`](./multi-agent-chaos/memory-overwrite.md)

**Verification**: when agents couple, ΔS does not spike; arbitration logs traceable.

---

### F) Infra / Deploy
Boot in a known-good order, every time.

- **Bootstrap Ordering** — [`bootstrap-ordering.md`](./bootstrap-ordering.md)  
- **Deployment Deadlock** — [`deployment-deadlock.md`](./deployment-deadlock.md)  
- **Pre-Deploy Collapse** — [`predeploy-collapse.md`](./predeploy-collapse.md)  
- **Live Monitoring & Debug Playbook** — [`ops/live_monitoring_rag.md`](./ops/live_monitoring_rag.md) · [`ops/debug_playbook.md`](./ops/debug_playbook.md)

**Verification**: deterministic warm-up; idempotent index builds; version/secret checks pass.

---

### G) Evaluation & Guardrails
Detect “double hallucination” and prevent regression.

- **RAG Precision/Recall** — [`eval/eval_rag_precision_recall.md`](./eval/eval_rag_precision_recall.md)  
- **Latency vs Accuracy** — [`eval/eval_latency_vs_accuracy.md`](./eval/eval_latency_vs_accuracy.md)  
- **Cross-Agent Consistency** — [`eval/eval_cross_agent_consistency.md`](./eval/eval_cross_agent_consistency.md)  
- **Semantic Stability** — [`eval/eval_semantic_stability.md`](./eval/eval_semantic_stability.md)

**Acceptance**: retrieve QA coverage ≥ 0.70 and ΔS ≤ 0.45; λ convergent; repeatability across seeds.

---

## Ask the AI to fix your AI (safe prompt)

```txt
Read the WFGY TXT OS and Problem Map docs. Extract ΔS, λ_observe, E_resonance and the modules (BBMC, BBPF, BBCR, BBAM).
Given my failure:

- symptom: [describe]
- traces: [ΔS probes, λ states if any]

Tell me:
1) which layer/family is failing and why,
2) which fix page to open,
3) minimal steps to push ΔS ≤ 0.45 and keep λ convergent,
4) how to verify the fix.
````

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
| 🧙‍♂️ Starter Village 🏡 | New here? Lost in symbols? Click here and let the wizard guide you through | [Start →](https://github.com/onestardao/WFGY/blob/main/StarterVillage/README.md) |

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


