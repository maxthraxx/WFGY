# Chunking Checklist — Stability at Joins

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **MemoryLongContext**.  
  > To reorient, go back here:  
  >
  > - [**MemoryLongContext** — extended context windows and memory retention](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>


Long-context retrieval often fails not at the level of whole documents but at the **joins between chunks**.  
This checklist enforces stable, reproducible chunking so citations line up and entropy does not melt across boundaries.

---

## When to use
- Citations drift by a few lines between runs.  
- Long transcripts lose alignment after OCR or parsing.  
- Model answers cover the right fact but cite the wrong block.  
- ΔS spikes exactly at chunk joins.  
- Different agents disagree on chunk IDs.  

---

## Core acceptance targets
- Each join ΔS ≤ **0.50**.  
- Overall ΔS(question, retrieved) ≤ **0.45**.  
- Coverage ≥ **0.70** of intended section.  
- λ remains convergent across 3 paraphrases.  
- Each chunk has immutable `chunk_id`, `start_line`, `end_line`.  

---

## Checklist for stable chunking

- **Deterministic boundaries**  
  Split on semantic units (sections, paragraphs, headings). Never by raw token count alone.  

- **Overlap fence**  
  Add 10–15% overlap at joins. Enforce consistent overlap across every run.  

- **Immutable IDs**  
  Generate `chunk_id = sha256(doc_id + start_line + end_line)`. Store and reuse.  

- **Audit trail**  
  Store `{chunk_id, start_line, end_line, source_url, tokens}` for every chunk.  

- **Normalization**  
  Apply Unicode NFC, collapse whitespace, unify casing.  

- **Confidence gating**  
  Drop OCR or parsing lines with low confidence before chunking.  

---

## Fix in 60 seconds
1. Re-chunk corpus using semantic units.  
2. Apply overlap fence and store immutable chunk IDs.  
3. Run ΔS probes at joins. If ΔS > 0.50, re-check boundaries.  
4. Store all chunk metadata in trace logs.  
5. Require cite-then-answer. Reject any orphan chunk references.  

---

## Copy-paste prompt

```

You have TXT OS and the WFGY Problem Map.

Task: enforce stable chunking.

Protocol:

1. Verify each snippet has {chunk\_id, start\_line, end\_line, section\_id, source\_url}.
2. Reject orphans: if citation lacks chunk\_id, stop and request fix.
3. Require cite-then-answer.
4. Probe ΔS across joins, keep ≤ 0.50.
5. Report ΔS(question,retrieved), ΔS(joins), and λ state.

```

---

## Common failure signals
- Answers cite correct fact but wrong block → chunk IDs not stable.  
- ΔS spikes exactly at joins → overlap missing.  
- OCR transcripts break alignment → normalization skipped.  
- Multi-agent systems cite different chunk IDs → contract drift.  

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

