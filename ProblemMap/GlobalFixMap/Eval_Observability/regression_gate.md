# Eval Observability — Regression Gate

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **Eval_Observability**.  
  > To reorient, go back here:  
  >
  > - [**Eval_Observability** — evaluation metrics and system observability](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>


A structural safeguard that enforces measurable thresholds before any pipeline is promoted to production.  
Use this page to define hard acceptance criteria (ΔS, coverage, λ, resonance) and stop silent regressions from shipping.

---

## Why regression gates matter

- **Catch semantic drift early**: A small rise in ΔS leads to compounding hallucinations downstream.  
- **Stable releases**: Prevents model upgrades or retraining from silently reducing accuracy.  
- **Auditable rules**: Clear thresholds mean every team member can verify before deploy.  
- **Cross-stack consistency**: Same rules apply across providers, retrievers, and orchestration layers.

---

## Core gate thresholds

| Metric | Requirement | Failure signal |
|--------|-------------|----------------|
| ΔS(question, retrieved) | ≤ 0.45 | drift ≥ 0.60 means block release |
| Coverage of target section | ≥ 0.70 | low coverage = missing context |
| λ_observe | Convergent across 3 paraphrases, 2 seeds | divergence = unstable reasoning |
| E_resonance | Flat on 50–100 step windows | spikes = entropy collapse risk |

---

## Deployment checklist

1. **Pre-release batch eval**  
   Run gold set of ~100–500 Q&A pairs. Collect ΔS, coverage, λ, resonance.

2. **Gate decision**  
   - If ΔS ≤ 0.45 AND coverage ≥ 0.70 → **pass**.  
   - If ΔS between 0.46–0.59 → **manual review**.  
   - If ΔS ≥ 0.60 OR coverage < 0.70 → **fail, block release**.

3. **Variance probe**  
   Check λ stability across 3 paraphrases × 2 seeds. Divergence disqualifies release.

4. **Regression log**  
   Store results with index hash + commit hash + retriever config.  
   Enables reproducibility and rollback.

---

## Example gating script (pseudo)

```yaml
# regression_gate.yml
metrics:
  deltaS: <=0.45
  coverage: >=0.70
  lambda: convergent
  resonance: flat
goldset: eval_set_500.json
policy:
  fail_on_drift: true
  manual_review_range: [0.46, 0.59]
  require_seeds: 2
  require_paraphrases: 3
````

---

## Common pitfalls

* **Changing retriever k** without updating gates. Always re-test thresholds.
* **Skipping paraphrase probes**. One stable query is not enough.
* **Not logging coverage**. ΔS alone cannot prove retrieval completeness.
* **Silent config drift**. Gate must bind to exact retriever + index hash.

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
