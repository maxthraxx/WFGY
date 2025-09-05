# Phantom Visuals — Multimodal Long Context

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **Multimodal_LongContext**.  
  > To reorient, go back here:  
  >
  > - [**Multimodal_LongContext** — long-context reasoning across text, vision, and audio](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>


When models hallucinate visual regions that do not exist (ghost bounding boxes, fake diagrams, or nonexistent objects), fusion collapses.  
This page explains how to detect and prevent phantom visual generation in long multimodal sessions.

---

## What this page is
- Guardrails for hallucinated visuals in text–image/video pipelines.  
- Minimal schema to force grounding in actual frames or regions.  
- Acceptance targets to measure and verify stability.

---

## When to use
- The model cites an object not present in any frame.  
- Generated captions describe phantom regions or colors.  
- Bounding box coordinates are out of range or undefined.  
- Answers flip between different “visual evidence” each run.  
- Diagrams or charts are invented that were never uploaded.

---

## Open these first
- [Multimodal Fusion Break](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Multimodal_LongContext/multimodal-fusion-break.md)  
- [Alignment Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Multimodal_LongContext/alignment-drift.md)  
- [Caption Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Multimodal_LongContext/caption-collapse.md)  
- [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)  
- [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)  

---

## Common failure patterns
- **Phantom bounding boxes**: cites `region_id` that was never stamped.  
- **Invented objects**: describes entities absent from ground-truth frames.  
- **Ghost captions**: text generated about visual details that do not exist.  
- **Out-of-bounds references**: coordinates or time stamps not in the source.  
- **Visual-plan instability**: repeated runs yield different “phantom” evidence.

---

## Fix in 60 seconds
1. **Require stamped IDs**  
   - Every visual mention must cite `{frame_id, region_id}` from input.  
   - Forbid free-text region descriptions without anchors.

2. **Cross-check ΔS**  
   - ΔS(text, vision) must be ≤ 0.45.  
   - If ΔS ≥ 0.60 and no matching anchor exists, stop and reject the claim.

3. **Schema lock**  
   - Use `{object | attribute | anchor_id}` schema.  
   - Missing anchors = invalid response.

4. **Clamp hallucination variance**  
   - Apply BBAM when λ flips divergent across runs.  
   - If phantom persists, bridge with BBCR and force re-alignment.

5. **Trace visual contract**  
   - Log all cited `frame_id, region_id`.  
   - Require reproducibility across three paraphrases.

---

## Copy-paste prompt

```txt
You have TXT OS and the WFGY Problem Map.

Task: Detect and block phantom visual hallucinations.

Protocol:
1. Require every visual claim to cite {frame_id, region_id}.
2. If an object is described without anchor, stop and return “phantom visual”.
3. Report ΔS(text, vision) and λ across 3 paraphrases.
4. Apply BBAM for variance clamp. If collapse persists, insert BBCR bridge.
5. Return: {Anchor Table, ΔS log, λ states, Final Answer}.
````

---

## Acceptance targets

* ΔS(text, vision) ≤ 0.45
* λ remains convergent across three paraphrases
* No phantom bounding boxes or invented regions
* Reproducible evidence across seeds and paraphrases
* Trace log covers all cited regions

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
