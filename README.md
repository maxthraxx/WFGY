````markdown
<!--
╭────────────────────────────────────────────────────────╮
│  W F G Y   S D K   ·   SELF-HEALING VARIANCE GATE      │
╰────────────────────────────────────────────────────────╯
-->

<p align="center">
  <img alt="WFGY Logo" src="docs/assets/wfgy_logo.png" width="240"><br>
  <strong>Turn any LLM—yes, even GPT-2—into an accuracy-addicted, hallucination-resistant super-brain in&nbsp;5 minutes.</strong>
</p>

<p align="center">
  <a href="https://github.com/onestardao/WFGY/actions/workflows/ci.yml">
    <img alt="CI" src="https://github.com/onestardao/WFGY/actions/workflows/ci.yml/badge.svg">
  </a>
  &nbsp;
  <a href="https://colab.research.google.com/github/onestardao/WFGY/blob/main/README_demo.ipynb">
    <img alt="Run on Colab" src="https://img.shields.io/badge/Colab-Run-yellow?logo=google-colab&labelColor=555555">
  </a>
  &nbsp;
  <a href="https://huggingface.co/spaces/onestardao/wfgy-demo">
    <img alt="Live Demo" src="https://img.shields.io/badge/HF-Space-blue?logo=huggingface&labelColor=555555">
  </a>
  &nbsp;
  <a href="https://doi.org/10.5281/zenodo.15630970">
    <img alt="DOI" src="https://img.shields.io/badge/DOI-10.5281%2Fzenodo.15630970-blue">
  </a>
</p>

> **One click. Forty percent less logit noise.**  
> Help us reach **10 000 ⭐ before July 1** to unlock **WFGY 2.0** (otherwise it goes pay-walled forever).

---

## 🚀 TL;DR – Five-Minute Magic

```bash
git clone https://github.com/onestardao/WFGY.git
cd WFGY
pip install -e .
python examples/example_01_basic_run.py      # variance / KL in terminal
````

or hit **“Run on Colab”** above and watch the histogram shrink—no GPU needed.

---

## ✨ Why WFGY?

| Pain                | Classic LLM | With WFGY              |
| ------------------- | ----------- | ---------------------- |
| Hallucination       | frequent    | drastically reduced    |
| Random logit spikes | everywhere  | variance ↓ 40–90 %     |
| Prompt sensitivity  | fragile     | robust, self-healing   |
| Black-box fear      | opaque      | ONNX graphs + open API |

---

## 🧩 Module Overview

| Acronym  | Role                | One-liner                      |
| -------- | ------------------- | ------------------------------ |
| **BBMC** | Semantic residue    | detects mis-alignment `I vs G` |
| **BBPF** | Progression flow    | smooths reasoning trajectory   |
| **BBCR** | Collapse–rebirth    | catches & restarts divergence  |
| **BBAM** | Attention modulator | squeezes logit noise           |

All public specs & ONNX graphs live in **[`specs/`](./specs)**.

---

## 🔥 Quick Start (Python)

```python
import wfgy_sdk as w, numpy as np
from wfgy_sdk.evaluator import pretty_print, compare_logits

raw = np.random.randn(32000)              # dummy logits
G = np.random.randn(256); G /= np.linalg.norm(G)
I = G + np.random.normal(scale=0.05, size=256)

out = w.get_engine().run(I, G, raw)
pretty_print(compare_logits(raw, out))
```

---

## 🖥️ CLI

```bash
wfgy "Explain quantum entanglement in emojis."
```

---

## 🌐 Live Demo

A zero-install Gradio Space:
[https://huggingface.co/spaces/onestardao/wfgy-demo](https://huggingface.co/spaces/onestardao/wfgy-demo)

Type a prompt → instant variance/KL → share to Twitter button included.

---

## 🐳 Docker (headless)

```bash
docker run -p 7860:7860 ghcr.io/onestardao/wfgy-lite:latest
open http://localhost:7860
```

---

## 📂 Secret Folder & Hidden Papers

**`I_am_not_lizardman/`** contains eight “Challenge-Einstein” papers and other easter eggs.
Find them, brag on Twitter, collect internet points.

---

## 📜 Official Paper

> **“WFGY 1.0 – A Self-Healing Variance Gate for Large-Scale Language Models”**
> Zenodo DOI 10.5281/zenodo.15630970

PDF is included in `/docs/` and mirrored on Zenodo for permanent access.

---

## 🚧 Roadmap

| Milestone                                  | ETA      | Status |
| ------------------------------------------ | -------- | ------ |
| Hugging Face Space MVP                     | now      | ✅      |
| CI badge & artifact GIF                    | now      | ✅      |
| Telegram `/wfgy` bot                       | v1.1     | 🟡     |
| Variance-drop on GPU tensors               | v1.1     | 🟡     |
| **WFGY 2.0** (adaptive gamma, cross-modal) | ⭐ 10 000 | 🔒     |

---

## Citation

```
@misc{psbigbig_2025_wfgy,
  title  = {WFGY 1.0: A Self-Healing Variance Gate for LLMs},
  author = {PSBigBig},
  year   = 2025,
  doi    = {10.5281/zenodo.15630970},
  url    = {https://github.com/onestardao/WFGY}
}
```

---

<p align="center">  
<i>Play WFGY for more than five minutes and you may never return to traditional AI.</i>  
</p>
```
