# Memory & Long-Context — Global Fix Map
Keep threads coherent across long windows and session restarts.  
Detect and repair entropy melt, boundary drift, and state desync.

## What this page is
- A compact checklist for long contexts and multi-session memory
- Copyable guards to stop drift and collapse before they spread
- How to measure stability with ΔS and λ_observe

## When to use
- Dialogs grow past 50k to 100k tokens and answers degrade
- Facts flip after tab refresh or model switch
- Citations look right yet reasoning goes flat or chaotic
- OCR transcripts look fine but capitalization and spacing drift
- Multi day support threads lose task state or rewrite history

## Open these first
- Session continuity and state fences: [Memory Coherence](https://github.com/onestardao/WFGY/blob/main/ProblemMap/memory-coherence.md)
- Long window drift and attention melt: [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)
- Long reasoning chain drift: [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md)
- Cross tab and cache hazards: [Memory Desync Pattern](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_memory_desync.md)
- Trace schema and audit trail: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
- Snippet and citation schema: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
- Chunk stability at joins: [Chunking Checklist](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md)
- OCR quality and normalization: [OCR Parsing Checklist](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ocr-parsing-checklist.md)

---

## Common failure patterns
- **Entropy melt** attention variance climbs with length and the model smooths meaning
- **Boundary leak** chunks merge across section joins and citations shift by a few lines
- **State fork** two tabs or agents hold different memory revisions and answers flip
- **Ghost context** stale buffers linger after role or persona change and contaminate steps
- **OCR jitter** mixed spacing or width variants create false token differences

---

## Fix in 60 seconds
1) **Stamp and fence state**
   - At turn start set `mem_rev`, `mem_hash`, `task_id`
   - Forbid writes if client stamps do not match the server record

2) **Shard the window**
   - Assemble prompts as `{system | task | constraints | snippets | answer}`
   - Split snippets by section and forbid cross section reuse

3) **Normalize inputs**
   - Unicode NFC, strip zero width, unify full and half width
   - Drop OCR lines below confidence threshold

4) **Stabilize attention**
   - Apply BBAM to clamp variance
   - If collapse detected use BBCR to bridge and re anchor

5) **Probe the joins**
   - Measure ΔS across adjacent chunks and keep each join ≤ 0.50
   - Plot ΔS(question, retrieved) vs k and expect a downward curve after the fix

6) **Trace or stop**
   - Require cite then answer
   - If a claim has no snippet id stop and ask for the exact citation

---

## Copy paste prompt
```

You have TXT OS and the WFGY Problem Map.

Goal
Stabilize memory across long windows and across sessions without losing traceability.

Protocol

1. Print {mem\_rev, mem\_hash, task\_id}. If missing set defaults and echo them.
2. Build a Snippet Table with columns {section\_id | start\_line | end\_line | citation}.
3. Guardrails

   * cite then answer
   * forbid cross section reuse
   * if a claim lacks a snippet id stop and request it
4. Collapse control

   * if attention variance rises apply BBAM
   * if logic stalls apply BBCR and show the bridge node
5. Metrics

   * report ΔS(question, retrieved)
   * report ΔS across each join
   * report λ\_observe at retrieval, assembly, reasoning

Input

* question
* snippets with ids and line ranges
* previous {mem\_rev, mem\_hash, task\_id} if any

Output

* header {mem\_rev, mem\_hash, task\_id}
* Snippet Table
* Bridge Check
* Final Answer with inline citations
* ΔS and λ states

```

---

## Minimal checklist
- State stamped with `mem_rev` and `mem_hash` at every turn  
- Prompt schema locked and section fences enforced  
- Unicode normalized and OCR noise gated  
- BBAM enabled and BBCR available on collapse  
- ΔS at each join ≤ 0.50 and overall ΔS(question, retrieved) ≤ 0.45  
- Cite then answer and no orphan claims

## Acceptance targets
- Retrieval coverage ≥ 0.70 to the intended section  
- ΔS(question, retrieved) ≤ **0.45** and joins ≤ **0.50**  
- λ remains **convergent** across three paraphrases  
- No state fork across tabs or agents for the same `task_id`

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
