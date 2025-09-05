# Eval: Operator Guidelines

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **Eval**.  
  > To reorient, go back here:  
  >
  > - [**Eval** — model evaluation and benchmarking](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>


This page sets strict rules for **human operators and evaluators** running WFGY-aligned evaluation suites. Evaluation is not a free-form activity. It must follow consistent contracts, logging standards, and reproducible steps.

---

## Open these first

* Gold set design: [goldset\_curation.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Eval/goldset_curation.md)
* Precision/recall evals: [eval\_rag\_precision\_recall.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Eval/eval_rag_precision_recall.md)
* Observability probes: [alerting\_and\_probes.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Eval_Observability/alerting_and_probes.md)

---

## Acceptance targets

* **Inter-annotator agreement** ≥ 0.85 across 3 operators
* **Annotation variance** ≤ 10%
* **Audit reproducibility** ≥ 95% (rerun matches logged label)
* **No operator-induced drift**: ΔS stability remains within ±0.05 after evaluation

---

## Operator responsibilities

1. **Stay schema-locked**
   Every operator must apply the same definition of "correct" → answer cites the correct snippet and explains consistently.

2. **Use three-paraphrase rule**
   Rephrase the query 3× before marking coverage. If answer flips across paraphrases, log as unstable.

3. **Log ΔS and λ**
   Each annotated run must include structural metrics: ΔS(question,retrieved), λ states, snippet IDs.

4. **Apply cost view**
   Record token counts and cost-per-correct when judging pipelines.

5. **No ad-hoc overrides**
   Do not improvise “fixes” in evaluation logs. All fixes must point to an existing ProblemMap page.

---

## Annotation protocol

* **Step 1: Load baseline**
  Open gold set. Verify expected snippet IDs.

* **Step 2: Apply candidate system**
  Run the same queries with candidate pipeline.

* **Step 3: Compare**

  * If candidate cites correct snippet and stays under ΔS ≤ 0.45 → mark correct.
  * If citation missing or ΔS ≥ 0.60 → mark fail, attach probable ProblemMap fix.

* **Step 4: Log JSON**

```json
{
  "operator": "user123",
  "q_id": "Q42",
  "question": "What is the cutoff for semantic drift?",
  "expected_snippet": "S123",
  "candidate_snippet": "S123",
  "ΔS": 0.39,
  "λ_state": "→",
  "correct": true,
  "cost_usd": 0.0012,
  "notes": "Stable across 3 paraphrases"
}
```

---

## When to escalate

* Annotators disagree by >15% → escalate to eval lead.
* ΔS drifts beyond thresholds but operators label "correct" → escalate and reconcile.
* Costs exceed 1.5× baseline → halt run until reviewed.

---

## Audit checklist

* [ ] All logs stored in versioned JSONL.
* [ ] At least 2 operators per eval run.
* [ ] Spot check 10% of logs with independent reviewer.
* [ ] Archive outputs with system hash, gold set version, and ProblemMap pointers.

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

