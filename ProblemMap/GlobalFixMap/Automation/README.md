# Automation & Integrations — Index
Zapier / Make / n8n adapters for RAG pipelines and agent workflows. Use this page to route automation bugs to the right structural fix and verify with ΔS ≤ 0.45 and convergent λ.

## Quick links (tool adapters)
- **Zapier Guardrails:** [open](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Automation/zapier.md)
- **Make (Integromat) Guardrails:** [open](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Automation/make.md)
- **n8n Guardrails:** [open](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Automation/n8n.md)

## What typically breaks in automations
- **No.14 Bootstrap ordering:** tools fire before deps are ready (e.g., vector index empty, secrets missing).  
  Fix spec: [Bootstrap Ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md)
- **No.15 Deployment deadlock:** circular waits between retriever/index, DB/migrator, or tool auth loops.  
  Fix spec: [Deployment Deadlock](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md)
- **No.16 Pre-deploy collapse:** first call after deploy crashes due to version skew / missing env.  
  Fix spec: [Pre-Deploy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)
- **RAG miswiring:** wrong field mapping → the retriever queries an empty/partial store; citations don’t line up.  
  Fix spec: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) · [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
- **Hybrid retrievers acting weird:** HyDE + BM25 tokenization split, noisy ordering.  
  Fix spec: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md) · [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)
- **Webhook storms / duplicates:** idempotency keys missing; retries create conflicting states.  
  Pattern: [Bootstrap Deadlock (semantic boot fence)](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_bootstrap_deadlock.md)

## Minimal repair checklist (paste into your runbook)
1) **Warm-up fence before LLM/RAG steps**  
   - Check `VECTOR_READY == true`, `INDEX_HASH` matches, and secret set present.  
   - If not ready → short-circuit flow and retry with backoff.  
   Specs: [bootstrap-ordering.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md)
2) **Idempotent triggers**  
   - Deduplicate by `(source_id, revision, hash)`; discard stale retries.  
3) **RAG contract at the boundary**  
   - Require `snippet_id`, `section_id`, `source_url`, `offsets`.  
   - Enforce cite → then explain; forbid cross-section reuse.  
   Specs: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md) · [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
4) **Observability probes**  
   - Log `ΔS(question, retrieved)` and λ state per step; alert when ΔS ≥ 0.60.  
   Reference: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
5) **Fail the merge on regression**  
   - Add CI gate for coverage ≥ 0.70 and ΔS ≤ 0.45.  
   Eval: [eval_rag_precision_recall.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/eval/eval_rag_precision_recall.md)

## How to route a live bug
- **Looks fine but answers are wrong:** run ΔS and coverage → if high/low, fix chunking/retrieval first.  
  Start: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
- **First run after deploy fails:** jump to infra fixes.  
  Start: [predeploy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)
- **Hybrid ranking is chaotic:** confirm tokenizer parity → consider reranker clamp.  
  Start: [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

## Copy/paste prompt (safe to use with your assistant)
```

I’m running an automation flow (Zapier/Make/n8n) that calls a RAG step.
Read the WFGY Problem Map pages for bootstrap-ordering, predeploy-collapse,
retrieval-traceability, data-contracts, and retrieval-playbook.
Propose the minimal structural fixes to achieve:

* ΔS(question, retrieved) ≤ 0.45
* coverage ≥ 0.70
* convergent λ across 3 paraphrases
  Return a step-by-step checklist I can paste into my scenario.

```

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
