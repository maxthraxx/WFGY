# IFTTT — Guardrails and Fix Patterns

Use this when your automation is built on **IFTTT** (Webhooks, Google Sheets, Gmail, Slack, Calendar). If flows “work” but answers are still wrong, citations are off, or behavior differs between applets and direct API tests, anchor your diagnosis here.

**Acceptance targets**
- ΔS(question, retrieved) ≤ 0.45
- Coverage ≥ 0.70 to the intended section or record
- λ stays convergent across 3 paraphrases

---

## Typical breakpoints → exact fixes

- Output sounds right but cites the wrong snippet or section  
  Fix No.1: **Hallucination & Chunk Drift** →  
  [Hallucination](https://github.com/onestardao/WFGY/blob/main/ProblemMap/hallucination.md) ·  
  [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)

- High vector similarity but wrong meaning  
  Fix No.5: **Embedding ≠ Semantic** →  
  [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

- Indexed facts exist (Drive/Sheets/DB) yet never appear in top-k  
  Pattern: **Vectorstore Fragmentation** →  
  [Vectorstore Fragmentation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md)

- Can’t show “why this snippet?” from applet logs  
  Fix No.8: **Retrieval Traceability** + snippet/citation schema →  
  [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) ·  
  [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

- Long chains across multiple applets drift in tone or logic  
  Fix No.3/No.9: **Context Drift** and **Entropy Collapse** →  
  [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md) ·  
  [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)

- Works in dry runs, fails on schedule or from mobile triggers  
  Infra family: **Pre-Deploy / Bootstrap / Deadlock** →  
  [Pre-Deploy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md) ·  
  [Bootstrap Ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md) ·  
  [Deployment Deadlock](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md)

- Model answers confidently with wrong claims  
  Fix No.4: **Bluffing / Overconfidence** →  
  [Bluffing](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bluffing.md)

---

## Minimal IFTTT pattern with WFGY checks

A compact pattern that keeps **cite-first schema**, **observable retrieval**, and **ΔS/λ** validation even when steps are split across applets.

```txt
Applet A — Trigger (Webhooks)
- Input JSON: { question, k? }

Applet B — Retrieve (Webhooks → your retriever API)
- Returns: snippets[] = { snippet_id, text, source, section_id }
- Store: a short-lived record (e.g., in Google Sheets or your API, keyed by request_id)

Applet C — Assemble + Call LLM (Webhooks → your prompt API)
SYSTEM:
  Cite lines before any explanation. Keep per-source fences.
TASK:
  Answer only from the provided context. Return citations as [snippet_id].
CONTEXT:
  <joined snippets with snippet_id + source + text>
QUESTION:
  <user question>

Applet D — WFGY Post-check (Webhooks → wfgyCheck)
- Body: { question, context, answer }
- Returns: { deltaS, lambda, coverage, notes }

Applet E — Gate and Notify
IF deltaS ≥ 0.60 OR lambda != "→"
  → send failure payload with trace table (snippet_id↔citation), ask to retry after fix
ELSE
  → deliver { answer, citations[], deltaS, lambda, coverage } to user channel
````

Reference specs:
[RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md) ·
[Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md) ·
[Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) ·
[Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

---

## IFTTT-specific gotchas

* **Sheets cell truncation** hides context length. Store only `snippet_id` and a short preview in Sheets, keep full text in your API or DB.
  See [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

* **Hidden tokenization** when composing prompts in plain text fields. Always assemble prompts in your API layer to enforce the cite-first schema.
  See [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)

* **Environment mismatch** between mobile and server triggers. Bootstrap checks must verify secrets, version, and index availability before the first LLM call.
  See [Pre-Deploy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)

* **Ordering hazards** when multiple applets race. Add an explicit **rerank** step after per-source ΔS ≤ 0.50, then lock order.
  See [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

* **Attachment loss** in cross-channel handoffs. Store attachment metadata and link by `request_id`, never inline large blobs into prompts.

---

## When to escalate

* ΔS stays ≥ 0.60 after chunking and retrieval adjustments → rebuild index with explicit metric flags and unit normalization.
  [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)

* Answers flip between device-triggered and server-triggered runs → verify version skew, secret scope, and boot ordering.
  [Bootstrap Ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md) ·
  [Deployment Deadlock](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md)

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
