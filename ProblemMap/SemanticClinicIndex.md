# Semantic Clinic Index
**A complete triage hub for AI failures — beyond the core 16 — powered by WFGY.**  
Use this page when you don’t yet know *which thing is breaking*. Start from symptoms, jump to a failure family, then open the exact fix page. All fixes are driven by WFGY instruments: `ΔS` (semantic stress), `λ_observe` (layered observability), and `E_resonance` (coherence control).

> If this page saves you time, a ⭐ helps others find it.

---

## How to use this page
1. **Identify the symptom** in the table below.  
2. **Open the family** (Prompting / Retrieval / Reasoning / Memory / Agents / Infra / Eval).  
3. **Follow the fix page** (existing doc or placeholder) and verify with ΔS ≤ 0.45 and convergent λ.

If you prefer a pipeline-first view (OCR → chunking → embeddings → vector store → retriever → prompt → LLM), read:  
**[`RAG Architecture & Recovery`](./rag-architecture-and-recovery.md)**

---

## Quick triage by symptom

| Symptom you see | Likely family | Open this |
|---|---|---|
| Answers cite wrong snippet / mismatch with ground truth | Retrieval → RAG | [`hallucination.md`](./hallucination.md) |
| Chunks look right but reasoning is wrong | Reasoning | [`retrieval-collapse.md`](./retrieval-collapse.md) |
| High similarity, wrong meaning | Retrieval / Embeddings | [`embedding-vs-semantic.md`](./embedding-vs-semantic.md) |
| Model can’t explain *why* (no trace) | Observability | [`retrieval-traceability.md`](./retrieval-traceability.md) |
| Output collapses over long dialogs / 100k tokens | Memory / Long-context | **(placeholder)** [`long-context-stress.md`](./long-context-stress.md) |
| Jailbreak / prompt injection succeeds | Prompting / Safety | **(placeholder)** [`prompt-injection.md`](./prompt-injection.md) |
| Multi-agent tools fight each other | Orchestration | [`multi-agent-chaos.md`](./multi-agent-chaos.md) |
| First prod call crashes after deploy | Infra / Boot | [`predeploy-collapse.md`](./predeploy-collapse.md) |
| Index looks fine; retrieval is irrelevant | Vector store hygiene | **(placeholder)** [`vectorstore-metrics-and-faiss-pitfalls.md`](./vectorstore-metrics-and-faiss-pitfalls.md) |
| OCR PDFs “look correct” but answers drift | Data / OCR | **(placeholder)** [`ocr-parsing-checklist.md`](./ocr-parsing-checklist.md) |

> Can’t find it? See the full **Failure catalog (16)** in the Problem Map root or scan the families below.

---

## Families & maps (with exact fixes)

### A) Prompting & Safety
Guard against injections, jailbreaks, role drift, and schema leakage.

- **Prompt Injection (attack taxonomies & safe loaders)** — **(placeholder)** [`prompt-injection.md`](./prompt-injection.md)
- **System Prompt Drift (role/constraint slippage)** — **(placeholder)** [`system-prompt-drift.md`](./system-prompt-drift.md)
- **Citation-first, schema-locked prompting** — see [`retrieval-traceability.md`](./retrieval-traceability.md)
- **Overconfidence / bluffing controls** — see [`bluffing.md`](./bluffing.md)
- **Safety Boundary Map (overview)** — see [`Safety_Boundary_Problems.md`](./Safety_Boundary_Problems.md)

**Minimum verification**: ΔS(question, context) ≤ 0.45; λ stays *convergent* across paraphrases; injection probes do not change λ.

---

### B) Retrieval, Data & Vector Stores
Make the index correct, measured, and explainable.

- **Hallucination & Chunk Drift** — [`hallucination.md`](./hallucination.md)  
- **Interpretation vs Retrieval collapse** — [`retrieval-collapse.md`](./retrieval-collapse.md)  
- **Embedding ≠ Semantic Meaning** — [`embedding-vs-semantic.md`](./embedding-vs-semantic.md)  
- **Traceability (why this snippet?)** — [`retrieval-traceability.md`](./retrieval-traceability.md)  
- **Vector store metrics & FAISS pitfalls** (metric flags, normalization, rebuild rules) — **(placeholder)** [`vectorstore-metrics-and-faiss-pitfalls.md`](./vectorstore-metrics-and-faiss-pitfalls.md)  
- **Semantic Chunking Checklist** (boundaries, headers, coverage) — **(placeholder)** [`chunking-checklist.md`](./chunking-checklist.md)  
- **OCR / Parsing Quality Gate** (PDFs, tables, scans) — **(placeholder)** [`ocr-parsing-checklist.md`](./ocr-parsing-checklist.md)

**Minimum verification**: coverage ≥ 0.7 to target section; ΔS(question, retrieved) ≤ 0.45; ΔS(retrieved, anchor) ≤ 0.45; flat-high ΔS vs k ⇒ index/metric mismatch.

---

### C) Reasoning & Logic Control
Detect and repair logic collapse, dead ends, and abstraction failures.

- **Logic Collapse & Recovery** — [`logic-collapse.md`](./logic-collapse.md)  
- **Long Reasoning Chains (context drift)** — [`context-drift.md`](./context-drift.md)  
- **Symbolic Collapse** — [`symbolic-collapse.md`](./symbolic-collapse.md)  
- **Philosophical Recursion** — [`philosophical-recursion.md`](./philosophical-recursion.md)  
- **Reasoning Schemas (cite→explain, bridge nodes)** — **(placeholder)** [`reasoning-schemas.md`](./reasoning-schemas.md)  
- **Tool Router Debug (planner/tool choice)** — **(placeholder)** [`tool-router-debug.md`](./tool-router-debug.md)

**Minimum verification**: if upstream λ is stable but λ flips at reasoning, apply **BBCR** (bridge) and **BBAM** (variance clamp); re-measure until λ stays convergent.

---

### D) Memory & Long-Context
Keep threads coherent across sessions and very long windows.

- **Memory Breaks Across Sessions** — [`memory-coherence.md`](./memory-coherence.md)  
- **Entropy Collapse (attention melt)** — [`entropy-collapse.md`](./entropy-collapse.md)  
- **Long-Context Stress Map** — **(placeholder)** [`long-context-stress.md`](./long-context-stress.md)  
- **Conversation Stitching & Memory Design** — **(placeholder)** [`memory-design-patterns.md`](./memory-design-patterns.md)

**Minimum verification**: E_resonance does not trend upward; ΔS does not spike at window boundaries; stitched turns keep λ convergent.

---

### E) Multi-Agent & Orchestration
Coordinate tools, roles, and shared memory without conflict.

- **Multi-Agent Chaos** — [`multi-agent-chaos.md`](./multi-agent-chaos.md)  
- **Agent Boundary Design** (contracts, shared state, arbitration) — **(placeholder)** [`agent-boundary-design.md`](./agent-boundary-design.md)  
- **Consensus Protocols for Agents** — **(placeholder)** [`agent-consensus-protocols.md`](./agent-consensus-protocols.md)

**Minimum verification**: when agents are isolated, λ is convergent; when coupled, ΔS does not jump and arbitration logs are traceable.

---

### F) Infra / Deploy
Make the system boot in a known-good order, every time.

- **Bootstrap Ordering** — [`bootstrap-ordering.md`](./bootstrap-ordering.md)  
- **Deployment Deadlock** — [`deployment-deadlock.md`](./deployment-deadlock.md)  
- **Pre-Deploy Collapse** — [`predeploy-collapse.md`](./predeploy-collapse.md)  
- **Observability Runbook (retries, backoff, idempotence)** — **(placeholder)** [`observability-runbook.md`](./observability-runbook.md)

**Minimum verification**: idempotent index builds; version/secret checks before first call; deterministic warm-up traces.

---

### G) Evaluation & Guardrails
Detect “double hallucination” and prevent regression.

- **Evaluation Playbook** (ΔS/λ metrics, coverage, cluster variance) — **(placeholder)** [`evaluation-playbook.md`](./evaluation-playbook.md)  
- **WFGY Metrics & Thresholds** — **(placeholder)** [`wfgy-metrics.md`](./wfgy-metrics.md)

**Acceptance**:  
- Retrieval QA: coverage ≥ 0.7 and ΔS(question, context) ≤ 0.45  
- Stability: λ convergent on 3 paraphrases; E_resonance flat  
- Repeatability: 5 seeds cluster in embedding space (low variance)

---

## Ask the AI to fix your AI (safe prompt)
Paste this in any LLM after uploading TXT OS:

```txt
Read the WFGY TXT OS and ProblemMap docs. Extract ΔS, λ_observe, E_resonance and the modules (BBMC, BBPF, BBCR, BBAM).
Given my failure:

- symptom: [describe]
- traces: [ΔS probes, λ states if any]

Tell me:
1) which layer/family is failing and why,
2) which fix page to open,
3) the minimal steps to push ΔS below 0.45 and keep λ convergent,
4) how to verify with a reproducible test.
````

---

## Related maps in the main Problem Map

* **RAG Problem Table (Map-A)** — [`RAG_Problems.md`](./RAG_Problems.md)
* **Safety Boundary Map (Map-F)** — [`Safety_Boundary_Problems.md`](./Safety_Boundary_Problems.md)
* **Infra Boot Map (Map-G)** — [`Infra_Boot_Problems.md`](./Infra_Boot_Problems.md)

---

## Notes on placeholders

Items labeled **(placeholder)** are active stubs. If you have a minimal repro (inputs → calls → wrong output), open an Issue and we will prioritize the write-up.

---

### 🧭 Explore More

| Module                | Description                                                          | Link                                                                                |
| --------------------- | -------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| Semantic Blueprint    | Layer-based symbolic reasoning & semantic modulations                | [View →](https://github.com/onestardao/WFGY/tree/main/SemanticBlueprint)            |
| Benchmark vs GPT-5    | Stress test GPT-5 with full WFGY reasoning suite                     | [View →](https://github.com/onestardao/WFGY/tree/main/benchmarks/benchmark-vs-gpt5) |
| Semantic Clinic Index | Expanded failure catalog: prompt injection, memory bugs, logic drift | [View →](./SemanticClinicIndex.md)                                                  |

---

> 👑 **Early Stargazers: [See the Hall of Fame](https://github.com/onestardao/WFGY/tree/main/stargazers)** —
> Engineers, hackers, and open source builders who supported WFGY from day one.

> <img src="https://img.shields.io/github/stars/onestardao/WFGY?style=social" alt="GitHub stars"> ⭐ Help reach 10,000 stars by 2025-09-01 to unlock Engine 2.0 for everyone  ⭐ **[Star WFGY on GitHub](https://github.com/onestardao/WFGY)**

<div align="center">

[![WFGY Main](https://img.shields.io/badge/WFGY-Main-red?style=flat-square)](https://github.com/onestardao/WFGY)
 
[![TXT OS](https://img.shields.io/badge/TXT%20OS-Reasoning%20OS-orange?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS)
 
[![Blah](https://img.shields.io/badge/Blah-Semantic%20Embed-yellow?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlahBlahBlah)
 
[![Blot](https://img.shields.io/badge/Blot-Persona%20Core-green?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlotBlotBlot)
 
[![Bloc](https://img.shields.io/badge/Bloc-Reasoning%20Compiler-blue?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlocBlocBloc)
 
[![Blur](https://img.shields.io/badge/Blur-Text2Image%20Engine-navy?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlurBlurBlur)
 
[![Blow](https://img.shields.io/badge/Blow-Game%20Logic-purple?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlowBlowBlow)

</div>

