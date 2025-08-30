# Memory & Long-Context — Global Fix Map

Keep threads coherent across long windows and session restarts.  
Detect and repair entropy melt, boundary drift, state forks, and ghost contexts.

---

## What this page is
- A compact checklist for long contexts and multi-session memory.
- Copyable guardrails to stop drift and collapse before they spread.
- Concrete measures with ΔS and λ_observe to verify stability.

---

## When to use
- Dialogs grow past 50k–100k tokens and answers degrade.  
- Facts flip after tab refresh or model switch.  
- Citations look right but reasoning goes flat or chaotic.  
- OCR transcripts look fine but capitalization and spacing drift.  
- Multi-day support threads lose task state or rewrite history.  

---

## Quick routes to per-page guides

- Memory fences and continuity  
  → [memory-coherence.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/MemoryLongContext/memory-coherence.md)

- Attention melt in long windows  
  → [entropy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/MemoryLongContext/entropy-collapse.md)

- Long reasoning drift  
  → [context-drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/MemoryLongContext/context-drift.md)

- Cross-tab and cache hazards  
  → [pattern_memory_desync.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/MemoryLongContext/pattern_memory_desync.md)

- Stale buffers and persona residue  
  → [ghost-context.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/MemoryLongContext/ghost-context.md)

- Divergent memory forks  
  → [state-fork.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/MemoryLongContext/state-fork.md)

- OCR-specific noise  
  → [ocr-parsing-checklist.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/MemoryLongContext/ocr-parsing-checklist.md), [ocr-jitter.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/MemoryLongContext/ocr-jitter.md)

- Traceability and audit trail  
  → [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/MemoryLongContext/retrieval-traceability.md), [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/MemoryLongContext/data-contracts.md)

- Chunk stability at joins  
  → [chunking-checklist.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/MemoryLongContext/chunking-checklist.md)

---

## Acceptance targets
- Retrieval coverage ≥ 0.70 to the intended section  
- ΔS(question, retrieved) ≤ **0.45** and joins ≤ **0.50**  
- λ remains **convergent** across three paraphrases  
- No state fork across tabs or agents for the same `task_id`  

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
