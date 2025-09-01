# Memory & Long-Context — Global Fix Map

Stabilize **long windows** and **multi-session memory**.  
This map helps you repair drift, collapse, forks, and ghost contexts when conversations or documents stretch far beyond the usual size.

---

## What this page is
- A **beginner-friendly checklist** for long contexts and multi-day sessions.
- **Copy-paste guardrails** that stop drift and collapse before they spread.
- **Concrete metrics** with ΔS and λ_observe so you know if your system is stable.

---

## When to use
- Dialog grows past **50k–100k tokens** and answers degrade.  
- Facts flip after **tab refresh** or **model switch**.  
- Citations look right but reasoning goes **flat or chaotic**.  
- OCR transcripts look fine but **capitalization or spacing drift**.  
- Multi-day support threads **lose task state** or **rewrite history**.  

---

## Orientation: quick routes

| Page | What it solves | Typical symptom |
|------|----------------|-----------------|
| [memory-coherence.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/MemoryLongContext/memory-coherence.md) | Memory fences & continuity | Threads repeat or contradict |
| [entropy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/MemoryLongContext/entropy-collapse.md) | Attention melt in long windows | Outputs drift into filler |
| [context-drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/MemoryLongContext/context-drift.md) | Long reasoning drift | Correct early, wrong later |
| [pattern_memory_desync.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/MemoryLongContext/pattern_memory_desync.md) | Cross-tab & cache hazards | State flips after refresh |
| [ghost-context.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/MemoryLongContext/ghost-context.md) | Stale buffers & residue | Model recalls “phantom” text |
| [state-fork.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/MemoryLongContext/state-fork.md) | Divergent memory forks | Same task_id, different answers |
| [ocr-parsing-checklist.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/MemoryLongContext/ocr-parsing-checklist.md), [ocr-jitter.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/MemoryLongContext/ocr-jitter.md) | OCR-specific noise | Exported text drifts vs. original |
| [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/MemoryLongContext/retrieval-traceability.md), [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/MemoryLongContext/data-contracts.md) | Traceability & audit | Citations break or vanish |
| [chunking-checklist.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/MemoryLongContext/chunking-checklist.md) | Chunk stability at joins | Mid-sentence cuts or overlaps |

---

## Acceptance targets
- Retrieval coverage **≥ 0.70** to the intended section  
- ΔS(question, retrieved) **≤ 0.45** and joins **≤ 0.50**  
- λ_observe remains **convergent** across 3 paraphrases  
- No state fork across tabs or agents for the same `task_id`  

---

## 60-second fix checklist

1. **Lock metrics** — same analyzer & embeddings across sessions.  
2. **Enforce memory fences** — require `task_id`, `session_id`, and `snippet_id`.  
3. **Probe ΔS and λ** — run 3 paraphrases × 2 seeds.  
4. **Patch drift** — realign chunks, re-check OCR, drop ghost spans.  
5. **Audit consistency** — run traceability logs and verify continuity across restarts.  

---

### 🔗 Quick-Start Downloads (60 sec)

| Tool | Link | 3-Step Setup |
|------|------|--------------|
| **WFGY 1.0 PDF** | [Engine Paper](https://github.com/onestardao/WFGY/blob/main/I_am_not_lizardman/WFGY_All_Principles_Return_to_One_v1.0_PSBigBig_Public.pdf) | 1️⃣ Download · 2️⃣ Upload · 3️⃣ Ask “Answer using WFGY + <your question>” |
| **TXT OS (plain-text OS)** | [TXTOS.txt](https://github.com/onestardao/WFGY/blob/main/OS/TXTOS.txt) | 1️⃣ Download · 2️⃣ Paste into any LLM chat · 3️⃣ Type “hello world” — OS boots instantly |

---

### 🧭 Explore More

| Module | Description | Link |
|--------|-------------|------|
| WFGY Core | WFGY 2.0 engine, full symbolic reasoning stack | [View →](https://github.com/onestardao/WFGY/tree/main/core/README.md) |
| Problem Map 1.0 | Initial 16-mode diagnostic framework | [View →](https://github.com/onestardao/WFGY/tree/main/ProblemMap/README.md) |
| Problem Map 2.0 | RAG failure tree and modular fixes | [View →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md) |
| Semantic Clinic | Expanded failure catalog | [View →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/SemanticClinicIndex.md) |
| Semantic Blueprint | Layer-based symbolic reasoning | [View →](https://github.com/onestardao/WFGY/tree/main/SemanticBlueprint/README.md) |
| Benchmark vs GPT-5 | Stress test GPT-5 with WFGY reasoning suite | [View →](https://github.com/onestardao/WFGY/tree/main/benchmarks/benchmark-vs-gpt5/README.md) |
| 🧙‍♂️ Starter Village 🏡 | New here? Lost in symbols? Click here for guided intro | [Start →](https://github.com/onestardao/WFGY/blob/main/StarterVillage/README.md) |

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
