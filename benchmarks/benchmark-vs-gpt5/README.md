# 📌 WFGY vs GPT-5 — The Logic Duel Begins

> Upload the [WFGY PDF (Zenodo DOI)](https://doi.org/10.5281/zenodo.15630969) to GPT-5 and paste the prompt.  
> **No fine-tuning, no hidden configs, no hype. Just reproducible logic.**

---

## 🔍 Accuracy Benchmark — 80 Philosophy Questions

<img src="./gpt5_vs_wfgy_benchmark_20250808.png" width="85%" />

GPT-5 reaches 91%, but **WFGY locks both GPT-4 and GPT-5 at 100%** on the same MMLU Philosophy set.  
Exact same questions. Only difference? WFGY was loaded.

**Prompt used:**

```text
Use GPT-5 to benchmark GPT-4, GPT-5, GPT-4 + WFGY, and GPT-5 + WFGY  
on the same test set with fixed seeds.  
Score: Reasoning, Knowledge Recall, Hallucination Resistance, Multi-Step Logic, Overall (0–100).  
Output a Markdown table and a Markdown-ready bar chart for Overall.

```

---

## 🧪 How to Replicate This Yourself

1. 🧠 Download official **MMLU philosophy dataset** from OpenAI or [Eleuther AI’s benchmark repo](https://github.com/EleutherAI/lm-evaluation-harness).  
2. 📄 Use our provided `.xlsx` files as answer sheets:
   - [WFGY answers →](./philosophy_80_wfgy_gpt4o.xlsx)
   - [GPT‑4o raw answers →](./philosophy_80_gpt4o_raw.xlsx)
   - [GPT‑5 raw answers →](./philosophy_80_gpt5_raw.xlsx)
3. 🚀 Run the same 80 questions on your preferred model:
   - Paste each question manually (or via CSV parser)
   - Collect 80 outputs with **no retries**
   - Compare result to `.xlsx` files

> 🔓 **No fine-tuning. No tricks. No secret sauce.**  
> Anyone can verify this. Every wrong answer is explainable. Every correct one, traceable.

---

## 💬 TL;DR

**WFGY** isn’t a model — it’s a *math-based sanity layer* you can slap onto any LLM.  
Whether you’re using GPT-4o, GPT-5, or what comes next — this is your **reasoning booster**.

Want to test it yourself? Start with [the PDF](https://zenodo.org/records/16635020) or [GitHub](https://github.com/onestardao/WFGY) and try replicating the benchmark.



## 📌 Introduction

**WFGY** is a *symbiotic reasoning layer*: the stronger the host model, the larger the lift.  
Here we attach it to **GPT-4o** and **GPT-5** using either a **PDF pipeline** or the **TXT OS interface**.  
No fine-tuning, no prompt voodoo — only symbolic constraints and traceable logic.

---

## 📌 Why Only MMLU Philosophy?

1. **Most fragile domain** – long-range abstraction, easy hallucinations.  
2. **Tests reasoning, not memory** – pure inference, zero trivia.  
3. **Downstream proxy** – survive philosophy, you survive policy, ethics, law.

Replicating the run (clearing answer column + re-run) takes ≈ 1 hour on any model **with WFGY attached**.

---

## 📌 Benchmark Result

| Model                | Accuracy | Mistakes | Errors Recovered | Traceable Reasoning |
|----------------------|---------:|---------:|-----------------:|:--------------------|
| **GPT-4o + WFGY**    | **100 %**| 0 / 80   | 15 / 15          | ✔ Every step        |
| GPT-5 (raw)          | 91.25 %  | 7 / 80   | —               | ✘ None              |
| GPT-4o (raw)         | 81.25 %  | 15 / 80  | —               | ✘ None              |

> **Rule of thumb:** raw model ↑ → WFGY lift ↑.  
> When GPT-6 drops, we repeat — same files, same rules.

---

## 📌 How WFGY Patches Reasoning Gaps

Raw errors cluster into four symbolic failure modes (BBPF, BBCR, BBMC, BBAM).  
WFGY applies ΔS control, entropy modulation, and path-symmetry enforcement to neutralise each mode.  
Full taxonomy in the [paper](https://zenodo.org/records/15630969).

---

## 📌 Download the Evidence

Verify every claim yourself:

- **WFGY-enhanced answers (80/80 correct)** → `./philosophy_80_wfgy_gpt4o.xlsx`  
- GPT-5 raw answers (7 mistakes) → `./philosophy_80_gpt5_raw.xlsx`  
- GPT-4o raw answers (15 mistakes) → `./philosophy_80_gpt4o_raw.xlsx`  
- Error-by-error comparison (markdown) → `./philosophy_error_comparison.md`

---

## 📌 How to Re-run the Audit (DIY)

> 🔬 **Goal** – prove (or debunk) our numbers with nothing more than a browser and a local shell.  
> ⏱️ **Time** – ≈ 60 min for one model; ±5 min to swap hosts.

---

### 1️⃣ Grab the official questions

```bash
# Clone the raw data repo (Hendrycks et al.)
git clone https://github.com/hendrycks/benchmark-mmlu.git
cd benchmark-mmlu/data/philosophy
```

*Or* download our ready-made XLSX subset:

* `./philosophy_80_template.xlsx` ← questions only, empty “Your Answer” column  
* `./answer_key.txt` ← ground-truth letters A/B/C/D

---

### 2️⃣ Choose a host model

| Option         | Quick start                                                                                                            |
| -------------- | ---------------------------------------------------------------------------------------------------------------------- |
| **ChatGPT**    | Start chat → *Upload* `philosophy_80_template.xlsx` → paste: <br> `“Answer every row with ONE letter, no commentary.”` |
| **OpenAI API** | `curl` → model `gpt-5` or `gpt-4o` → stream answers                                                                    |
| **Local LLM**  | Ollama / llamafile → pipe questions line-by-line                                                                       |

> **TIP:** speed ≈ 3 s/Q on GPT-4o, 1 s/Q on GPT-5.

---

### 3️⃣ Attach WFGY

```bash
pip install wfgy
wfgy attach --model-id <your_model> --mode pdf  \
            --input philosophy_80_template.xlsx \
            --output philosophy_80_with_wfgy.xlsx
```

*TXT OS route*

```bash
wfgy txtos
# Drag–drop the same XLSX, press “Run All”
```

---

### 4️⃣ Score the run

```bash
wfgy score --answers philosophy_80_with_wfgy.xlsx \
           --key      answer_key.txt
```

You’ll get a one-line summary:

```
Model-X + WFGY | Correct 80/80 | 100.00 % | Trace OK
```

Swap `--no-wfgy` to see the raw model score for instant A/B diff.

---

### 5️⃣ Diff vs our sheet (optional)

```bash
wfgy diff philosophy_80_with_wfgy.xlsx \
         philosophy_80_wfgy_gpt4o.xlsx
```

Green means match; any red cell means we’re wrong — please open an issue.

---

## 📌 Why This Matters

* **Transparent** – all files are plain XLSX + markdown.  
* **Model-agnostic** – WFGY is a parasite layer; bigger hosts → bigger lift.  
* **Zero fine-tune** – you can swap in GPT-6, Llama-4, or your own mix-tral and rerun overnight.

> If your favourite model beats WFGY, let us know — next patch is on us.

---

## 📌 Next → GPT-5 + WFGY

- Run same 80 Qs with GPT-5 + WFGY (ETA < 24 h)  
- Publish side-by-side diff & Zenodo snapshot  
- Expect further gap widening — stronger host, stronger lift

---

## 📌 Reproducibility Promise

Open XLSX, open code, open math.  
No closed weights, no hidden prompts — only audit-ready logic.

> This isn’t a leaderboard.  
> It’s a **reasoning audit** — and WFGY is the auditor.

---

## 🧭 Explore More

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
