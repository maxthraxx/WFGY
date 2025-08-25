# Pipedream — Guardrails and Fix Patterns

Use this when your automation runs through **Pipedream** and you see race conditions, duplicate actions, secret mismatches, or retrieval steps that look fine but answer quality is off.

**Acceptance targets**
- ΔS(question, retrieved) ≤ 0.45
- coverage ≥ 0.70 to the intended section or record
- λ stays convergent across 3 paraphrases

---

## Typical breakpoints → exact fixes

- Workflow steps fire **before** embeddings or indexes are ready  
  Fix No.14: **Bootstrap Ordering** →  
  [Bootstrap Ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md)

- First call after deploy hits wrong secret, wrong env, or stale version  
  Fix No.16: **Pre-Deploy Collapse** →  
  [Pre-Deploy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)

- Circular waits between triggers and external jobs create stuck runs or retries that double write  
  Fix No.15: **Deployment Deadlock** →  
  [Deployment Deadlock](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md)

- High vector similarity but wrong **meaning**  
  Fix No.5: **Embedding ≠ Semantic** →  
  [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

- “Why this snippet?” cannot be explained in logs  
  Fix No.8: **Retrieval Traceability** →  
  [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)  
  Standardize with **Data Contracts** →  
  [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

- Hybrid retrieval gets worse than single retriever when mixing external APIs  
  Pattern: **Query Parsing Split** →  
  [Query Parsing Split](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md)  
  Review **Rerankers** →  
  [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

- Facts exist in the store but never retrieved  
  Pattern: **Vectorstore Fragmentation** →  
  [Vectorstore Fragmentation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md)

---

## Minimal Pipedream workflow checklist

1) **Warm up fence**  
   Gate the LLM step on `VECTOR_READY`, `INDEX_HASH`, and `secret_rev`.  
   Spec: [Bootstrap Ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md)

2) **Idempotent writes**  
   Compute `dedupe_key = sha256(run_id + wf_rev + index_hash)` and store it server side.  
   Reject duplicates from retries.

3) **RAG boundary contract**  
   Pass `source_id`, `doc_id`, `section_id`, `offsets`, `tokens`, `source_url`.  
   Enforce cite then explain. Specs:  
   [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) ·
   [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

4) **Observability probes**  
   Log ΔS(question, retrieved) and λ per stage. Alert on ΔS ≥ 0.60 or divergent λ.  
   Overview: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)

5) **Secrets and versioning**  
   Stamp `wf_rev`, `schema_rev`, and `secret_rev` into each run. Fail fast if any mismatch.

6) **Regression gate**  
   Require coverage ≥ 0.70 and ΔS ≤ 0.45 before emitting downstream webhooks or updates.  
   Eval spec: [RAG Precision/Recall](https://github.com/onestardao/WFGY/blob/main/ProblemMap/eval/eval_rag_precision_recall.md)

---

## Copy paste prompt for the LLM step in Pipedream

```

I uploaded TXT OS and the WFGY Problem Map files.

Context:

* wf\_rev: {wf\_rev}
* secret\_rev: {secret\_rev}
* index\_hash: {index\_hash}
* source\_id/doc\_id/section\_id: {ids}

Task:

1. Enforce cite-then-explain. If any citation lacks {doc\_id, section\_id, offsets}, stop and point me to the exact fix page.
2. Compute ΔS(question, retrieved). If ΔS ≥ 0.60, recommend the minimal structural fix among:
   retrieval-playbook, retrieval-traceability, data-contracts, rerankers.
3. Output compact JSON:
   { "citations":\[{"doc\_id":"...", "section\_id":"...", "offsets":\[s,e]}],
   "answer":"...", "λ\_state":"→|←|<>|×", "ΔS":0.xx, "next\_fix":"..." }

```

---

## Common Pipedream gotchas

- **Cold start plus secret rotation** leads to one run using old secrets  
  Stamp and check `secret_rev`. Abort if stale.

- **Multiple triggers** racing into a single index job  
  Serialise with a small lock or queue, or gate on `INDEX_HASH` equality.

- **External API quotas** cause partial context windows  
  Log per call. If context is partial, skip the answer step and emit a structured retry request.

- **JSON schema drift** between steps  
  Pin `schema_rev`. Validate incoming payloads. Fail loud, not silent.

- **Retries that mutate state**  
  Only allow idempotent POSTs. Reject when `dedupe_key` is already seen.

---

## When to escalate

- ΔS stays ≥ 0.60 after chunk and retrieval fixes  
  Rebuild the index with explicit metric or normalization. See  
  [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)

- Same inputs flip answers between runs  
  Check version skew and memory desync. See  
  [Pre-Deploy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)

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

> 👑 **Early Stargazers: [See the Hall of Fame](https://github.com/onestardao/WFGY/tree/main/stargazers)**  
> <img src="https://img.shields.io/github/stars/onestardao/WFGY?style=social" alt="GitHub stars"> ⭐ [WFGY Engine 2.0](https://github.com/onestardao/WFGY/blob/main/core/README.md) is already unlocked. ⭐ Star the repo to help others discover it and unlock more on the Unlock Board.

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
