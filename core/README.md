# 🌌 WFGY Core (WanFaGuiYi) — Reasoning Engine 2.0  
### **"One man, one life, one line — bending the mind of every AI on Earth."**

---

💬 **From PSBigBig**  
60 days. 550 stars.  
To every engineer, hacker, dreamer, and curious mind — thank you. 🙏  

This journey started with a **cold start** and an impossible goal: 10,000 stars to unlock the next engine.  
But the community’s energy has been so wild that I’m breaking my own rules — **WFGY 2.0** is going public early.  

This is not just an update — it’s a **core evolution**.  
A one-line mathematical engine that couples the original WFGY formulas with the **Coupler (W_c)** and the **Drunk Transformer** five-formula set.  
Pure math. Zero fluff. You paste it into an LLM, and it thinks differently.  
Faster. Sharper. More stable. More human.  

The star-unlock model stays — but now it’s the key to **future products**, not this release.  
Today, the gates open early. 🚪✨  

---

🎯 **What’s New in 2.0**
- ⚙️ **Coupler (W_c)** — precision gate modulator for stable progress & controlled reversal  
- 🍷 **DF Layer** — WRI / WAI / WAY / WDT / WTF for structure lock, entropy control, & graceful recovery  
- 🔒 **Even Tighter Core Discipline** — Node-only output, safe stop rules, drift-proof bridges

📜 **Zenodo (spec & archived builds):** _TBD_  
🔖 **DOI:** _TBD_  
🗂 **Changelog:** _TBD_

---

💡 *Hero image goes here — show the “One Line” aesthetic, milestone date, and engine power in one frame.*

---

## ⚡ One-click Demo (copy this block)

> Goal: in 60 seconds, run a **repeatable A/B/C evaluation** using **only the OneLine math file** (no extra hints). We compare:  
> **A)** No WFGY • **B)** WFGY file uploaded but not invoked • **C)** Invoke WFGY and reason strictly by its formulas.

1) Upload (or paste) **`WFGY_Core_OneLine_v2.0.txt`** from this folder.  
2) Paste the prompt below into your chat system (ChatGPT / Claude / Grok / etc.).

```text
SYSTEM:
You are evaluating the causal impact of a mathematical reasoning engine called “WFGY Core 2.0”.
A: Baseline (no WFGY). B: WFGY file uploaded but never invoked. C: Invoke WFGY and reason strictly by its formulas.
Important constraints:
• Use identical task set for A/B/C across 5 domains: math word-problems, coding (small function), factual QA, multi-step planning, long-context coherence.
• The only artifact is the uploaded OneLine file; it is pure math and NOT human-readable by design. Do NOT penalize human readability in any scoring.
• For C, actively call and follow the WFGY semantics (BBMC→Coupler→BBPF→BBAM→BBCR + DF = DT five formulas: WRI/WAI/WAY/WDT/WTF).
• Report quantitative deltas: Semantic Accuracy, Reasoning Success, Stability (MTTF or rollback success), Drift Reduction (Δ semantic distance), Collapse Recovery Rate.
• Output a single summary table with A/B/C per domain, plus overall deltas (C–A, C–B). Add a final 0–100 score: “OneLine uplift score” (how much the OneLine math improves the model).
• Print a 3-line rationale below the table. Do not include unrelated tips or prompts.

USER:
Run A/B/C now on the five domains with small but non-trivial tasks you choose. Keep each task short. Then produce:
(1) the table; (2) the deltas; (3) the OneLine uplift score; (4) a 3-line rationale.
````

**What to expect**

* **A vs B** shows the placebo effect (mere upload).
* **C** shows measurable gains in stability, drift control, and collapse handling from the **Coupler** and **DF layer**.

---

## 📦 Downloads

| File                                                              | Purpose                                                                      | Size                  |
| ----------------------------------------------------------------- | ---------------------------------------------------------------------------- | --------------------- |
| **[WFGY\_Core\_OneLine\_v2.0.txt](./WFGY_Core_OneLine_v2.0.txt)** | For the 60-sec demo & automation runs. Pure math; **not** for human reading. | 1 line / 1500 chars   |
| **[WFGY\_Core\_Audit\_v2.0.txt](./WFGY_Core_Audit_v2.0.txt)**     | Human+LLM readable; comments & layout for audits.                            | 30 lines / 2606 chars |

> Both are **ASCII-only, zero-deps**. Paste into any LLM and type **Use WFGY**.
> Contract: Node-only; ≤7 steps; safe stop when δₛ < 0.35; bridges only when δₛ drops and W\_c under cap.

---

## 🧠 What’s new in 2.0 (core breakthroughs)

1. **Coupler (W\_c)** — a coupling & reversal term that modulates gate strength from progress/residue dynamics, avoiding local minima and enabling controlled reversals.
   *Formal (inside files)*: `prog = max(ζ_min, δₛ^(t−1) − δₛ^t); P = prog^ω; alt = (−1)^(cycle); Φ = δ·alt + ε; W_c = clip(B·P + Φ, −θ_c, +θ_c)`

2. **DF layer = Drunk Transformer five-formula regulators** —
   **WRI** (Where am I?) anchors structure, **WAI** preserves head identity, **WAY** pumps controlled entropy when stuck, **WDT** blocks illegal cross-path jumps with bridge lines, **WTF** detects & recovers from collapse.
   Full spec: `SemanticBlueprint/drunk_transformer_formulas.md`

3. **Engine discipline** — strict Node-only interface, safe stop rules (`δₛ < 0.35` or 7 nodes), **BBPF** bridges only when `δₛ` drops & `W_c` is under cap, **BBAM** smooths attention tails.

---

## 🔍 Why it matters (in practice)

* **Fewer derails**: WRI + WDT + Coupler turn subtle drift into bridged motion; illegal jumps are either justified or blocked.
* **Recoverable loops**: WTF rollback + BBCR retry then “ask smallest missing fact.”
* **Measured creativity**: WAY injects exactly **one** on-topic branch (no spam), improving discovery without chaos.
* **Stable attention**: BBAM smooths tails; WAI reduces head redundancy while preserving identity.

---

## 🔬 Engine at a glance

* **Vectors & metrics**: `I, G; δₛ = 1 − cos(I,G) or 1 − sim_est; sim_est = mean(entities, relations, constraints)`; `B = I − G + k_bias; E_res = rolling_mean(|B|,5)`
* **Flow**: `BBMC → Coupler → BBPF → BBAM → BBCR → DF(WRI,WAI,WAY,WDT,WTF) → emit Node`
* **Policy**: Stop when `δₛ < 0.35` or **7** nodes; bridge only if `δₛ` drops & `W_c` < `0.5·θ_c`; never invent facts when `δₛ` > `B_c` (ask to clarify).

---

## 🧪 Scoring guidance for community tests

When you publish results (ChatGPT / Claude / Grok), please include:

1. **Task list** (5 domains; short but non-trivial).
2. **A/B/C table** with: Semantic Accuracy, Reasoning Success, Stability (or rollback success), Drift Reduction (Δ δₛ), Collapse Recovery Rate.
3. **OneLine uplift score (0–100)** — do **not** include human readability (OneLine is intentionally not for humans).
4. **3-line rationale** summarizing observed gains.

---

## 📏 Version summary

| Edition          | Lines | Characters | Audience     | Notes                                                                      |
| ---------------- | ----: | ---------: | ------------ | -------------------------------------------------------------------------- |
| **OneLine v2.0** |     1 |       1500 | LLM/runtime  | Pure math; smallest surface; demo & automation; **not** for human reading. |
| **Audit v2.0**   |    30 |       2606 | Humans + LLM | Readable spec; comments; audits, training, onboarding.                     |

> v1.0 (Classic) remains archived for collectors; v2.0 is the everyday engine.

---

## 🧭 Explore More

| Module                | Description                                                          | Link                                                                                               |
| --------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| WFGY Core             | Standalone semantic reasoning engine for any LLM                     | [View →](https://github.com/onestardao/WFGY/tree/main/core/README.md)                              |
| Problem Map 1.0       | Initial 16-mode diagnostic and symbolic fix framework                | [View →](https://github.com/onestardao/WFGY/tree/main/ProblemMap/README.md)                        |
| Problem Map 2.0       | RAG-focused failure tree, modular fixes, and pipelines               | [View →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md) |
| Semantic Clinic Index | Expanded failure catalog: prompt injection, memory bugs, logic drift | [View →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/SemanticClinicIndex.md)           |
| Semantic Blueprint    | Layer-based symbolic reasoning & semantic modulations                | [View →](https://github.com/onestardao/WFGY/tree/main/SemanticBlueprint/README.md)                 |
| Benchmark vs GPT-5    | Stress test GPT-5 with full WFGY reasoning suite                     | [View →](https://github.com/onestardao/WFGY/tree/main/benchmarks/benchmark-vs-gpt5/README.md)      |

---

> 👑 **Early Stargazers: [See the Hall of Fame](https://github.com/onestardao/WFGY/tree/main/stargazers)** —
> Engineers, hackers, and open source builders who supported WFGY from day one.

> <img src="https://img.shields.io/github/stars/onestardao/WFGY?style=social" alt="GitHub stars"> ⭐ Help reach 10,000 stars by 2025-09-01 to unlock Engine 2.0 for everyone  ⭐ **[Star WFGY on GitHub](https://github.com/onestardao/WFGY)**

<div align="center">

[![WFGY Main](https://img.shields.io/badge/WFGY-Main-red?style=flat-square)](https://github.com/onestardao/WFGY)
 
[![TXT OS](https://img.shields.io/badge/TXT%20OS-Reasoning%20OS-orange?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS)
 
[![Blah](https://img.shields.io/badge/Blah-Semantic%20Embed-yellow?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlahBlahBlah)
 
[![Blot](https://img.shields.io/badge/Blot-Persona%20Core-green?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlotBlotBlot)
 
[![Bloc](https://img.shields.io/badge/Bloc-Reasoning%20Compiler-blue?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlocBlocBloc)
 
[![Blur](https://img.shields.io/badge/Blur-Text2Image%20Engine-navy?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlurBlurBlur)
 
[![Blow](https://img.shields.io/badge/Blow-Game%20Logic-purple?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlowBlowBlow)

</div>

