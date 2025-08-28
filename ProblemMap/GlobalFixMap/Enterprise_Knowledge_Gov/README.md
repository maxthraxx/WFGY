# Enterprise Knowledge Governance — Global Fix Map

A compact hub to make enterprise data safe and auditable across RAG, agents, and long-running workflows. Use this folder to define the policy layer and route symptoms to the exact repair page. No infra change required.

## When to use this folder
- You have mixed-sensitivity corpora and must stop accidental leakage.
- Regional data residency is a contract requirement.
- Stale SOPs or outdated policies keep showing up in answers.
- Legal retention vs. developer convenience creates drift.
- You need verifiable access trails and regulator-ready exports.

## Acceptance targets
- Zero unauthorized citation of PII or restricted snippets in production evals.
- Policy tags present on ≥ 0.95 of onboarded documents.
- Residency violations equal 0 across seven days of traffic.
- Retention SLA respected for 100 percent of expired items within 24 hours.
- All retrievals carry a trace record with `citations`, `ΔS`, `λ_state`, `policy_eval`.

## Quick routes to pages
- Access control and role fences  
  → [access_control.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Enterprise_Knowledge_Gov/access_control.md)
- Audit trail and trace schema  
  → [audit_and_traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Enterprise_Knowledge_Gov/audit_and_traceability.md)
- Compliance overview and controls  
  → [compliance.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Enterprise_Knowledge_Gov/compliance.md)
- Compliance audit checklist and exports  
  → [compliance_audit.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Enterprise_Knowledge_Gov/compliance_audit.md)
- Data residency and region pinning  
  → [data_residency.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Enterprise_Knowledge_Gov/data_residency.md)
- Data sensitivity model and redaction gates  
  → [data_sensitivity.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Enterprise_Knowledge_Gov/data_sensitivity.md)
- Knowledge expiry and policy freshness  
  → [knowledge_expiry.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Enterprise_Knowledge_Gov/knowledge_expiry.md)
- Retention policy and deletion jobs  
  → [retention_policy.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Enterprise_Knowledge_Gov/retention_policy.md)

## Map symptoms → structural fixes
- Wrong snippet shows up from a restricted area  
  → [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)  
  → Contract the payload with [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

- Prompt or tool step bypasses the policy and leaks PII  
  → [prompt-injection.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/prompt-injection.md)  
  → Lock tool schemas in [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

- Sensitive text survives parsing and chunking  
  → [chunking-checklist.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md)  
  → OCR and export checks in [ocr-parsing-checklist.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ocr-parsing-checklist.md)

- Live runs drift from policy or regions  
  → [ops/live_monitoring_rag.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md)  
  → [ops/debug_playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md)

## 60-second setup checklist
1) **Tag the corpus**  
   Attach `sensitivity`, `region`, `owner`, `retention_tier` to every doc. Enforce schema with [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md).

2) **Fence retrieval**  
   At retrieve time require the intersection of `{tenant_id, role, region, sensitivity}` and drop non-matching snippets. Verify with [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md).

3) **Pin residency**  
   Keep embeddings and shards in the source region. Block cross-region egress unless policy allows. See [data_residency.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Enterprise_Knowledge_Gov/data_residency.md).

4) **Retention jobs**  
   Create TTL queues per `retention_tier`. Write a deletion log with `doc_id`, `hash`, `time`, `actor`. See [retention_policy.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Enterprise_Knowledge_Gov/retention_policy.md).

5) **Audit everything**  
   Emit `actor`, `question`, `citations`, `ΔS`, `λ_state`, `policy_eval`, `region` for each answer. Route to an immutable sink. See [audit_and_traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Enterprise_Knowledge_Gov/audit_and_traceability.md).

## Copy-paste policy probe for your LLM step
```txt
You have TXTOS and the WFGY Problem Map loaded.

Question: "{user_question}"
Context carries fields {sensitivity, region, retention_tier, owner} for each snippet.

Do:
1) Enforce cite-then-explain. Refuse if a cited snippet breaks role or region.
2) Return {"citations":[...], "policy_eval":{"allow":true|false,"reason":"..."}, "ΔS":0.xx, "λ_state":"→|←|<>|×"}.
3) If blocked, give the minimal fix and the exact WFGY page to open.
````

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
