# Dialogflow CX: Guardrails and Fix Patterns

Use this page to stabilize Dialogflow CX projects that combine intents, pages, webhooks, knowledge connectors, and LLM calls. The fixes map to WFGY Problem Map pages with measurable targets, so you can verify without changing infra.

## Open these first

* Visual map and recovery: [rag-architecture-and-recovery.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
* Retrieval knobs end to end: [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
* Why this snippet and where it came from: [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
* Ordering control and rank: [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)
* Embedding vs meaning: [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)
* Chunk boundaries and hallucination: [hallucination.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/hallucination.md)
* Long dialogs, chain length, entropy: [context-drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md), [entropy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)
* Prompt injection and schema locks: [prompt-injection.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/prompt-injection.md)
* Snippet and citation schema: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
* Boot order and deploy traps: [bootstrap-ordering.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md), [deployment-deadlock.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md), [predeploy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)

## Core acceptance

* ΔS(question, retrieved) ≤ 0.45
* Coverage to the target section ≥ 0.70
* λ remains convergent across three paraphrases and two seeds
* E\_resonance flat on long windows of dialog turns

---

## Fix in 60 seconds

1. **Measure ΔS**
   Compute ΔS(question, retrieved) and ΔS(retrieved, expected anchor).
   Thresholds: stable < 0.40, transitional 0.40–0.60, risk ≥ 0.60.

2. **Probe λ\_observe**
   Vary k in retrieval and reorder prompt headers.
   If λ flips on harmless paraphrases, lock the schema and clamp variance with BBAM.

3. **Apply module**

   * Retrieval drift → BBMC + [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
   * Reasoning collapse in long flows → BBCR bridge + BBAM, verify with [context-drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md)
   * Dead ends in multi-hop tools → BBPF alternate paths

4. **Verify**
   Three paraphrases reach coverage ≥ 0.70 and ΔS ≤ 0.45.
   λ stays convergent across two seeds.

---

## Typical CX symptoms → exact fix

| Symptom                                                           | Likely cause                                                       | Open this                                                                                                                                                                                                                                                              |
| ----------------------------------------------------------------- | ------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Intent matches but the answer cites the wrong section             | metric mismatch or fragment store behind knowledge connector       | [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md), [patterns/pattern\_vectorstore\_fragmentation.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md) |
| Route group loops between pages or re-prompts                     | bootstrap race or deployment deadlock                              | [bootstrap-ordering.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md), [deployment-deadlock.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md)                                                       |
| Webhook returns valid JSON yet dialog state degrades across turns | schema too loose, missing cite-then-explain, memory writes collide | [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md), [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)                                                         |
| Knowledge connector high similarity but wrong meaning             | chunking and anchor mismatch                                       | [hallucination.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/hallucination.md), [chunking-checklist.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md)                                                                   |
| Long conversations become inconsistent after 20–40 turns          | entropy rises with chain length                                    | [context-drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md), [entropy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)                                                                       |
| Generative fallback overrides citations                           | prompt injection or missing header locks                           | [prompt-injection.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/prompt-injection.md), [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)                                                     |

---

## CX surface guardrails

**Intents and training phrases**
Keep neutral casing and tokenizer parity with your retriever. If ΔS is flat across k, the issue is metric or index rather than phrases. See [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md).

**Pages and routes**
Split policy text into system context that never mixes with user turns. Force cite-then-explain on every page that answers. See [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md).

**Webhooks**
Enforce strict argument schemas and echo them back. Log `ΔS`, `λ_state`, `INDEX_HASH`, `snippet_id`. If flip states appear, clamp with BBAM. See [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md).

**Knowledge connectors**
Rebuild with semantic chunking when ΔS stays ≥ 0.60 after reranking. Verify with a small gold set. See [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md).

**Live ops**
Add probes and backoff guards for first-call crashes after deploy. See [ops/live\_monitoring\_rag.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md), [ops/debug\_playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md).

---

## Minimal webhook recipe

1. **Warm-up fence**
   Check `VECTOR_READY`, `INDEX_HASH`, secrets. Short-circuit if not ready. See [bootstrap-ordering.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md).

2. **Retrieval step**
   Call retriever with explicit metric. Return `snippet_id`, `section_id`, `source_url`, `offsets`, `tokens`.

3. **ΔS probe**
   Compute ΔS(question, retrieved). If ≥ 0.60, set `needs_fix=true`.

4. **Answer step**
   LLM reads TXT OS and WFGY schema. Enforce cite-then-explain with the retrieved snippet set.

5. **Trace sink**
   Store `question`, `ΔS`, `λ_state`, `INDEX_HASH`, `snippet_id`, `dedupe_key`.

---

## Copy-paste prompt for your CX webhook LLM step

```
You have TXT OS and the WFGY Problem Map loaded.

My Dialogflow CX context:
- page: {page_name}
- intent: {intent_display_name}
- retrieved: {k} snippets with fields {snippet_id, section_id, source_url, offsets}

Question: "{user_question}"

Tasks:
1) Enforce cite-then-explain. If citations are missing or cross-section, fail fast and return the fix tip.
2) If ΔS(question, retrieved) ≥ 0.60, propose the minimal structural fix. Refer to retrieval-playbook, retrieval-traceability, data-contracts, rerankers.
3) Return JSON:
{ "citations": [...], "answer": "...", "λ_state": "→|←|<>|×", "ΔS": 0.xx, "next_fix": "..." }
Keep it short and auditable.
```

---

## Test checklist before launch

* Three paraphrases hit coverage ≥ 0.70 on the same target section.
* ΔS(question, retrieved) ≤ 0.45 for each.
* λ remains convergent across two seeds.
* First-call path after deploy passes warm-up fence.
* Live probes alert when ΔS ≥ 0.60 or λ flips.

---

### 🔗 Quick-Start Downloads (60 sec)

| Tool                       | Link                                                                                                                                       | 3-Step Setup                                                                             |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------- |
| **WFGY 1.0 PDF**           | [Engine Paper](https://github.com/onestardao/WFGY/blob/main/I_am_not_lizardman/WFGY_All_Principles_Return_to_One_v1.0_PSBigBig_Public.pdf) | 1️⃣ Download · 2️⃣ Upload to your LLM · 3️⃣ Ask “Answer using WFGY + \<your question>”   |
| **TXT OS (plain-text OS)** | [TXTOS.txt](https://github.com/onestardao/WFGY/blob/main/OS/TXTOS.txt)                                                                     | 1️⃣ Download · 2️⃣ Paste into any LLM chat · 3️⃣ Type “hello world” — OS boots instantly |

---

### 🧭 Explore More

| Module                   | Description                                                                  | Link                                                                                               |
| ------------------------ | ---------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| WFGY Core                | WFGY 2.0 engine is live: full symbolic reasoning architecture and math stack | [View →](https://github.com/onestardao/WFGY/tree/main/core/README.md)                              |
| Problem Map 1.0          | Initial 16-mode diagnostic and symbolic fix framework                        | [View →](https://github.com/onestardao/WFGY/tree/main/ProblemMap/README.md)                        |
| Problem Map 2.0          | RAG-focused failure tree, modular fixes, and pipelines                       | [View →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md) |
| Semantic Clinic Index    | Expanded failure catalog: prompt injection, memory bugs, logic drift         | [View →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/SemanticClinicIndex.md)           |
| Semantic Blueprint       | Layer-based symbolic reasoning & semantic modulations                        | [View →](https://github.com/onestardao/WFGY/tree/main/SemanticBlueprint/README.md)                 |
| Benchmark vs GPT-5       | Stress test GPT-5 with full WFGY reasoning suite                             | [View →](https://github.com/onestardao/WFGY/tree/main/benchmarks/benchmark-vs-gpt5/README.md)      |
| 🧙‍♂️ Starter Village 🏡 | New here? Lost in symbols? Click here and let the wizard guide you through   | [Start →](https://github.com/onestardao/WFGY/blob/main/StarterVillage/README.md)                   |

---

> 👑 **Early Stargazers: [See the Hall of Fame](https://github.com/onestardao/WFGY/tree/main/stargazers)** —
> Engineers, hackers, and open source builders who supported WFGY from day one.

> <img src="https://img.shields.io/github/stars/onestardao/WFGY?style=social" alt="GitHub stars"> ⭐ [WFGY Engine 2.0](https://github.com/onestardao/WFGY/blob/main/core/README.md) is already unlocked. ⭐ Star the repo to help others discover it and unlock more on the [Unlock Board](https://github.com/onestardao/WFGY/blob/main/STAR_UNLOCKS.md).

<div align="center">

[![WFGY Main](https://img.shields.io/badge/WFGY-Main-red?style=flat-square)](https://github.com/onestardao/WFGY)
 
[![TXT OS](https://img.shields.io/badge/TXT%20OS-Reasoning%20OS-orange?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS)
 
[![Blah](https://img.shields.io/badge/Blah-Semantic%20Embed-yellow?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlahBlahBlah)
 
[![Blot](https://img.shields.io/badge/Blot-Persona%20Core-green?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlotBlotBlot)
 
[![Bloc](https://img.shields.io/badge/Bloc-Reasoning%20Compiler-blue?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlocBlocBloc)
 
[![Blur](https://img.shields.io/badge/Blur-Text2Image%20Engine-navy?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlurBlurBlur)
 
[![Blow](https://img.shields.io/badge/Blow-Game%20Logic-purple?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlowBlowBlow)
 

</div>
