# Asana — Guardrails and Fix Patterns

Use this page when your RAG or agent flow is orchestrated through **Asana** (rules, webhooks, custom apps) and behavior drifts: tasks duplicate, sections race, or citations don’t match the source.

**Acceptance targets**
- ΔS(question, retrieved) ≤ 0.45
- coverage ≥ 0.70 to the target section
- λ remains convergent across 3 paraphrases

---

## Typical breakpoints → exact fixes

- Webhooks or rules trigger **before** data/index is actually ready  
  Fix No.14: **Bootstrap Ordering** →  
  [Bootstrap Ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md)

- First run after deploy crashes or uses the wrong secret  
  Fix No.16: **Pre-Deploy Collapse** →  
  [Pre-Deploy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)

- Parallel automations create circular waits (task → comment → external job → task)  
  Fix No.15: **Deployment Deadlock** →  
  [Deployment Deadlock](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md)

- High cosine similarity but the retrieved text is not the intended meaning  
  Fix No.5: **Embedding ≠ Semantic** →  
  [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

- Citations don’t match snippets or “why this snippet?” is opaque  
  Fix No.8: **Retrieval Traceability** →  
  [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)  
  Standardize payloads with **Data Contracts** →  
  [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

- Hybrid retrieval via external tools performs worse than single retriever  
  Pattern: **Query Parsing Split** →  
  [Query Parsing Split](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md)  
  Also review **Rerankers** →  
  [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

- Facts are indexed but never surface  
  Pattern: **Vectorstore Fragmentation** →  
  [Vectorstore Fragmentation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md)

- Status rollups blend two sources into one narrative  
  Pattern: **Symbolic Constraint Unlock (SCU)** →  
  [Symbolic Constraint Unlock](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_symbolic_constraint_unlock.md)

---

## Minimal Asana workflow checklist

1) **Warm-up fence**  
   Before any LLM step, call a health endpoint that verifies `VECTOR_READY`, `INDEX_HASH`, `secret_rev`.  
   If not ready, delay/requeue. Spec:  
   [Bootstrap Ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md)

2) **Idempotency**  
   Build `dedupe_key = sha256(task.gid + wf_rev + index_hash)` and store it (custom field or external KV).  
   Drop duplicates on retries.

3) **RAG boundary contract**  
   Always pass `snippet_id`, `section_id`, `source_url`, `offsets`, `tokens`, `project_gid`.  
   Enforce **cite-then-explain**. Specs:  
   [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) ·
   [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

4) **Observability probes**  
   Log ΔS(question, retrieved) and λ per stage; alert on ΔS ≥ 0.60 or divergent λ.  
   Overview map:  
   [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)

5) **Single writer**  
   Route task/comments/field updates through one writer branch or one integration user with a mutex.  
   See:  
   [Deployment Deadlock](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md)

6) **Regression gate**  
   Require coverage ≥ 0.70 and ΔS ≤ 0.45 before posting summaries back to Asana.  
   Eval spec:  
   [RAG Precision/Recall](https://github.com/onestardao/WFGY/blob/main/ProblemMap/eval/eval_rag_precision_recall.md)

---

## Copy-paste prompt for the Asana LLM step

```

I uploaded TXT OS and the WFGY Problem Map files.
This Asana flow retrieved {k} snippets with fields {snippet\_id, section\_id, source\_url, offsets, project\_gid}.
Question: "{user\_question}"

Do:

1. Enforce cite-then-explain. If any citation is missing, stop and return which fix page to open.
2. Compute ΔS(question, retrieved). If ΔS ≥ 0.60, point me to the minimal structural fix:
   retrieval-playbook, retrieval-traceability, data-contracts, rerankers.
3. Output compact JSON:
   { "citations": \[...], "answer": "...", "λ\_state": "→|←|<>|×", "ΔS": 0.xx, "next\_fix": "..." }

```

---

## Common Asana gotchas

- **Webhook retries** produce duplicate tasks/comments  
  Use the `dedupe_key` and a KV lock; make writes idempotent.

- **Project/section renames** break downstream references  
  Pass `project_gid` and `section_id` explicitly in the data contract.

- **Parallel rules** edit the same fields  
  Funnel edits through a single writer branch or queue.

- **External rate limits** destabilize hybrids  
  Prefer dense retriever + reranking, keep per-retriever params logged.

---

## When to escalate

- ΔS remains ≥ 0.60 after chunk/retrieval fixes → rebuild index with explicit metric/normalization.  
  See:  
  [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)

- Same input yields different answers across runs → check version skew and memory desync.  
  See:  
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

