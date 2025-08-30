# Data Contracts — Enforcing Snippet Schema & Payload Integrity

RAG and long-context reasoning collapse quickly if payloads drift.  
**Data Contracts** define the minimal schema that every retrieval, citation, and reasoning step must satisfy to remain auditable and reproducible.

---

## When to use
- Citations appear but fields like `snippet_id` or `section_id` are missing.  
- JSON payloads change shape across runs.  
- Downstream agents receive free-text with no schema lock.  
- Long-context sessions silently lose attribution or overwrite fields.  
- Multi-agent handoffs mutate keys or flatten nested fields.  

---

## Root causes
- **Loose schemas**: free-form JSON without validation.  
- **Field drift**: different casing, missing offsets, or swapped names.  
- **Silent truncation**: long answers cut JSON blocks.  
- **Inconsistent contracts**: each component defines its own schema.  
- **Opaque citations**: only plain text without structured trace.  

---

## Core acceptance targets
- Every snippet payload must include:  
  `{snippet_id, section_id, start_line, end_line, source_url, offsets, tokens}`  
- Coverage ≥ 0.70 for the target section.  
- ΔS(question, retrieved) ≤ 0.45.  
- λ convergent across 3 paraphrases.  
- Contracts must validate under the same schema across sessions.  

---

## Structural fixes

- **Schema lock**  
  Define a JSON schema for citations and enforce validation at ingestion.  

- **Contract inheritance**  
  Pass the same schema downstream to every agent and reasoning step.  

- **Casing & normalization**  
  Enforce consistent field names and Unicode normalization.  

- **Fail fast**  
  If schema validation fails, block reasoning and return fix instructions.  

---

## Fix in 60 seconds
1. Define contract:  
   ```json
   {
     "snippet_id": "string",
     "section_id": "string",
     "start_line": "int",
     "end_line": "int",
     "source_url": "string",
     "offsets": [int],
     "tokens": [string]
   }
````

2. Validate every retrieval step against the contract.
3. Store the validated payload in the trace log.
4. Require cite-then-answer. Reject orphan claims.
5. Report ΔS and λ for each reasoning step.

---

## Copy-paste prompt

```
You have TXT OS and the WFGY Problem Map.

Task: enforce Data Contracts for retrieval and citation.

Protocol:
1. Validate that each snippet includes {snippet_id, section_id, start_line, end_line, source_url}.  
2. Reject orphans: if missing fields, stop and return fix tip.  
3. Require cite-then-answer.  
4. Log {ΔS(question,retrieved), λ_state, mem_rev, mem_hash}.  
5. Answer only with citations that pass contract validation.
```

---

## Common failure signals

* Citations alternate across runs → contract not enforced.
* JSON mode fails in provider → schema too loose.
* Free-text answers with no snippet\_id → orphan claims.
* Multi-agent pipelines mutate payloads → inconsistent contracts.

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
