# Roles and Access (RBAC / ABAC) — Guardrails and Fix Pattern

This page defines **role-based access control (RBAC)** and **attribute-based access control (ABAC)** guardrails for AI pipelines.  
Without explicit access boundaries, LLMs may read from unintended sources, leak sensitive data, or bypass audit policy.

---

## When to use this page
- Your RAG or agent stack integrates multiple data stores with different sensitivity levels.  
- You cannot trace **who accessed what** across prompts, embeddings, or tool calls.  
- Evaluation runs fail because different users see different knowledge bases.  
- Compliance requires proof of **least privilege** but no policy schema exists.  

---

## Acceptance targets
- 100% of RAG data calls tagged with `role` or `attribute` context.  
- Coverage ≥ 0.95 of sensitive datasets behind access boundaries.  
- Audit trails record `who`, `what`, `when`, `ΔS`, `λ_state`.  
- Role drift probes show λ remains convergent across 3 paraphrases.  
- Exceptions logged with owner and expiry date.  

---

## Common failures → exact fixes

| Symptom | Likely cause | Open this |
|---------|--------------|-----------|
| Agents fetch data beyond allowed scope | missing RBAC fences | [policy_baseline.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Governance/policy_baseline.md) |
| Two users get different citations | inconsistent ABAC checks | [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) |
| Logs don’t show who triggered retrieval | no role injection | [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md) |
| Role drift causes schema injection | misplaced role attributes | [prompt-injection.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/prompt-injection.md) |
| Sensitive snippets leak in chains | missing attribute check | [pii_handling_and_minimization.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Governance/pii_handling_and_minimization.md) |

---

## Fix in 60 seconds

1. **Attach context**  
   Every retrieval call carries `{role, attribute_set, index_hash, ΔS, λ_state}`.  

2. **Enforce least privilege**  
   Roles map to dataset groups. Attributes refine down (e.g. geography, project).  

3. **Log every decision**  
   Audit trail logs query, ΔS, λ state, role, attributes, and snippet ids.  

4. **Probe role drift**  
   Run 3 paraphrases per role. If λ flips, enforce schema lock.  

---

## Minimal copy-paste checklist

- [ ] Define roles (admin, annotator, auditor, agent).  
- [ ] Define attributes (region, dataset sensitivity, project scope).  
- [ ] Attach `{role, attr}` to all tool and retrieval calls.  
- [ ] Enforce least privilege at ingestion and retrieval.  
- [ ] Log ΔS and λ_state by role.  
- [ ] Review and expire waivers.  

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


要我直接繼續幫你生出來嗎？
