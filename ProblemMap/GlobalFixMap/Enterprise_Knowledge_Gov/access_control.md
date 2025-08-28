# Access Control — Enterprise Knowledge Governance

Guardrails and fix patterns to ensure that enterprise knowledge bases are segmented, secured, and retrievable without silent leaks. Use this page when failures look like “permissions bug” but root cause is schema drift, missing contracts, or evaluation blind spots.

---

## When to use this page
- Agents or LLMs retrieve snippets that a user role should not see.  
- Answers omit key passages even though data is present in the KB.  
- Knowledge base permissions collapse after re-index or migration.  
- Citation shows content from a restricted section without a trace.  
- External connectors expose more fields than expected.  

---

## Core acceptance targets
- ΔS(question, retrieved) ≤ 0.45, with access role enforced.  
- Coverage ≥ 0.70 for the allowed scope, and <0.05 for disallowed scope.  
- λ remains convergent across three paraphrases and two seeds.  
- All snippets carry explicit `role_scope`, `section_id`, and `source_hash`.  

---

## Typical access problems → exact fix

| Symptom | Likely cause | Open this |
|---------|--------------|-----------|
| Leaked restricted snippet | Missing role tag or weak contract | [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md), [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) |
| Role upgrade not reflected | Cache or index skew | [bootstrap-ordering.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md), [deployment-deadlock.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md) |
| Over-blocking (user sees nothing) | Schema mismatch or λ collapse | [logic-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md) |
| Citations missing access tag | Parser or contract drift | [ocr-parsing-checklist.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ocr-parsing-checklist.md), [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md) |

---

## Fix in 60 seconds
1. **Measure ΔS** for the retrieved vs allowed anchor.  
2. **Check role_scope** — ensure every snippet has an explicit scope.  
3. **Rebuild contract** — enforce schema: `{snippet_id, section_id, role_scope, hash}`.  
4. **Re-index** if role tags missing, with explicit normalization.  
5. **Verify λ stability** across paraphrases with access role locked.  

---

## Copy-paste schema (YAML)

```yaml
snippet_id: "KB-12345"
section_id: "SEC-42"
role_scope: "finance_analyst"
source_hash: "sha256:..."
text: "..."
````

Every snippet must carry these fields, and retrieval probes must validate them before citation.

---

## Escalate when

* ΔS remains ≥ 0.60 even with contracts enforced.
* Citations show cross-scope bleed.
* Index mismatch recurs after two re-indexes.

Escalation path: rebuild with [chunking-checklist.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md) and validate via [eval\_rag\_precision\_recall.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/eval/eval_rag_precision_recall.md).

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
