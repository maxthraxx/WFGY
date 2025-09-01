# Governance — Global Fix Map

A hub for governance controls around AI pipelines.  
Use this folder when failures are not infra or retrieval bugs, but breakdowns in policy, approvals, lineage, or compliance.  
Every page links to a structural WFGY fix and carries measurable acceptance targets so you can verify governance gates quickly.

---

## When to use this folder

- Policies exist but are unclear, obsolete, or unenforced
- Prompts or models change without sign-off and audit trail
- Data provenance is lost between documents, chunks, embeddings, and answers
- PII handling, minimization, or redaction cannot be proven
- License or usage rights are ambiguous for datasets or generated outputs
- Incident response or postmortems are missing or not actionable

---

## Acceptance targets

- Policy coverage ≥ 0.95 across datasets, prompts, models, eval
- ΔS(question, retrieved) ≤ 0.45 for governed outputs
- Coverage of the target section ≥ 0.70 with cite-then-explain
- λ remains convergent across 3 paraphrases and 2 seeds
- Every waiver has owner, expiry, and review link
- Immutable audit logs are joinable to lineage and approvals

---

## Quick index — per governance page

| Area | Page |
|---|---|
| Policy baseline | [policy_baseline.md](./policy_baseline.md) |
| Roles and access (RBAC and ABAC) | [roles_and_access_rbac_abac.md](./roles_and_access_rbac_abac.md) |
| Data lineage and provenance | [data_lineage_and_provenance.md](./data_lineage_and_provenance.md) |
| PII handling and minimization | [pii_handling_and_minimization.md](./pii_handling_and_minimization.md) |
| License and dataset rights | [license_and_dataset_rights.md](./license_and_dataset_rights.md) |
| Prompt policy and change control | [prompt_policy_and_change_control.md](./prompt_policy_and_change_control.md) |
| Model governance, model cards, releases | [model_governance_model_cards_and_releases.md](./model_governance_model_cards_and_releases.md) |
| Eval governance, gates and sign-off | [eval_governance_gates_and_signoff.md](./eval_governance_gates_and_signoff.md) |
| Audit and logging | [audit_and_logging.md](./audit_and_logging.md) |
| Audit logs and traceability | [audit_logs_and_traceability.md](./audit_logs_and_traceability.md) |
| Escalation and governance | [escalation_and_governance.md](./escalation_and_governance.md) |
| Ethics and bias mitigation | [ethics_and_bias_mitigation.md](./ethics_and_bias_mitigation.md) |
| Regulatory alignment | [regulatory_alignment.md](./regulatory_alignment.md) |
| Transparency and explainability | [transparency_and_explainability.md](./transparency_and_explainability.md) |
| Incident response and postmortems | [incident_response_and_postmortems.md](./incident_response_and_postmortems.md) |
| Risk register and waivers | [risk_register_and_waivers.md](./risk_register_and_waivers.md) |

---

## Map symptoms to structural fixes

| Symptom | Likely cause | Open this |
|---|---|---|
| Prompts or models change silently | No change control, missing approvals | [prompt_policy_and_change_control.md](./prompt_policy_and_change_control.md) · [eval_governance_gates_and_signoff.md](./eval_governance_gates_and_signoff.md) |
| PII appears in answers or logs | Weak minimization, missing redaction gates | [pii_handling_and_minimization.md](./pii_handling_and_minimization.md) · [audit_and_logging.md](./audit_and_logging.md) |
| Cannot show why a citation was selected | Missing trace schema or lineage joins | [audit_logs_and_traceability.md](./audit_logs_and_traceability.md) · [data_lineage_and_provenance.md](./data_lineage_and_provenance.md) |
| Disputes about dataset or output rights | Missing license registry or usage constraints | [license_and_dataset_rights.md](./license_and_dataset_rights.md) |
| Bias complaints or ethical risk | No bias probes, weak mitigation playbooks | [ethics_and_bias_mitigation.md](./ethics_and_bias_mitigation.md) |
| Regulatory questions block a release | No mapping from policy to artifacts | [regulatory_alignment.md](./regulatory_alignment.md) · [policy_baseline.md](./policy_baseline.md) |
| Incidents repeat with no learning | Postmortems not tied to gates | [incident_response_and_postmortems.md](./incident_response_and_postmortems.md) · [eval_governance_gates_and_signoff.md](./eval_governance_gates_and_signoff.md) |
| Access is too broad or untracked | RBAC or ABAC not enforced or logged | [roles_and_access_rbac_abac.md](./roles_and_access_rbac_abac.md) |
| Waivers never expire | Risk register lacks owner or timer | [risk_register_and_waivers.md](./risk_register_and_waivers.md) |
| Users say answers are opaque | No public card, weak rationale trail | [model_governance_model_cards_and_releases.md](./model_governance_model_cards_and_releases.md) · [transparency_and_explainability.md](./transparency_and_explainability.md) |

---

## Governance in 60 seconds

1. **Gate before ship**  
   Require cite-then-explain, ΔS ≤ 0.45, coverage ≥ 0.70 on 3 paraphrases and 2 seeds.
2. **Lock the policy surface**  
   For each change, capture who, what, why, and link to risk entry. Block if approvals missing.
3. **Prove lineage**  
   Emit a joinable record for question, snippets, ΔS, λ state, policy checks, model rev.
4. **Escalate with a plan**  
   If any gate fails, open the page from the table above and attach a time-boxed fix.

---

## Copy-paste governance gate

```yaml
governance_gate:
  approvals: required
  citations: cite_then_explain
  eval_window:
    seeds: 2
    paraphrases: 3
  targets:
    deltaS: <=0.45
    coverage: >=0.70
    lambda: convergent
  artifacts:
    lineage_log: required
    change_request: required
    model_card: required
  waivers:
    owner: required
    expiry_days: 30
    reason: required
block_on_failure: true
````

---

## FAQ

**Q1. We already have security reviews. Why add governance here as well**
Security reviews focus on systems and data access. Governance closes the policy loop for prompts, models, eval, and end user impact. It gives repeatable gates for ΔS, coverage, and approvals so releases are auditable.

**Q2. What is the fastest path to “good enough” governance for a small team**
Start with three items. Change control for prompts and models. Eval gate with cite-then-explain and ΔS and coverage targets. A minimal lineage log that joins questions, snippets, and approvals.

**Q3. How do I prove PII minimization without slowing teams down**
Tag sensitivity at ingest, redact at export, and enforce a schema that carries policy flags with each snippet. Keep a joinable audit log. See PII handling and the audit pages.

**Q4. Our legal team asks who owns the generated outputs. What should we track**
Record the base model license, any fine-tune datasets with rights, and the allowed uses. Store the link to the release note and model card for each production rev.

**Q5. We passed eval but a week later users saw regressions**
Your gate is not attached to change control. Hook the same eval and targets to the approval workflow and block deploys if the gate fails.

**Q6. What is a practical rule for waivers**
Every waiver must have an owner, an expiry, a review link, and a rollback. Put it in a risk register and report open waivers weekly.

**Q7. People ask for explainability but do not read long reports**
Provide a short model card and keep the citation trail visible. For complex cases include one visual lineage join to show where an answer came from.

**Q8. Which metrics should appear on an executive dashboard**
Policy coverage, count of approved changes, open waivers by age, ΔS and coverage medians, incident count and mean time to resolution, and percentage of runs with cite-then-explain.

**Q9. How do we align with new regulations without rewriting everything**
Keep your policy baseline and evidence mapping separate from code. Store proofs in an immutable sink and link them to releases. Update the mappings as new rules arrive.

**Q10. What triggers an escalation**
Any failed gate, waiver beyond expiry, missing lineage, or production PII event. Follow the escalation page and attach a dated recovery plan.

---

### 🔗 Quick-Start Downloads (60 sec)

| Tool | Link | 3-Step Setup |
|------|------|--------------|
| **WFGY 1.0 PDF** | [Engine Paper](https://github.com/onestardao/WFGY/blob/main/I_am_not_lizardman/WFGY_All_Principles_Return_to_One_v1.0_PSBigBig_Public.pdf) | 1️⃣ Download · 2️⃣ Upload to your LLM · 3️⃣ Ask “Answer using WFGY + <your question>” |
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
