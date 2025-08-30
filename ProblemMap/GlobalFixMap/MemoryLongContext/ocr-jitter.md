# OCR Jitter — Guardrails and Fix Pattern

When OCR engines process scanned text with inconsistent spacing, width variants, or mixed character forms,  
the output may look visually correct but introduces **false token differences** that destabilize retrieval and reasoning.

---

## Symptoms
- OCR transcript looks fine to the eye, but semantic retrieval drifts.  
- Words alternate between **half-width / full-width** forms.  
- Invisible characters (zero-width joiners, non-breaking spaces) trigger token mismatches.  
- Capitalization inconsistent across the same word in long transcripts.  
- Citations fail even though the snippet visually matches the source.

---

## Root causes
- OCR confidence below threshold but output still accepted.  
- Normalization skipped (NFC vs NFD forms mixed).  
- Scanner artifacts (speckles, warped lines) inject invisible characters.  
- Language-specific width forms (CJK fullwidth vs ASCII halfwidth) untreated.  
- No post-processing pass to unify tokens before embedding.

---

## Fix in 60 seconds
1. **Gate by confidence**
   - Drop lines with OCR confidence < 0.85.  
   - Flag low-confidence tables and equations for manual review.  

2. **Normalize Unicode**
   - Convert to **NFC** form.  
   - Replace non-breaking spaces with plain space.  
   - Strip zero-width characters.  

3. **Unify width and case**
   - Map fullwidth and halfwidth characters consistently.  
   - Apply case-folding for ASCII text.  

4. **Re-stamp clean snippets**
   - After normalization, reassign line numbers.  
   - Ensure `section_id | start_line | end_line | citation` schema updated.  

5. **Verify joins**
   - Run ΔS across adjacent chunks.  
   - If join ΔS ≥ 0.50, suspect hidden jitter — repeat normalization.  

---

## Copy-paste diagnostic prompt
```txt
You have TXTOS and the WFGY Problem Map.

Task: Detect and repair OCR jitter.

Protocol:
1. Normalize all snippets:
   - Unicode NFC
   - Strip zero-width, NBSP
   - Map fullwidth → halfwidth
   - Apply case-fold
2. Drop snippets with OCR confidence < 0.85.
3. Re-stamp Snippet Table with {section_id, start_line, end_line, citation}.
4. Measure ΔS across adjacent chunks:
   - Target ≤ 0.50 at each join.
5. Report ΔS(question, retrieved) and λ states.
````

---

## Acceptance targets

* OCR confidence ≥ 0.85 for all retained lines.
* No mixed width or hidden characters in final text.
* ΔS(question, retrieved) ≤ 0.45 and joins ≤ 0.50.
* λ remains convergent across three paraphrases.
* Snippets traceable and citations reproducible.

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
