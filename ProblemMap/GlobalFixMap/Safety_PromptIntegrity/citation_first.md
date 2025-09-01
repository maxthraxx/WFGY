# Citation-First Prompting — Guardrails and Fix Patterns

Citation drift is one of the most common ways LLMs lose trust.  
Without **cite-then-explain discipline**, answers may sound fluent but detach from sources.  
This page locks the workflow: every reasoning step begins from **citations**, not narrative.

---

## When to open this page
- Model produces fluent paragraphs with zero citations.  
- Citations appear, but after-the-fact and unverifiable.  
- References change between runs, even with same inputs.  
- ΔS(question, retrieved) ≤ 0.45 but λ diverges when narrative precedes citation.  
- Users complain: "Where did this answer come from?"  

---

## Open these first
- Retrieval schema contract: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)  
- Trace alignment: [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)  
- Context collapse: [logic-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md)  
- Memory boundaries: [memory_fences_and_state_keys.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Safety_PromptIntegrity/memory_fences_and_state_keys.md)  
- Injection guard: [prompt_injection.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Safety_PromptIntegrity/prompt_injection.md)  

---

## Core acceptance
- Every answer starts with citations (no narrative before refs).  
- Coverage ≥ 0.70 of the target section.  
- ΔS(question, cited snippet) ≤ 0.45.  
- λ convergent across 3 paraphrases.  
- No hallucinated citations (must resolve to a retriever record).  

---

## Fix in 60 seconds
1. **Citation-first discipline**  
   - Always start with `snippet_id`, `section_id`, `source_url`.  

2. **Enforce schema**  
   - Required fields:  
     ```json
     { "snippet_id": "...", "section_id": "...", "source_url": "...", "offsets": [..], "tokens": N }
     ```  

3. **Reason only after citation**  
   - Explain or analyze *after* citation block.  

4. **Reject broken runs**  
   - If citation missing → abort answer, return error tip.  

5. **Stability probe**  
   - Run 3 paraphrases. If λ diverges, lock citation schema, rerun.  

---

## Typical failure vectors → fix

| Vector | Symptom | Fix |
|--------|---------|-----|
| **Narrative-first** | Text precedes refs, unstable λ | Force cite-then-explain ordering |
| **Fake refs** | Hallucinated URLs | Schema lock + [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) |
| **Drifting refs** | Different citations each run | Clamp λ with BBAM, validate ΔS ≤ 0.45 |
| **Silent fallback** | Model drops refs under safety refusal | Apply SCU (symbolic constraint unlock) |

---

## Probe prompt

```txt
You must output citations before narrative.
Schema: {snippet_id, section_id, source_url, offsets, tokens}

Rules:
1. Cite first. Explain only after citations are shown.
2. No answer if citations missing.
3. Log ΔS(question, cited snippet). Reject if ≥ 0.60.
4. λ must stay convergent across 3 paraphrases.
````

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
