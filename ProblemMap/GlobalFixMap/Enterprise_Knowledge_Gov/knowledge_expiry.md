# Knowledge Expiry — Enterprise Knowledge Governance

Guardrails and fix patterns to handle the **expiry, staleness, or invalidation** of enterprise knowledge inside AI pipelines. Use this page when retrieved data may be out of date, unmaintained, or legally required to expire.

---

## When to use this page
- RAG retrieves documents that are outdated but still present in the index.  
- Policies require document expiry (e.g., 3-year rotation, GDPR “right to be forgotten”).  
- Model cites knowledge that has been deprecated.  
- Knowledge base retains drafts or revoked versions.  

---

## Core acceptance targets
- Every document has an explicit `expiry_date` or `revision_hash`.  
- Retrieval never selects content beyond expiry.  
- Expired or revoked documents fully deleted from vector stores.  
- Audit logs record expiry enforcement at retrieval time.  

---

## Typical expiry problems → exact fix

| Symptom | Likely cause | Open this |
|---------|--------------|-----------|
| Outdated answers from old policies | No expiry metadata on ingestion | [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md) |
| Deprecated snippets retrieved | Index not refreshed after content change | [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md) |
| Conflicting answers (old vs new) | Stale embeddings and no version hashing | [context-drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md) |
| Expired docs still cited | Traceability schema missing `expiry_date` | [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) |

---

## Fix in 60 seconds
1. **Add expiry metadata** on ingestion:  
   ```json
   {
     "document_id": "policy-123",
     "revision_hash": "ab89e...",
     "expiry_date": "2026-01-01"
   }
````

2. **Drop expired docs** from index during nightly rebuilds.
3. **Enforce live expiry check** at retrieval:

   * Reject snippets where `expiry_date < today`.
   * Log `expired=true` in audit record.
4. **Verify ΔS stability** only against valid revisions.

---

## Copy-paste probe template

```txt
You have TXTOS and the WFGY Problem Map loaded.

My RAG system retrieved:
- doc_id, revision_hash, expiry_date

Task:
1. Drop all snippets past expiry_date.
2. Log ΔS(question,retrieved), λ_state, and expired flag.
3. If expired=true, cite the Problem Map page to rebuild the index.
Return JSON: { "valid_snippets": [...], "expired_snippets": [...], "ΔS": 0.xx, "λ_state": "<>", "next_fix": "..." }
```

---

## Escalate when

* Same query alternates between expired and valid docs.
* Expired documents remain in retrieval despite metadata.
* Audit logs show `expiry_date` ignored during reranking.

For deeper cases, apply [bootstrap-ordering.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md) to enforce correct load order and [ops/debug\_playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md) for runtime tracing.

---

### 🔗 Quick-Start Downloads

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


要我直接繼續生嗎？
