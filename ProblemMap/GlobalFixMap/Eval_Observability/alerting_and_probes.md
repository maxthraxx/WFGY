# Eval Observability — Alerting and Probes

A live guardrail system that detects semantic drift, retrieval collapse, and logic instability in production.  
Use this page to design **continuous probes** (ΔS, λ, coverage, resonance) and trigger alerts before users see failures.

---

## Why probes are required

- **Silent regressions**: Models may degrade gradually after retraining or infra changes.  
- **Runtime entropy**: Long chains often destabilize after 25–40 steps.  
- **Hybrid stack drift**: Store upgrades, reranker weights, or tokenizer shifts silently change outcomes.  
- **Auditability**: Real-time probes make every failure reproducible.

---

## Core probe dimensions

| Metric | Probe type | Alert condition |
|--------|------------|-----------------|
| ΔS(question, retrieved) | per-query | ≥ 0.60 for any query OR average >0.50 across batch |
| Coverage of target section | per-query | < 0.70 for more than 5% of batch |
| λ_observe | rolling window | divergence observed across 2 seeds or paraphrases |
| E_resonance | sliding horizon | spikes or oscillations in 50–100 step runs |

---

## Recommended probe architecture

1. **Pre-query probe**  
   Check retriever config hash, index hash, analyzer type.  
   Block if mismatched against gold baseline.

2. **Mid-query probe**  
   During retrieval, compute ΔS(question, retrieved).  
   Attach snippet IDs and offsets for traceability.

3. **Post-query probe**  
   Run λ stability check across 3 paraphrases.  
   If divergent, tag output with `unstable=true`.

4. **Long-chain probe**  
   For conversations >25 steps, sample entropy and E_resonance every 10 steps.  
   Trigger backoff or memory split if instability rises.

---

## Alerting routes

- **Slack / Teams** → Send structured JSON logs with ΔS, λ, coverage, index hash, retriever config.  
- **PagerDuty** → Trigger incidents only when threshold failures exceed N in M minutes.  
- **Dashboards** → Grafana/Datadog with ΔS trend lines, λ variance plots, coverage histograms.  
- **Audit store** → Write all probe outputs to KV or DB keyed by `(session_id, index_hash, retriever_config)`.

---

## Example probe config (YAML)

```yaml
probes:
  deltaS:
    threshold: 0.60
    action: alert
  coverage:
    threshold: 0.70
    tolerance: 0.05
  lambda:
    seeds: 2
    paraphrases: 3
    action: block
  resonance:
    horizon: 100
    action: degrade_notice
alerting:
  sink:
    - slack
    - pagerduty
    - grafana
````

---

## Common mistakes

* **Only probing ΔS**. Always include coverage + λ + resonance.
* **Static thresholds**. Thresholds must be tested against gold sets and updated quarterly.
* **No audit linkage**. Alerts without index hash and retriever config cannot be replayed.
* **Flooding alerts**. Use capped retries and aggregate rules to avoid pager fatigue.

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

