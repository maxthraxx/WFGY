# Make.com Guardrails and Patterns

Use this page when your RAG or agent workflow runs on **Make.com**. It maps typical automation failures to the exact structural fixes in the WFGY Problem Map and gives a minimal recipe you can paste into a scenario.

**Acceptance targets**
- ΔS(question, retrieved) ≤ 0.45
- coverage ≥ 0.70 for the target section
- λ stays convergent across 3 paraphrases

---

## Typical breakpoints and the right fix

- Modules fire before dependencies are ready (Webhook → Tools → RAG too early)  
  Fix No.14: **Bootstrap Ordering** → [Open](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md)

- First production call after deploy crashes, wrong secret selected in Connections  
  Fix No.16: **Pre-Deploy Collapse** → [Open](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)

- Router/Iterator loops create circular waits or partial writes  
  Fix No.15: **Deployment Deadlock** → [Open](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md)

- High cosine similarity but answers are semantically wrong  
  Fix No.5: **Embedding ≠ Semantic** → [Open](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

- Snippet is wrong or citations do not line up with the source  
  Fix No.8: **Retrieval Traceability** → [Open](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)  
  Contract the payload: **Data Contracts** → [Open](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

- Hybrid retrieval (HyDE + BM25 service) performs worse than single retriever  
  Pattern: **Query Parsing Split** → [Open](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md)  
  Also review: **Rerankers** → [Open](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

- Some indexed facts never appear in results  
  Pattern: **Vectorstore Fragmentation** → [Open](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md)

- Two sources are merged into one answer in long chains  
  Pattern: **Symbolic Constraint Unlock (SCU)** → [Open](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_symbolic_constraint_unlock.md)

---

## Minimal scenario checklist

1) **Warm-up fence before RAG/LLM modules**  
   Validate `VECTOR_READY`, `INDEX_HASH` match, and required secrets exist.  
   If not ready, short-circuit to **Sleep** then retry with a capped counter.  
   Spec: [Bootstrap Ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md)

2) **Idempotency and dedupe**  
   Compute `dedupe_key = sha256(source_id + revision + index_hash)` in a **Tools > Code** module.  
   Check a KV (Airtable / Notion / Make Data Store) before side effects. Skip duplicates.

3) **RAG boundary contract**  
   Require fields: `snippet_id`, `section_id`, `source_url`, `offsets`, `tokens`.  
   Enforce cite-then-explain at the LLM step.  
   Specs: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md) ·
   [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)

4) **Observability probes**  
   Log ΔS(question, retrieved) and λ per stage (retrieve, assemble, reason).  
   Alert when ΔS ≥ 0.60 or λ flips divergent.  
   Overview: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)

5) **Router/Iterator safety**  
   Use a **single writer** branch for index updates and external writes.  
   Apply queue mode or mutex; avoid parallel writes to the same index.  
   See: [Deployment Deadlock](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md)

6) **Regression gate**  
   Before publish, require coverage ≥ 0.70 and ΔS ≤ 0.45.  
   Eval: [RAG Precision/Recall](https://github.com/onestardao/WFGY/blob/main/ProblemMap/eval/eval_rag_precision_recall.md)

---

## Scenario pattern (copy)

> Replace the concrete modules with your stack. Keep the guardrails.

1. **Webhook/Trigger**  
   Capture `source_id`, `revision`, `wf_rev`.

2. **Warm-up Check (Tools > Code)**  
   Pull `INDEX_HASH`, `VECTOR_READY`, and secrets.  
   If not ready → set `ready=false`.

3. **Router**  
   - **Not ready** → **Sleep 30–90s**, increment `retry`, stop after N attempts.  
   - **Ready** → continue.

4. **Retriever (HTTP or App)**  
   - Fix metric and normalization; use the same analyzer as the writer.  
   - Output `snippet_id`, `section_id`, `source_url`, `offsets`, `tokens`.

5. **ΔS Probe (Tools > Code)**  
   - Compute ΔS(question, retrieved). If ΔS ≥ 0.60 → tag `needs_fix=true`.

6. **LLM (OpenAI/Claude/Gemini module)**  
   - Load TXT OS; enforce cite-then-explain; return `{ΔS, λ_state, citations, answer}`.

7. **Trace Sink (Data Store / Airtable)**  
   - Write `question`, `snippet_id`, `ΔS`, `λ_state`, `INDEX_HASH`, `dedupe_key`.

8. **Idempotent Writer**  
   - Check `dedupe_key` before any external publish or email.

---

## LLM prompt you can paste

```

I uploaded TXT OS and the WFGY Problem Map files.
This Make.com scenario retrieved {k} snippets with fields {snippet\_id, section\_id, source\_url, offsets}.
Question: "{user\_question}"

Do:

1. Enforce cite-then-explain. If citations are missing, fail fast and return the fix page to open.
2. If ΔS(question, retrieved) ≥ 0.60, propose the minimal structural fix referencing:
   retrieval-playbook, retrieval-traceability, data-contracts, rerankers.
3. Output compact JSON:
   { "citations": \[...], "answer": "...", "λ\_state": "→|←|<>|×", "ΔS": 0.xx, "next\_fix": "..." }

```

---

## Common Make.com gotchas

- **Connections** silently switch between prod and staging  
  Stamp `env`, `INDEX_HASH`, and `secret_rev` into traces; block on mismatch.

- **Array Aggregator / Iterator** duplicates writes  
  Route all writes through a **single writer** with idempotency.

- **Rate-limits** make hybrid queries diverge  
  Prefer reranking with a stable dense retriever; see [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

- **Template mapping** renames fields and breaks the contract  
  Lock schema and run a pre-LLM schema check.

---

## When to escalate

- ΔS stays ≥ 0.60 after chunk/retrieval fixes  
  Rebuild the index with explicit metric/normalization.  
  See: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)

- Same input alternates answers between runs  
  Investigate version skew and memory desync.  
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


say “next page” when ready.
