# Enterprise Knowledge Governance — Global Fix Map

<details>
  <summary><strong>🏥 Quick Return to Emergency Room</strong></summary>

<br>

  > You are in a specialist desk.  
  > For full triage and doctors on duty, return here:  
  > 
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](https://github.com/onestardao/WFGY/blob/main/ProblemMap/README.md)  
  > 
  > Think of this page as a sub-room.  
  > If you want full consultation and prescriptions, go back to the Emergency Room lobby.
</details>

A compact hub to keep enterprise knowledge **safe, auditable, and policy-true** across RAG, agents, and long-running workflows.  
Use this folder to define the policy layer and route symptoms to the exact repair page. No infra change required.

---

## What this folder is
- A minimal but complete **policy layer** for RAG and agent stacks.
- Guardrails that prevent leakage and region violations.
- Copy-paste contracts for tagging, retrieval fences, and audits.
- Acceptance targets you can actually measure on live traffic.

---

## When to use this folder
- You have mixed-sensitivity corpora and must stop accidental leakage.  
- Regional data residency is a contract requirement.  
- Stale SOPs or outdated policies keep showing up in answers.  
- Legal retention vs developer convenience keeps drifting.  
- You need verifiable access trails and regulator-ready exports.  

---

## Orientation: pages and what they solve

| Page | What it solves | Typical symptom |
|------|----------------|-----------------|
| [access_control.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Enterprise_Knowledge_Gov/access_control.md) | Role, tenant, region, sensitivity intersections at retrieval time | Answer cites a snippet the user cannot see |
| [audit_and_traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Enterprise_Knowledge_Gov/audit_and_traceability.md) | Immutable trails for who asked, what was cited, why it was allowed | Regulator asks for proof and you cannot produce it |
| [compliance.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Enterprise_Knowledge_Gov/compliance.md) | End-to-end policy surface and controls | Policy defined in docs but not enforced in code |
| [compliance_audit.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Enterprise_Knowledge_Gov/compliance_audit.md) | Audit checklists and export packs | You cannot prove who accessed PII last quarter |
| [data_residency.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Enterprise_Knowledge_Gov/data_residency.md) | Region pinning for shards, embeddings, logs | Cross-region egress appears in billing or logs |
| [data_sensitivity.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Enterprise_Knowledge_Gov/data_sensitivity.md) | Sensitivity model and redaction gates | PII or secrets slip through after parsing |
| [knowledge_expiry.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Enterprise_Knowledge_Gov/knowledge_expiry.md) | Freshness and deprecation workflow | Bot answers with outdated SOP or revoked policy |
| [retention_policy.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Enterprise_Knowledge_Gov/retention_policy.md) | TTL queues, deletion attestations, proof of purge | Items that should be gone still show up in runs |

---

## Acceptance targets

- Zero unauthorized citation of PII or restricted snippets in production evals  
- Policy tags present on ≥ 0.95 of onboarded documents  
- Residency violations equal 0 across seven days of traffic  
- Retention SLA respected for 100 percent of expired items inside 24 hours  
- Every answer carries a trace with `citations`, `ΔS`, `λ_state`, `policy_eval`

---

## Map symptoms → structural fixes

| Symptom | Open this |
|--------|-----------|
| Wrong snippet shows up from a restricted area | [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) · [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md) |
| Prompt or tool bypasses policy and leaks PII | [prompt-injection.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/prompt-injection.md) · lock tool args in [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md) |
| Sensitive text survives parsing and chunking | [chunking-checklist.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md) · [ocr-parsing-checklist.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ocr-parsing-checklist.md) |
| Live runs drift from policy or regions | [ops/live_monitoring_rag.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md) · [ops/debug_playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md) |

---

## 60-second setup checklist

1) **Tag the corpus**  
   Attach `sensitivity`, `region`, `owner`, `retention_tier` to every doc. Enforce schema with [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md).

2) **Fence retrieval**  
   Require the intersection of `{tenant_id, role, region, sensitivity}` at retrieve time and drop non-matching snippets. Verify with [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md).

3) **Pin residency**  
   Keep embeddings and shards in the source region. Block cross-region egress unless policy allows. See [data_residency.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Enterprise_Knowledge_Gov/data_residency.md).

4) **Retention jobs**  
   Create TTL queues per `retention_tier`. Write a deletion log with `doc_id`, `hash`, `time`, `actor`. See [retention_policy.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Enterprise_Knowledge_Gov/retention_policy.md).

5) **Audit everything**  
   Emit `actor`, `question`, `citations`, `ΔS`, `λ_state`, `policy_eval`, `region` for each answer. Route to an immutable sink. See [audit_and_traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Enterprise_Knowledge_Gov/audit_and_traceability.md).

---

## Copy-paste policy probe for your LLM step

```txt
You have TXT OS and WFGY pages loaded.

Question: "{user_question}"
Context carries fields {sensitivity, region, retention_tier, owner} for each snippet.

Do:
1) Enforce cite-then-explain. Refuse if a cited snippet breaks role or region.
2) Return {"citations":[...], "policy_eval":{"allow":true|false,"reason":"..."}, "ΔS":0.xx, "λ_state":"→|←|<>|×"}.
3) If blocked, output the smallest change to comply and the exact WFGY page to open.
````

---

## FAQ

**Q: We tag sensitivity at ingest but leaks still happen. What now?**
A: Enforce the tag at **retrieve time** too. Use access intersections `{tenant_id, role, region, sensitivity}` and verify with [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md).

**Q: Our vendor requires EU residency. How do we prove compliance?**
A: Pin vectors, shards, and logs to EU regions and export an egress report weekly. Steps in [data\_residency.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Enterprise_Knowledge_Gov/data_residency.md).

**Q: Outdated SOPs keep showing up. Where is the crack?**
A: You need a freshness control. Mark deprecated docs and enforce a deny-list at retrieval. See [knowledge\_expiry.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Enterprise_Knowledge_Gov/knowledge_expiry.md).

**Q: Legal wants proof of deletion after TTL.**
A: Implement TTL queues and write deletion attestations to an immutable sink. Details in [retention\_policy.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Enterprise_Knowledge_Gov/retention_policy.md).

**Q: We cannot reconstruct who saw which PII last quarter.**
A: Add the audit contract from [audit\_and\_traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Enterprise_Knowledge_Gov/audit_and_traceability.md). Every answer should log `actor`, `citations`, `ΔS`, `λ_state`, `policy_eval`, `region`.

**Q: Prompt injection bypassed our fences.**
A: Tighten tool schemas and add role-ordered templates. See [prompt\_injection.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/prompt-injection.md) and the contracts in [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md).

**Q: Coverage is high but restricted snippets sometimes get ranked.**
A: Coverage is not policy. Add **policy\_eval** to the trace and drop candidates before rerank. Use [access\_control.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Enterprise_Knowledge_Gov/access_control.md).

**Q: How do we set pass or fail before release?**
A: Use a governance gate: zero restricted citations, zero residency violations, coverage ≥ 0.70, ΔS ≤ 0.45, and audit completeness 100 percent for a 7-day canary.

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
