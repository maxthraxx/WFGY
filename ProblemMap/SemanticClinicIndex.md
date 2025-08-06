<!-- ============================================================= -->
<!--  SemanticClinicIndex.md · Complete triage hub · v2025-08-06    -->
<!--  All sub-pages implemented — no placeholders remain.           -->
<!-- ============================================================= -->

# 🏥 Semantic Clinic Index  
**A complete triage hub for AI failures — beyond the core 16 — powered by WFGY.**  
Use this page when you don’t yet know *which thing is breaking*. Start from symptoms, jump to a failure family, then open the exact fix page. All fixes are driven by WFGY instruments: `ΔS` (semantic stress), `λ_observe` (layered observability), and `E_resonance` (coherence control).

> If this page saves you time, a ⭐ helps others find it.

---

## How to use this page
1. **Identify the symptom** in the table below.  
2. **Open the family** (Prompting / Retrieval / Reasoning / Memory / Agents / Infra / Eval).  
3. **Follow the fix page**, then verify with ΔS ≤ 0.45 and convergent λ.

Prefer a pipeline-first view (OCR → chunk → embed → store → retrieve → prompt → LLM)?  
Read **[`RAG Architecture & Recovery`](./rag-architecture-and-recovery.md)**.

---

## Quick triage by symptom

| Symptom you see | Likely family | Open this |
|---|---|---|
| Answers cite wrong snippet / mismatch with ground truth | Retrieval → RAG | [`hallucination.md`](./hallucination.md) |
| Chunks look right but reasoning is wrong | Reasoning | [`retrieval-collapse.md`](./retrieval-collapse.md) |
| High similarity, wrong meaning | Retrieval / Embeddings | [`embedding-vs-semantic.md`](./embedding-vs-semantic.md) |
| Model can’t explain *why* (no trace) | Observability | [`retrieval-traceability.md`](./retrieval-traceability.md) |
| Output collapses over long dialogs / 100 k tokens | Memory / Long-context | [`long-context-stress.md`](./long-context-stress.md) |
| Jailbreak or prompt injection succeeds | Prompting / Safety | [`prompt-injection.md`](./prompt-injection.md) |
| Vector store index “looks fine” but retrieval irrelevant | Retrieval / Data | [`vectorstore-metrics-and-faiss-pitfalls.md`](./vectorstore-metrics-and-faiss-pitfalls.md) |
| OCR PDFs **look** correct yet answers drift | Data / OCR | [`ocr-parsing-checklist.md`](./ocr-parsing-checklist.md) |
| Multi-agent tools fight each other | Agents | [`multi-agent-chaos.md`](./multi-agent-chaos.md) |
| First prod call crashes after deploy | Infra / Boot | [`predeploy-collapse.md`](./predeploy-collapse.md) |

> Still lost? Open the **Beginner Guide** symptom checklist first.

---

## Families & maps (with exact fixes)

### A) Prompting & Safety
Guard against injections, jailbreaks, role drift, and schema leakage.

- **Prompt Injection** — [`prompt-injection.md`](./prompt-injection.md)  
- **System Prompt Drift** — [`system-prompt-drift.md`](./system-prompt-drift.md)  
- **Citation-first, schema-locked prompting** — [`retrieval-traceability.md`](./retrieval-traceability.md)  
- **Overconfidence / Bluffing Controls** — [`bluffing.md`](./bluffing.md)  
- **Safety Boundary Map (overview)** — [`Safety_Boundary_Problems.md`](./Safety_Boundary_Problems.md)

**Verification**: ΔS(question, context) ≤ 0.45; λ remains convergent across paraphrases; injection probes do not flip λ.

---

### B) Retrieval, Data & Vector Stores
Make the index correct, measured, and explainable.

- **Hallucination & Chunk Drift** — [`hallucination.md`](./hallucination.md)  
- **Interpretation vs Retrieval Collapse** — [`retrieval-collapse.md`](./retrieval-collapse.md)  
- **Embedding ≠ Semantic Meaning** — [`embedding-vs-semantic.md`](./embedding-vs-semantic.md)  
- **Traceability (why this snippet?)** — [`retrieval-traceability.md`](./retrieval-traceability.md)  
- **Vector Store Metrics & FAISS Pitfalls** — [`vectorstore-metrics-and-faiss-pitfalls.md`](./vectorstore-metrics-and-faiss-pitfalls.md)  
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
- **Reasoning Schemas (cite → explain, bridge nodes)** — [`reasoning-schemas.md`](./reasoning-schemas.md)  
- **Tool Router Debug** — [`tool-router-debug.md`](./tool-router-debug.md)

**Verification**: fix point when λ stays convergent after applying BBCR (bridge) + BBAM (variance clamp).

---

### D) Memory & Long-Context
Keep threads coherent across sessions and very long windows.

- **Memory Breaks Across Sessions** — [`memory-coherence.md`](./memory-coherence.md)  
- **Entropy Collapse** — [`entropy-collapse.md`](./entropy-collapse.md)  
- **Long-Context Stress Map** — [`long-context-stress.md`](./long-context-stress.md)  
- **Conversation Stitching & Memory Design** — [`memory-design-patterns.md`](./memory-design-patterns.md)

**Verification**: E_resonance flat; ΔS stable at window joins.

---

### E) Multi-Agent & Orchestration
Coordinate tools, roles, and shared memory without conflict.

- **Multi-Agent Chaos** — [`multi-agent-chaos.md`](./multi-agent-chaos.md)  
- **Agent Boundary Design** — [`agent-boundary-design.md`](./agent-boundary-design.md)  
- **Consensus Protocols for Agents** — [`agent-consensus-protocols.md`](./agent-consensus-protocols.md)

**Verification**: when agents couple, ΔS does not spike; arbitration logs traceable.

---

### F) Infra / Deploy
Boot in a known-good order, every time.

- **Bootstrap Ordering** — [`bootstrap-ordering.md`](./bootstrap-ordering.md)  
- **Deployment Deadlock** — [`deployment-deadlock.md`](./deployment-deadlock.md)  
- **Pre-Deploy Collapse** — [`predeploy-collapse.md`](./predeploy-collapse.md)  
- **Observability Runbook** — [`observability-runbook.md`](./observability-runbook.md)

**Verification**: deterministic warm-up; idempotent index builds; version/secret checks pass.

---

### G) Evaluation & Guardrails
Detect “double hallucination” and prevent regression.

- **Evaluation Playbook** — [`evaluation-playbook.md`](./evaluation-playbook.md)  
- **WFGY Metrics Spec** — [`wfgy-metrics.md`](./wfgy-metrics.md)

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

| Module                | Description                                           | Link                                                                                |
| --------------------- | ----------------------------------------------------- | ----------------------------------------------------------------------------------- |
| Semantic Blueprint    | Layer-based symbolic reasoning & semantic modulations | [View →](https://github.com/onestardao/WFGY/tree/main/SemanticBlueprint)            |
| Benchmark vs GPT-5    | Stress-test GPT-5 with full WFGY reasoning suite      | [View →](https://github.com/onestardao/WFGY/tree/main/benchmarks/benchmark-vs-gpt5) |
| Semantic Clinic Index | (you are here) full failure catalog                   | –                                                                                   |

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
