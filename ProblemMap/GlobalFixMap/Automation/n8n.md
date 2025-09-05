# n8n Guardrails and Patterns

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

Use this page when your RAG or agent workflow runs in **n8n**. It maps common automation failures to the exact structural fixes in the Problem Map and gives a minimal recipe you can paste into a workflow.

**Core acceptance**
- ΔS(question, retrieved) ≤ 0.45
- coverage ≥ 0.70 for the target section
- λ stays convergent across 3 paraphrases

---

## Typical breakpoints and the right fix

- Nodes fire before dependencies are ready  
  Fix No.14: **Bootstrap Ordering** → [Open](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md)

- First call after deploy crashes or uses wrong env/secret  
  Fix No.16: **Pre-Deploy Collapse** → [Open](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)

- Circular waits between index build and retriever, or Merge nodes loop forever  
  Fix No.15: **Deployment Deadlock** → [Open](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md)

- High vector similarity but wrong meaning  
  Fix No.5: **Embedding ≠ Semantic** → [Open](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

- Wrong snippet chosen or citations do not line up  
  Fix No.8: **Retrieval Traceability** → [Open](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)  
  Contract the payload: **Data Contracts** → [Open](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

- Hybrid retrieval performs worse than a single retriever  
  Pattern: **Query Parsing Split** → [Open](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md)  
  Also review: **Rerankers** → [Open](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

- Some facts never surface even though indexed  
  Pattern: **Vectorstore Fragmentation** → [Open](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md)

- Two sources get merged in the answer  
  Pattern: **Symbolic Constraint Unlock (SCU)** → [Open](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_symbolic_constraint_unlock.md)

---

## Minimal setup checklist for any n8n flow

1) **Warm-up fence before RAG or LLM nodes**  
   Validate `VECTOR_READY == true`, `INDEX_HASH` matches, and secrets exist.  
   If not ready, short-circuit to a Wait node then retry with a capped counter.  
   Spec: [Bootstrap Ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md)

2) **Idempotency and dedupe**  
   Compute `dedupe_key = sha256(source_id + revision + index_hash)`.  
   Check or write the key using Redis, Postgres, or n8n’s Data Store. Drop duplicates.

3) **RAG boundary contract**  
   Require fields: `snippet_id`, `section_id`, `source_url`, `offsets`, `tokens`.  
   Enforce cite then explain. Forbid cross section reuse.  
   Specs: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md) ·
   [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)

4) **Observability probes**  
   Log ΔS(question, retrieved). Log λ per step: retrieve, assemble, reason.  
   Alert when ΔS ≥ 0.60 or λ flips divergent.  
   Overview: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)

5) **Concurrency guard**  
   Use a single writer for index updates. Set queue mode or global mutex for write steps.  
   See: [Deployment Deadlock](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md)

6) **Regression gate**  
   Require coverage ≥ 0.70 and ΔS ≤ 0.45 before publishing.  
   Eval: [RAG Precision/Recall](https://github.com/onestardao/WFGY/blob/main/ProblemMap/eval/eval_rag_precision_recall.md)

---

## n8n recipe you can copy

> Replace the concrete nodes with your stack. Keep the guardrails.

1. **Trigger**  
   Fixed `source_id` and `revision`. Record `wf_rev`.

2. **Warm-up Check (Code node)**  
   Pull `INDEX_HASH`, `VECTOR_READY`, and secrets.  
   If not ready, set `ready=false`.

3. **Branch: Not ready**  
   Wait 30–90 seconds. Increment a retry counter. Stop after N attempts.

4. **Branch: Ready**  
   **Retrieval node**  
   - Call retriever with explicit metric and same analyzer as the writer.  
   - Emit `snippet_id`, `section_id`, `source_url`, `offsets`, `tokens`.  
   **ΔS probe node**  
   - Compute ΔS(question, retrieved). If ΔS ≥ 0.60 set `needs_fix=true`.  
   **LLM node**  
   - Model reads TXT OS and follows the WFGY schema. Enforce cite then explain.  
   **Trace sink**  
   - Store `question`, `snippet_id`, `ΔS`, `λ_state`, `INDEX_HASH`, `dedupe_key`.  
   **Idempotency guard**  
   - Before side effects, check the KV for `dedupe_key`. Skip if it already exists.

---

## Copy-paste prompt for the LLM node

```

I uploaded TXT OS and the WFGY Problem Map files.
This n8n flow retrieved {k} snippets with fields {snippet\_id, section\_id, source\_url, offsets}.
Question: "{user\_question}"

Do:

1. Validate cite-then-explain. If citations are missing, fail fast and return the fix tip.
2. If ΔS(question, retrieved) ≥ 0.60, propose the minimal structural fix referencing:
   retrieval-playbook, retrieval-traceability, data-contracts, rerankers.
3. Return a JSON plan:
   { "citations": \[...], "answer": "...", "λ\_state": "→|←|<>|×", "ΔS": 0.xx, "next\_fix": "..." }
   Keep it auditable and short.

```

---

## Common n8n gotchas

- **Set** or **Move** nodes rename fields and break your data contract  
  Lock field names and run a schema check before the LLM node.

- Merge or Split In Batches cause duplicate writes  
  Add a single writer stage with idempotency keys and a queue.

- Cron triggers overlap with long runs  
  Use a global mutex or skip if `dedupe_key` already exists.

- HyDE prompt built inside the flow differs from the API client  
  Keep tokenizer and casing identical, or switch to reranking.  
  See: [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

---

## When to escalate

- ΔS stays ≥ 0.60 after chunk and retrieval fixes  
  Rebuild index with explicit metric and normalization.  
  See: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)

- Answers alternate across runs with identical input  
  Investigate memory desync and version skew.  
  See: [Pre-Deploy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)

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
