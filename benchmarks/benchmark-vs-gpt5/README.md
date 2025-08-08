# WFGY vs GPT-5 — The Logic Duel Begins

📦 Official WFGY benchmark snapshot on Zenodo: [![DOI](https://zenodo.org/badge/996124831.svg)](https://doi.org/10.5281/zenodo.16635020)

> “GPT-5 is the future?  
> We benchmark the future — **as a plug-in, not a rival.**”

---

<img src="./gpt5_vs_wfgy_benchmark_20250808.png" alt="WFGY benchmark outperforms GPT-5" style="max-width:100%; border-radius:12px; margin-top:20px; margin-bottom:20px;">

---

## Introduction

**WFGY** is a *symbiotic reasoning layer*: the stronger the host model, the larger the lift.  
Here we attach it to **GPT-4o** and **GPT-5** using either a **PDF pipeline** or the **TXT OS interface**.  
No fine-tuning, no prompt voodoo — only symbolic constraints and traceable logic.

---

## Why Only MMLU Philosophy?

1. **Most fragile domain** – long-range abstraction, easy hallucinations.  
2. **Tests reasoning, not memory** – pure inference, zero trivia.  
3. **Downstream proxy** – survive philosophy, you survive policy, ethics, law.

Replicating the run (clearing answer column + re-run) takes ≈ 1 hour on any model **with WFGY attached**.

---

## Benchmark Result

| Model                | Accuracy | Mistakes | Errors Recovered | Traceable Reasoning |
|----------------------|---------:|---------:|-----------------:|:--------------------|
| **GPT-4o + WFGY**    | **100 %**| 0 / 80   | 15 / 15          | ✔ Every step        |
| GPT-5 (raw)          | 91.25 %  | 7 / 80   | —               | ✘ None              |
| GPT-4o (raw)         | 81.25 %  | 15 / 80  | —               | ✘ None              |

> **Rule of thumb:** raw model ↑ → WFGY lift ↑.  
> When GPT-6 drops, we repeat — same files, same rules.

---

## How WFGY Patches Reasoning Gaps

Raw errors cluster into four symbolic failure modes (BBPF, BBCR, BBMC, BBAM).  
WFGY applies ΔS control, entropy modulation, and path-symmetry enforcement to neutralise each mode.  
Full taxonomy in the [paper](https://zenodo.org/records/15630969).

---

## Download the Evidence

Verify every claim yourself:

- **WFGY-enhanced answers (80/80 correct)** → `./philosophy_80_wfgy_gpt4o.xlsx`  
- GPT-5 raw answers (7 mistakes) → `./philosophy_80_gpt5_raw.xlsx`  
- GPT-4o raw answers (15 mistakes) → `./philosophy_80_gpt4o_raw.xlsx`  
- Error-by-error comparison (markdown) → `./philosophy_error_comparison.md`

---

## Next → GPT-5 + WFGY

- Run same 80 Qs with GPT-5 + WFGY (ETA < 24 h)  
- Publish side-by-side diff & Zenodo snapshot  
- Expect further gap widening — stronger host, stronger lift

---

## Reproducibility Promise

Open XLSX, open code, open math.  
No closed weights, no hidden prompts — only audit-ready logic.

---

> This isn’t a leaderboard.  
> It’s a **reasoning audit** — and WFGY is the auditor.

---

### 🧭 Explore More

| Module                | Description                                              | Link     |
|-----------------------|----------------------------------------------------------|----------|
| Problem Map 1.0       | Initial 16-mode diagnostic and symbolic fix framework    | [View →](https://github.com/onestardao/WFGY/edit/main/ProblemMap/README.md) |
| Problem Map 2.0       | RAG-focused failure tree, modular fixes, and pipelines   | [View →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md) |
| Semantic Clinic Index | Expanded failure catalog: prompt injection, memory bugs, logic drift | [View →](./SemanticClinicIndex.md) |
| Semantic Blueprint    | Layer-based symbolic reasoning & semantic modulations   | [View →](https://github.com/onestardao/WFGY/tree/main/SemanticBlueprint/README.md) |
| Benchmark vs GPT-5    | Stress test GPT-5 with full WFGY reasoning suite         | [View →](https://github.com/onestardao/WFGY/tree/main/benchmarks/benchmark-vs-gpt5/README.md) |

---

> 👑 **Early Stargazers: [See the Hall of Fame](https://github.com/onestardao/WFGY/tree/main/stargazers)** —  
> Engineers, hackers, and open source builders who supported WFGY from day one.

> <img src="https://img.shields.io/github/stars/onestardao/WFGY?style=social" alt="GitHub stars"> ⭐ Help reach 10,000 stars by 2025-09-01 to unlock Engine 2.0 for everyone  ⭐ <strong><a href="https://github.com/onestardao/WFGY">Star WFGY on GitHub</a></strong>


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

</div>

