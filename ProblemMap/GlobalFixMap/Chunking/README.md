# Chunking — Global Fix Map
Find and fix the silent breaks at document boundaries.  
You use this when sections look fine but retrieved snippets cut mid idea, tables split, or anchors vanish.

## What this page is
- A quick route to correct chunk sizes, fences, and anchors.
- Structural rules to stop boundary drift without touching models.
- Checks you can measure and repeat.

## When to use
- Top-k looks plausible but citations point to the wrong half of a section.
- Tables or code blocks are split across chunks.
- Headers disappear or merge with the next paragraph.
- Long answers smear topics across two sources.
- Recall is high but precision is noisy around joins.

## Open these first
- Boundary checklist: [Chunking Checklist](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md)
- Hallucination at boundaries: [Hallucination](https://github.com/onestardao/WFGY/blob/main/ProblemMap/hallucination.md)
- Snippet schema and trace: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md) · [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
- Drift in long windows: [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md) · [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)

## Fix in 60 seconds
1) **Probe ΔS at joins**  
   - Compute ΔS across adjacent chunks A↔B for the same section title.  
   - Trigger: ΔS ≥ 0.50 at the join or ΔS spikes when you remove the header.
2) **Add λ_observe markers**  
   - Ask cite-then-explain. If cite fails and explain passes, boundary drift is the cause.
3) **Patch the structure**  
   - Keep headers and section ids inside each chunk.  
   - Do not split code fences, tables, math.  
   - Cap plain-text chunks by semantic units, not hard token length.  
   - Add `section_id`, `page_no`, `char_span` to every snippet.  
   - For very long sections store sub-section anchors.

## Copy-paste prompt
```

I uploaded TXT OS and the WFGY ProblemMap files.

My chunking bug:

* symptom: \[brief]
* traces: \[ΔS at several joins], \[examples of split tables or code], \[λ states]

Tell me:

1. which boundary rule is violated and why,
2. which fix pages to open in this repo,
3. minimal steps to push ΔS(join) ≤ 0.45 and keep λ convergent,
4. how to verify with a snippet ↔ citation table.
   Use BBMC for anchor alignment. If logic still flips, apply BBCR bridge.

```

## Minimal checklist
- One header per chunk. Keep the header text in the chunk body.  
- Never cut a table, code block, or list mid item.  
- Prefer sentence or paragraph aware splitters.  
- Store stable ids: `source_id`, `section_id`, `sub_id` if any.  
- Keep cross-refs like figure or table captions with the referenced block.  
- Add back-pressure: if a chunk would cut a fence, expand to include the full unit.

## Acceptance targets
- ΔS(question, retrieved) ≤ 0.45 on three paraphrases.  
- ΔS at adjacent joins ≤ 0.50.  
- Cite-then-answer passes consistently.  
- λ stays convergent when you reorder non-semantic headers.  
- Retrieval coverage to the target section ≥ 0.70.

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
