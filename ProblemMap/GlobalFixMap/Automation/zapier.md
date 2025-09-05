# Zapier Guardrails and Patterns

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

Use this page when your RAG or agent flow runs in Zapier. It routes common automation failures to the exact structural fixes in the Problem Map and gives a minimal recipe you can paste into a Zap.

**Core acceptance**
- ΔS(question, retrieved) ≤ 0.45
- coverage ≥ 0.70 for the target section
- λ stays convergent across 3 paraphrases

---

## Typical breakpoints and the right fix

- Tools fire before dependencies are ready  
  Fix No.14: **Bootstrap Ordering** → [Open](../../bootstrap-ordering.md)

- First call after deploy crashes or uses wrong version  
  Fix No.16: **Pre-Deploy Collapse** → [Open](../../predeploy-collapse.md)

- Circular waits between index and retriever or auth loops  
  Fix No.15: **Deployment Deadlock** → [Open](../../deployment-deadlock.md)

- High vector similarity but wrong meaning  
  Fix No.5: **Embedding ≠ Semantic** → [Open](../../embedding-vs-semantic.md)

- Wrong snippet selected or citations do not line up  
  Fix No.8: **Retrieval Traceability** → [Open](../../retrieval-traceability.md)  
  Contract the payload: **Data Contracts** → [Open](../../data-contracts.md)

- Hybrid retrieval performs worse than a single retriever  
  Pattern: **Query Parsing Split** → [Open](../../patterns/pattern_query_parsing_split.md)  
  Also review: **Rerankers** → [Open](../../rerankers.md)

- Webhook storms or duplicate executions  
  Pattern: **Bootstrap Deadlock** → [Open](../../patterns/pattern_bootstrap_deadlock.md)

---

## Minimal setup checklist for any Zap

1) **Warm-up fence before RAG or LLM steps**  
   Validate `VECTOR_READY == true`, `INDEX_HASH` matches, and secrets exist.  
   If not ready, short-circuit with a Delay and retry with capped backoff.  
   Spec: [Bootstrap Ordering](../../bootstrap-ordering.md)

2) **Idempotency and dedupe**  
   Compute `dedupe_key = sha256(source_id + revision + index_hash)`.  
   Use Zapier Storage by Zap or an external KV to drop duplicates.

3) **RAG boundary contract**  
   Require fields: `snippet_id`, `section_id`, `source_url`, `offsets`, `tokens`.  
   Enforce cite-then-explain. Forbid cross-section reuse.  
   Specs: [Data Contracts](../../data-contracts.md) · [Retrieval Traceability](../../retrieval-traceability.md)

4) **Observability probes**  
   Log ΔS(question, retrieved). Log λ per step: retrieve, assemble, reason.  
   Alert when ΔS ≥ 0.60 or λ flips divergent.  
   Overview: [RAG Architecture & Recovery](../../rag-architecture-and-recovery.md)

5) **Regression gate**  
   Require coverage ≥ 0.70 and ΔS ≤ 0.45 before publishing the Zap.  
   Eval: [RAG Precision/Recall](../../eval/eval_rag_precision_recall.md)

---

## Zapier recipe you can copy

> Replace the concrete tools with your stack. Keep the guardrails.

1. **Trigger**  
   Stable `source_id` and `revision`.

2. **Warm-up Check**  
   Code step pulls `INDEX_HASH`, `VECTOR_READY`, secrets.  
   If not ready, set `ready=false`.

3. **Path: Not ready**  
   Delay 30–90 seconds.  
   Re-run with a capped retry count.

4. **Path: Ready**  
   **Retrieval step**  
   - Call the retriever with explicit metric and consistent analyzer.  
   - Collect `snippet_id`, `section_id`, `source_url`, `offsets`, `tokens`.  
   **ΔS probe step**  
   - Compute ΔS(question, retrieved). If ΔS ≥ 0.60 set `needs_fix=true`.  
   **Reasoning step**  
   - LLM reads TXT OS and uses the WFGY schema. Enforce cite-then-explain.  
   **Trace sink**  
   - Store `question`, `snippet_id`, `ΔS`, `λ_state`, `INDEX_HASH`, `dedupe_key`.  
   **Idempotency guard**  
   - Before side effects, check KV for `dedupe_key`. If exists, skip.

---

## Copy-paste prompt for the LLM step

```

I uploaded TXT OS and the WFGY Problem Map pages.
My Zapier flow retrieved {k} snippets with fields {snippet\_id, section\_id, source\_url, offsets}.
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

## Common Zapier gotchas

- Formatter renames fields and breaks your data contract  
  Lock field names. Verify with a schema check step.

- Parallel paths write to the same index or KV without a fence  
  Use a single writer or a queue. Apply idempotency keys.

- HyDE prompt created inside Zap differs from the API client  
  Keep tokenizer and casing identical, or switch to reranking.  
  See: [Rerankers](../../rerankers.md)

---

## When to escalate

- ΔS stays ≥ 0.60 after chunk and retrieval fixes  
  Rebuild index with explicit metric and normalization.  
  See: [Retrieval Playbook](../../retrieval-playbook.md)

- Answers alternate across Zap runs with identical input  
  Investigate memory desync and version skew.  
  See: [Pre-Deploy Collapse](../../predeploy-collapse.md)

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

