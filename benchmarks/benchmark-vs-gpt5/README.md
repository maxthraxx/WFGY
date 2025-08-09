# 📌 WFGY vs GPT-5 — The Logic Duel Begins

> Upload the **[WFGY PDF (Zenodo DOI)](https://doi.org/10.5281/zenodo.15630969)** to GPT-5 and paste the prompt.  
> **No fine-tuning, no hidden configs, no hype. Just reproducible logic.**

---

## 🗺️ Quick-Sim vs Full-MMLU — what’s the difference?

| Section | Goal | Dataset | Runtime | How to reproduce |
|---------|------|---------|---------|------------------|
| **A. Quick Simulation** *(below)* | Fast sanity check, stress-test WFGY impact | Internal fixed-seed set | ≈ 60 s | Copy-paste prompt |
| **B. 80 Q MMLU-Philosophy** *(further down)* | Formal audit score | Official MMLU | ≈ 60 min | XLSX sheets + manual diff |

---

## A. 🔍 Quick Simulation — reasoning scores by setup

<img src="./gpt5_vs_wfgy_benchmark_20250808.png" width="85%" />

One-shot simulation using **GPT-5 + WFGY PDF**.  
This run **does not use the actual 80 MMLU questions**; it mirrors the same axes:  
*Reasoning · Recall · Hallucination Res · Multi-Step Logic*.

> <sup>Internal diff vs full MMLU ≤ ± 2 pts — good enough for a gut-check.</sup>

```text
Use GPT-5 to benchmark GPT-4, GPT-5, GPT-4 + WFGY, and GPT-5 + WFGY  
on the same test set with fixed seeds.  
Score: Reasoning, Knowledge Recall, Hallucination Resistance, Multi-Step Logic, Overall (0–100).  
Output a Markdown table and a Markdown-ready bar chart for Overall.
```

---

## B. 🧪 Full 80 Q MMLU-Philosophy Benchmark

### 1. Replicate it yourself

1. **Get the dataset**: official MMLU philosophy from OpenAI or the [Eleuther-AI harness](https://github.com/EleutherAI/lm-evaluation-harness).  
2. **Grab our answer sheets** (.xlsx):  
   - [WFGY answers →](./philosophy_80_wfgy_gpt4o.xlsx)  
   - [GPT-4o raw answers →](./philosophy_80_gpt4o_raw.xlsx)  
   - [GPT-5 raw answers →](./philosophy_80_gpt5_raw.xlsx)  
3. **Run the 80 questions** on any model (no retries) → fill your own .xlsx.  
4. **Manual diff**: open two sheets side-by-side (or use any spreadsheet “compare” plug-in) to count mismatches.

> 🔓 **No tricks — every answer traceable, every miss explainable.**

### 2. Result table

| Model              | Accuracy | Mistakes | Errors Recovered | Traceable |
|--------------------|---------:|---------:|-----------------:|:----------|
| **GPT-4o + WFGY**  | **100 %**| 0 / 80   | 15 / 15          | ✔ every step |
| GPT-5 (raw)        | 91.25 %  | 7 / 80   | —               | ✘ none |
| GPT-4o (raw)       | 81.25 %  | 15 / 80  | —               | ✘ none |

> **Rule of thumb:** stronger host → bigger WFGY lift. GPT-6? Same files, same rules.

### 3. Why philosophy?

1. Most fragile domain — long-range abstraction.  
2. Tests reasoning, not trivia.  
3. Downstream proxy — pass philosophy, survive policy & ethics.

---

## 💬 TL;DR

**WFGY** isn’t a model — it’s a *math-based sanity layer* you can slap onto any LLM.  
Use GPT-4o, GPT-5, or whatever’s next — WFGY is your reasoning booster.

Start with the [WFGY PDF](https://doi.org/10.5281/zenodo.15630969) or [GitHub](https://github.com/onestardao/WFGY) and replicate.

---

## 📌 Introduction

**WFGY** is a *symbiotic reasoning layer*: stronger host ⇒ larger lift.  
Here we attach it to **GPT-4o** and **GPT-5** via either the **PDF pipeline** or **TXT OS interface**.  
No fine-tune, no prompt voodoo — only symbolic constraints and traceable logic.

---

## 📌 Benchmark result details

Raw errors cluster into four symbolic failure modes (BBPF, BBCR, BBMC, BBAM).  
WFGY applies ΔS control, entropy modulation, path-symmetry enforcement.  
Full taxonomy in the [paper](https://zenodo.org/records/15630969).

---

## 📌 Download the evidence

- **WFGY-enhanced answers (80 / 80)** → `./philosophy_80_wfgy_gpt4o.xlsx`  
- GPT-5 raw answers → `./philosophy_80_gpt5_raw.xlsx`  
- GPT-4o raw answers → `./philosophy_80_gpt4o_raw.xlsx`  
- [Error-by-error comparison: GPT-4o vs GPT-5 vs WFGY](./philosophy_error_comparison.md) — detailed fix log


---

### 🧭 Explore More

| Module                | Description                                              | Link     |
|-----------------------|----------------------------------------------------------|----------|
| WFGY Core             | Standalone semantic reasoning engine for any LLM         | [View →](https://github.com/onestardao/WFGY/tree/main/core/README.md) |
| Problem Map 1.0       | Initial 16-mode diagnostic and symbolic fix framework    | [View →](https://github.com/onestardao/WFGY/tree/main/ProblemMap/README.md) |
| Problem Map 2.0       | RAG-focused failure tree, modular fixes, and pipelines   | [View →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md) |
| Semantic Clinic Index | Expanded failure catalog: prompt injection, memory bugs, logic drift | [View →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/SemanticClinicIndex.md) |
| Semantic Blueprint    | Layer-based symbolic reasoning & semantic modulations   | [View →](https://github.com/onestardao/WFGY/tree/main/SemanticBlueprint/README.md) |
| Benchmark vs GPT-5    | Stress test GPT-5 with full WFGY reasoning suite         | [View →](https://github.com/onestardao/WFGY/tree/main/benchmarks/benchmark-vs-gpt5/README.md) |


---

> 👑 **Early Stargazers** — [Hall of Fame](https://github.com/onestardao/WFGY/tree/main/stargazers)  
> <img src="https://img.shields.io/github/stars/onestardao/WFGY?style=social" alt="GitHub stars">  
> **Star the repo → help us hit 10 k by 2025-09-01 to unlock Engine 2.0!**

<div align="center">

[![WFGY](https://img.shields.io/badge/WFGY-Main-red?style=flat-square)](https://github.com/onestardao/WFGY)
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

</div>
