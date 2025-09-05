# LangChain Guardrails and Patterns

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **Automation Platforms**.  
  > To reorient, go back here:  
  >
  > - [**Automation Platforms** — stabilize no-code workflows and integrations](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>

Use this page when your RAG or agent workflow runs in **LangChain**. It maps common orchestration failures to the exact structural fixes in the Problem Map and gives a minimal recipe you can embed in a chain or agent.

**Core acceptance**

* ΔS(question, retrieved) ≤ 0.45
* coverage ≥ 0.70 for the target section
* λ stays convergent across 3 paraphrases

---

## Typical breakpoints and the right fix

* **Chains run before retriever or vectorstore is ready**
  Fix No.14: **Bootstrap Ordering** → [Open](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md)

* **First query after deploy crashes due to env/secret mismatch**
  Fix No.16: **Pre-Deploy Collapse** → [Open](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)

* **Event loop deadlocks when retriever and synthesis wait on each other**
  Fix No.15: **Deployment Deadlock** → [Open](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md)

* **Embedding distance looks fine but semantics drift**
  Fix No.5: **Embedding ≠ Semantic** → [Open](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

* **Output citations don’t map to snippets**
  Fix No.8: **Retrieval Traceability** → [Open](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
  Contract payloads with: **Data Contracts** → [Open](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

* **Hybrid retrieval chains underperform**
  Pattern: **Query Parsing Split** → [Open](https://github.com/onestardao/WFGY/blob/main/ProblemMap/query_parsing_split.md)
  Review: **Rerankers** → [Open](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

* **Facts indexed but never surfaced**
  Pattern: **Vectorstore Fragmentation** → [Open](https://github.com/onestardao/WFGY/blob/main/ProblemMap/vectorstore-fragmentation.md)

* **Two knowledge sources get blended in a single answer**
  Pattern: **Symbolic Constraint Unlock (SCU)** → [Open](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_symbolic_constraint_unlock.md)

---

## Minimal setup checklist for LangChain flows

1. **Warm-up fence**
   Check vectorstore readiness and index hash. If mismatch, retry or short-circuit.
   Spec: [Bootstrap Ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md)

2. **Idempotency key**
   Before persisting outputs, compute a dedupe key from `(doc_id + rev + index_hash)`.

3. **Contracted retriever outputs**
   Must emit: `snippet_id, section_id, source_url, offsets, tokens`.
   Enforce cite-then-explain.
   Specs: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md) · [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)

4. **Observability probes**
   Log ΔS for retrieval steps and λ state transitions.
   Overview: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)

5. **Concurrency guard**
   Use a single writer pattern for retriever updates.
   See: [Deployment Deadlock](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md)

6. **Eval before publish**
   Run precision/recall probes.
   Eval: [RAG Precision/Recall](https://github.com/onestardao/WFGY/blob/main/ProblemMap/eval/eval_rag_precision_recall.md)

---

## Copy-paste prompt for LangChain LLMChain

```
You have access to TXT OS and WFGY Problem Map files.
This retriever produced {k} docs with fields {snippet_id, section_id, source_url, offsets}.

Do:

1. Enforce cite-then-explain. If citations are missing, stop and return fix tip.
2. If ΔS(question, retrieved) ≥ 0.60, propose minimal structural fix referencing:
   retrieval-playbook, retrieval-traceability, data-contracts, rerankers.
3. Output JSON plan:
   { "citations": [...], "answer": "...", "λ_state": "...", "ΔS": 0.xx, "next_fix": "..." }
```

---

## Common LangChain gotchas

* **Async chains** drop context windows or run steps before retrievers return.
  Solution: enforce await barriers, or wrap with guard nodes.

* **Tool/agent outputs exceed JSON mode limits**
  Add schema locks and contract enforcement before passing downstream.

* **Retriever mismatch** between indexer and chain (different casing/tokenizer)
  Fix: normalize pipelines, or enable reranking.
  See: [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

* **Long context windows collapse into filler**
  Monitor entropy. If collapse, trigger recovery.
  See: [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)

---

## When to escalate

* ΔS remains ≥ 0.60 even after chunking and retriever fixes
  → Rebuild vectorstore with explicit metric + normalization.
  Spec: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)

* Identical inputs yield divergent answers
  → Investigate long-context drift.
  Spec: [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md)

---

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
| 🧙‍♂️ Starter Village 🏡 | New here? Lost in symbols? Click here and let the wizard guide you through | [Start →](https://github.com/onestardao/WFGY/blob/main/StarterVillage/README.md) |

---

> 👑 **Early Stargazers: [See the Hall of Fame](https://github.com/onestardao/WFGY/tree/main/stargazers)** —  
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
