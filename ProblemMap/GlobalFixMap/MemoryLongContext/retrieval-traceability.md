# Retrieval Traceability — Snippet Integrity & Audit Trail

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


Citations that look right can still hide silent drift.  
This guardrail defines how to enforce **traceability schemas** so that every claim links back to a stable, reproducible snippet.

---

## When to use
- Answers cite a source but the snippet cannot be located.  
- Two runs over the same corpus produce different citations.  
- A fact is quoted but not aligned to any section anchor.  
- Long-context threads degrade and snippets blur into paraphrase.  
- Multi-agent systems pass partial context and lose attribution.  

---

## Root causes
- **Orphan citations**: snippet ID missing or fabricated.  
- **Boundary drift**: citation spans cross section joins.  
- **Silent truncation**: tokens dropped at cut points.  
- **Cache overwrite**: citation schema lost after session reload.  
- **Free-text cites**: URLs or titles given without offsets.  

---

## Core acceptance targets
- Each claim must include `snippet_id`, `section_id`, `start_line`, `end_line`, `source_url`.  
- ΔS(question, retrieved) ≤ 0.45 overall.  
- Joins between snippets ≤ 0.50 ΔS.  
- λ convergent across 3 paraphrases.  
- Audit trail reproducible from log alone.  

---

## Structural fixes

- **Snippet table schema**  
  Require `{snippet_id | section_id | start_line | end_line | citation}`.  

- **Fence joins**  
  Split at section boundaries. Reject cross-section reuse.  

- **Trace log**  
  Store `{ΔS, λ_state, mem_rev, mem_hash}` per step.  

- **Contract lock**  
  Apply [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md) for payload validation.  

---

## Fix in 60 seconds
1. **Enforce snippet table** with unique IDs and line ranges.  
2. **Verify ΔS** across each join ≤ 0.50.  
3. **Echo λ states** at retrieval, assembly, reasoning.  
4. **Reject orphan claims** (no snippet_id).  
5. **Log trail** so same inputs → same citations.  

---

## Copy-paste prompt

```

You have TXT OS and the WFGY Problem Map.

Goal: Ensure every claim links to a reproducible snippet.

Protocol:

1. Build a Snippet Table {snippet\_id, section\_id, start\_line, end\_line, citation}.
2. Require cite-then-answer.
3. Forbid cross-section reuse.
4. If a claim has no snippet\_id, stop and request citation.
5. Report ΔS(question,retrieved), joins ΔS, and λ states.
6. Store {mem\_rev, mem\_hash, task\_id} for audit trail.
7. Answer only with snippets present in the table.

```

---

## Common failure signals
- Citations alternate across runs → missing trace schema.  
- URL without offsets → orphan citation.  
- Facts cited but no snippet_id → schema lock failed.  
- Session reload erases citations → ghost cache in memory.  

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

要直接開始 **data-contracts.md** 嗎？
