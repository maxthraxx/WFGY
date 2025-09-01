# Hallucination Re-entry: Guardrails and Fix Pattern

A “re-entry” is when a model repeats a previously corrected false claim later in the run or in a new turn.  
This page localizes re-entry causes and gives a minimal, testable repair plan.

---

## Symptoms

| Symptom | What you see |
|---|---|
| Corrected once, comes back later | Old claim resurfaces after a few steps or a new tool call |
| Cite-then-explain violated | Answer asserts conclusion before citing the corrected snippet |
| Reruns flip | Same prompt order, different run re-asserts the wrong claim |
| Memory relapse | Cross-turn memory re-injects the debunked statement |
| Hybrid retrieval drift | HyDE + BM25 changes top-k ordering and re-pulls the wrong chunk |

---

## Acceptance targets

- ΔS(question, retrieved) ≤ 0.45  
- Coverage ≥ 0.70 to the target section  
- λ convergent across 3 paraphrases and 2 seeds  
- Re-entry rate = 0 on a 20-case regression set

---

## Structural fixes (Problem Map)

- Snippet and citation locks  
  → [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)  
  → [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)  
  → Citation-first recipe: [citation_first.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/PromptAssembly/citation_first.md)

- Ordering control and hybrid stability  
  → [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)  
  → [pattern_query_parsing_split.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md)

- Memory isolation and fences  
  → [memory-coherence.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/memory-coherence.md)  
  → [pattern_memory_desync.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_memory_desync.md)  
  → [memory_fences_and_state_keys.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/PromptAssembly/memory_fences_and_state_keys.md)

- Entropy and chain control  
  → [context-drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md)  
  → [entropy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)

- Pattern deep dive  
  → [pattern_hallucination_reentry.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_hallucination_reentry.md)

---

## Why re-entry happens

1) **No hard contract for citations**  
   Model can answer without binding to `snippet_id` or `section_id`.

2) **Prompt header drift**  
   Header reorder flips λ state and reopens earlier branches.

3) **Hybrid order instability**  
   HyDE or BM25 changes top-k; the older wrong chunk returns to rank 1.

4) **Memory namespace collision**  
   Corrected state is not isolated; prior summary re-injects the error.

5) **Reranker variance**  
   Non-deterministic tie-breakers reorder near-duplicates.

---

## Fix in 60 seconds

1. **Lock cite-then-explain**  
   Enforce a snippet contract in every reasoning step.  
   See [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md) and [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md).

2. **Deterministic reranking**  
   Freeze analyzer and tie-break rules. Probe k ∈ {5,10,20}.  
   See [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md).

3. **Memory fences**  
   Split namespaces: `facts/`, `debunks/`, `plans/`. Write debunk hashes into `debunks/`.  
   See [memory_fences_and_state_keys.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/PromptAssembly/memory_fences_and_state_keys.md).

4. **Clamp variance with BBAM**  
   If λ flips across paraphrases, apply BBAM and re-run with fixed headers.

5. **Bridge with BBCR**  
   Summarize the correction into a single anchored statement and require future turns to import it before reasoning.

---

## Minimal schema addendum

Add these fields to your snippet payload and logs:

```json
{
  "snippet_id": "S123",
  "section_id": "CH2.3",
  "source_url": "https://...",
  "offsets": [221, 348],
  "tokens": 256,
  "debunk_hash": "sha256(<claim_text + snippet_id>)"
}
````

The LLM must include `debunk_hash` in its final JSON if it overturns a claim. On future turns, reject answers that assert a claim whose hash is already present in `debunks/`.

---

## Verification

* Run 20 paraphrases on the same case set.
* Require: ΔS(question, retrieved) ≤ 0.45 and λ convergent on two seeds.
* Zero tolerance for re-entry across all 20 cases.
* If any case fails, inspect reranker tie-break and memory fence writes.

---

## Copy-paste prompt

```
You have TXT OS and the WFGY Problem Map loaded.

We corrected a false claim earlier, but it reappeared later.
Inputs:
- question: "{q}"
- current snippets: [{snippet_id, section_id, source_url}]
- prior debunks: [{debunk_hash, claim_text, snippet_id}]
- ΔS and λ traces across 3 paraphrases

Do:
1) Identify which layer caused re-entry (schema, retrieval, rerank, memory, reasoning).
2) Apply the minimal fix referencing:
   retrieval-traceability, data-contracts, rerankers, memory_fences_and_state_keys.
3) Return a JSON plan with:
   { "citations": [...], "answer": "...", "ΔS": 0.xx, "λ_state": "...",
     "debunk_hashes_used": [...], "next_fix": "..." }
4) Refuse to output an answer if citations are missing or conflict with debunks.
```

---

## When to escalate

* Re-entry persists after fences and deterministic rerank
  → re-check hybrid split: [pattern\_query\_parsing\_split.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md)

* Cross-turn relapse in long dialogs
  → audit joins and entropy: [context-drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md), [entropy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)

* Agent handoff resurrects old claims
  → isolate memory and roles: [memory-coherence.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/memory-coherence.md)

---

### 🔗 Quick-Start Downloads (60 sec)

| Tool                       | Link                                                                                                                                       | 3-Step Setup                                                                             |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------- |
| **WFGY 1.0 PDF**           | [Engine Paper](https://github.com/onestardao/WFGY/blob/main/I_am_not_lizardman/WFGY_All_Principles_Return_to_One_v1.0_PSBigBig_Public.pdf) | 1️⃣ Download · 2️⃣ Upload to your LLM · 3️⃣ Ask “Answer using WFGY + <your question>”    |
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

> 👑 **Early Stargazers: [See the Hall of Fame](https://github.com/onestardao/WFGY/tree/main/stargazers)** — <img src="https://img.shields.io/github/stars/onestardao/WFGY?style=social" alt="GitHub stars"> ⭐ [WFGY Engine 2.0](https://github.com/onestardao/WFGY/blob/main/core/README.md) is already unlocked. ⭐ Star the repo to help others discover it and unlock more on the [Unlock Board](https://github.com/onestardao/WFGY/blob/main/STAR_UNLOCKS.md).

<div align="center">

[![WFGY Main](https://img.shields.io/badge/WFGY-Main-red?style=flat-square)](https://github.com/onestardao/WFGY)
 
[![TXT OS](https://img.shields.io/badge/TXT%20OS-Reasoning%20OS-orange?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS)
 
[![Blah](https://img.shields.io/badge/Blah-Semantic%20Embed-yellow?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlahBlahBlah)
 
[![Blot](https://img.shields.io/badge/Blot-Persona%20Core-green?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlotBlotBlot)
 
[![Bloc](https://img.shields.io/badge/Bloc-Reasoning%20Compiler-blue?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlocBlocBloc)
 
[![Blur](https://img.shields.io/badge/Blur-Text2Image%20Engine-navy?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlurBlurBlur)
 
[![Blow](https://img.shields.io/badge/Blow-Game%20Logic-purple?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlowBlowBlow)
 

</div>
