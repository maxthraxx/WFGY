# License and Dataset Rights — Guardrails and Fix Pattern

This page tracks **legal and licensing risks** in AI systems.  
If datasets, embeddings, or outputs rely on unverified sources, you risk compliance violations, takedowns, or IP litigation.  
Use this guide to enforce clear rights boundaries across ingestion, training, and generation.

---

## When to use this page
- You do not know the license of a dataset included in your retrieval or training pipeline.  
- Mixed rights (MIT, Apache, proprietary, unknown) exist in the same corpus.  
- Legal review requires proof that generated answers respect dataset terms.  
- Audit asks for compliance with GDPR/CCPA or publisher licensing.  

---

## Acceptance targets
- 100% of datasets tagged with a license identifier.  
- ≥ 95% coverage of ingestion checks include license + attribution metadata.  
- ΔS stability maintained when filtering licensed vs. non-licensed subsets.  
- Audit logs capture `license_id`, `rights_holder`, `expiry`.  
- LLM refuses or flags outputs when license terms are violated.  

---

## Common failures → exact fixes

| Symptom | Likely cause | Open this |
|---------|--------------|-----------|
| Snippets from unknown or scraped sources appear | dataset missing license metadata | [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md) |
| Open source corpus mixes with paid corpus | no role/rights separation | [roles_and_access_rbac_abac.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Governance/roles_and_access_rbac_abac.md) |
| Model answers cite restricted publishers | no attribution enforcement | [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) |
| Generated outputs reuse licensed patterns | prompt injection bypassing rights filter | [prompt-injection.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/prompt-injection.md) |
| Training run includes expired or revoked dataset | missing expiry validation | [policy_baseline.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Governance/policy_baseline.md) |

---

## Fix in 60 seconds

1. **Tag every dataset**  
   Attach `{license_id, rights_holder, expiry, attribution_required}` at ingestion.  

2. **Separate corpora**  
   Open source vs. proprietary vs. paid corpora must remain in distinct retrieval indices.  

3. **Enforce attribution**  
   Require citation-first prompting for any licensed corpus.  

4. **Audit pipeline**  
   Store logs with dataset version, license, and usage context.  

5. **Expiry enforcement**  
   Block or purge expired corpora automatically.  

---

## Minimal compliance checklist

- [ ] Every ingestion pipeline requires license metadata.  
- [ ] RBAC + ABAC enforced to keep datasets separated.  
- [ ] Retrieval schema logs license_id with every snippet.  
- [ ] Expiry checks run nightly.  
- [ ] Audit reports exportable on request.  

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

