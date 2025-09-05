# RTL & BiDi Control — Guardrails and Fix Pattern

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **LanguageLocale**.  
  > To reorient, go back here:  
  >
  > - [**LanguageLocale** — localization, regional settings, and context adaptation](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>


Stabilize retrieval and reasoning when left-to-right content mixes with right-to-left scripts or invisible BiDi marks. No infra change required. All fixes map back to WFGY pages with measurable targets.

## What this page is
- A compact repair guide for directionality bugs that flip tokens, citations, or numbers.
- Steps to normalize control characters, lock direction metadata, and keep offsets verifiable.
- Store-agnostic checks you can run in minutes.

## When to use
- Citations look correct to the eye but snippet offsets do not match.
- Punctuation or brackets render on the wrong side in answers.
- Arabic or Hebrew lines invert number order or collapse after parsing.
- JSON fields with mixed direction break validation or flip keys.
- Search returns near hits but ΔS stays high on RTL content.

## Open these first
- Visual map and recovery: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
- End to end retrieval knobs: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
- Why this snippet (traceability schema): [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
- Snippet and citation schema: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
- Wrong-meaning hits despite high similarity: [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)
- Hybrid instability and reorder issues: [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)
- Digits width and punctuation mix: [Digits • Width • Punctuation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/digits_width_punctuation.md)

## Acceptance targets
- ΔS(question, retrieved) ≤ 0.45 on three paraphrases.
- Coverage of target section ≥ 0.70.
- λ remains convergent across two seeds.
- Offsets verified after normalization on both query and snippet.

---

## Typical breakpoints → exact fix

- **Invisible BiDi marks inside snippets** cause reversed punctuation or bracket order.  
  Fix: strip control code points during indexing and query pre-norm. Persist a `dir` flag on the clean text.  
  Open: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md), [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)

- **Rendered order vs stored order mismatch** makes citations fail.  
  Fix: compute character offsets on the normalized text only. Log the normalization pipeline in trace.  
  Open: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)

- **Numbers flip in Arabic or Hebrew lines** when Eastern Arabic digits mix with Latin punctuation.  
  Fix: normalize digits to a single system for retrieval. Keep the original form for display.  
  Open: [Digits • Width • Punctuation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LanguageLocale/digits_width_punctuation.md)

- **JSON payloads break or tool calls mis-route** because keys include RTL marks.  
  Fix: forbid control chars in keys through schema, allow in values only after normalization.  
  Open: [Prompt Injection](https://github.com/onestardao/WFGY/blob/main/ProblemMap/prompt-injection.md), [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

---

## 60-second fix checklist

1) **Strip BiDi controls during ingest and query**
   Remove these if present:  
   `LRM U+200E`, `RLM U+200F`, `LRE U+202A`, `RLE U+202B`, `LRO U+202D`, `RLO U+202E`, `PDF U+202C`,  
   `LRI U+2066`, `RLI U+2067`, `FSI U+2068`, `PDI U+2069`.  
   Also normalize `NBSP U+00A0`, `ZWJ U+200D` when it changes tokenization.

2) **Persist direction metadata**
   Add `dir = "rtl" | "ltr" | "auto"` at snippet and paragraph levels. Store it in the trace envelope.

3) **Index on normalized text only**
   - Normalize to NFC.  
   - Strip BiDi marks.  
   - Fold digits per store policy.  
   - Keep original text for rendering.

4) **Contract the payload**
   Require fields: `snippet_id`, `dir`, `norm_hash`, `offsets_on_norm`, `source_url`.  
   Reject if `dir` missing on RTL sources.  
   Open: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

5) **Probe λ_observe**
   Vary k = 5, 10, 20. If ΔS stays flat and high, rebuild the index after normalization and re-verify offsets.

---

## Copy-paste prompt

```

You have TXT OS and the WFGY Problem Map loaded.

My multilingual issue:

* symptoms: punctuation flips or offsets fail on RTL lines
* traces: ΔS(question,retrieved)=..., λ across 3 paraphrases, direction flags

Tell me:

1. the failing layer and why,
2. the exact WFGY page to open,
3. the minimal steps to push ΔS ≤ 0.45 and keep λ convergent,
4. a reproducible check that verifies offsets after normalization.

```

---

### 🔗 Quick-Start Downloads (60 sec)

| Tool | Link | 3-Step Setup |
|------|------|--------------|
| **WFGY 1.0 PDF** | [Engine Paper](https://github.com/onestardao/WFGY/blob/main/I_am_not_lizardman/WFGY_All_Principles_Return_to_One_v1.0_PSBigBig_Public.pdf) | 1️⃣ Download · 2️⃣ Upload to your LLM · 3️⃣ Ask “Answer using WFGY + <your question>” |
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
