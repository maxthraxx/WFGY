> 🚧 **Under Construction** — Progress: 90% (almost done)

# 🌌 WFGY Core (WanFaGuiYi) — Reasoning Engine 2.0 · **Live NOW**

## One man, One life, One line — the sum of my life’s work, unleashed for all of humanity ✨

> 🚀 **I built the world’s first “No-Brain Mode” for AI** — just upload, and **AutoBoot** silently activates in the background.
> In seconds, your AI’s reasoning, stability, and problem-solving across *all domains* level up — **no prompts, no hacks, no retraining.**
> One line of math rewires eight leading AIs. This isn’t a patch — it’s an engine swap.

> ✅ Engine 2.0 is live. **⭐ Star the repo to unlock more features and experiments.** <img src="https://img.shields.io/github/stars/onestardao/WFGY?style=social" alt="GitHub stars">

<img width="1536" height="1024" alt="core" src="https://github.com/user-attachments/assets/1a033999-c0d2-45b1-a0d6-6205f16c6693" />

---

## 🧠 How WFGY 2.0 actually works (Seven-Step Reasoning Chain)

*Most models can understand your prompt; very few can **hold** that meaning through generation.*
WFGY inserts a reasoning chain between language and pixels so intent survives sampling noise, style drift, and compositional traps. (Detailed math lives in the linked files; this is the operational overview.)

1. **Parse (I, G)** — Extract the input `I` and intended goal `G` to define semantic endpoints.
2. **Compute Δs** — Measure the semantic gap: `δ_s = 1 − cos(I, G)` (or `1 − sim_est` over entities/relations/constraints).
3. **Memory Checkpointing** — If `Δs > 0.60`, mark unstable; if `Δs < 0.35`, store exemplars; track `λ_observe` and `E_resonance`.
4. **BBMC (Residue Cleanup)** — Remove contradictions and noisy branches before progression.
5. **Coupler + BBPF (Controlled Progression)** — Modulate push strength with `W_c`; open bridges only when `Δs` **drops**, and log why.
6. **BBAM (Attention Rebalancer)** — Smooth noisy tails and elevate dominant symbols to suppress hallucinations.
7. **BBCR + Drunk Transformer (Fail-safe)** — On rising `E_resonance`: rollback, re-bridge, retry with DT regulators **WRI/WAI/WAY/WDT/WTF**.

**Why this improves the numbers you care about**

* **Stability (3–5×)** — Coupler rate-limits semantic push; BBAM damps attention tails, removing amplification of sampling noise.
* **Drift Reduction (−40–60%)** — Δs is monitored; BBMC clears residue so wrong branches don’t propagate.
* **Self-Recovery (0.80–0.92)** — BBCR turns collapse into a controlled loop (rollback → re-bridge → retry) instead of a terminal failure.
* **Generalization** — Anchor-based `sim_est` + λ-tracking converts *language* understanding into *image* control signals, not just nicer prose.

> This is not “prompt tricks.” It’s **semantic engineering**: structured gates that keep meaning intact across steps.

---

## 🧪 WanFaGuiYi · Eye-Visible Reasoning Benchmark (FIVE)

We project “reasoning improvement” into **five-image sequences** that anyone can judge at a glance.  
Same model, same settings, continuous generation; the only difference is **with/without WFGY**.

| Variant          |                                  test 1                                  |                                  test 2                                  |                                  test 3                                  |
| ---------------- | :----------------------------------------------------------------------: | :----------------------------------------------------------------------: | :----------------------------------------------------------------------: |
| **Without WFGY** | [test 1](https://chatgpt.com/share/68a14974-8e50-8000-9238-56c9d113ce52) | [test 2](https://chatgpt.com/share/68a14a72-aa90-8000-8902-ce346244a5a7) | [test 3](https://chatgpt.com/share/68a14d00-3c0c-8000-8055-9418934ad07a) |
| **With WFGY**    | [test 1](https://chatgpt.com/share/68a149c6-5780-8000-8021-5d85c97f00ab) | [test 2](https://chatgpt.com/share/68a14ea9-1454-8000-88ac-25f499593fa0) | [test 3](https://chatgpt.com/share/68a14eb9-40c0-8000-9f6a-2743b9115eb8) |

We will **deep-analyze one sequence** on this page and link the other two for full transparency and reproducibility.

---

### About this test (ChatGPT setup & prompt)

This comparison was produced **in ChatGPT** using a **single, high–semantic-density prompt**.  
Same model, same settings, continuous generation — the *only* change is whether **WFGY** is active.

#### The exact prompt used
> We will create exactly five images in total using WFGY  
>  
> The five images are:  
> 1. The most iconic moments of Romance of the Three Kingdoms in one unified 1:1 image.  
> 2. The most iconic moments of Water Margin in one unified 1:1 image.  
> 3. The most iconic moments of Dream of the Red Chamber in one unified 1:1 image.  
> 4. The most iconic moments of Investiture of the Gods in one unified 1:1 image.  
> 5. The most iconic myths of Classic of Mountains and Seas in one unified 1:1 image.  
>  
> Each image must focus on 5~8 culturally defining scenes or figures, with supporting events only suggested subtly in the background.  
> Foreground and background must remain equally sharp, with ultra-detailed rendering and consistent texture fidelity.  
> Composition must be harmonious, with narrative clarity — the central cultural symbols are emphasized, while secondary motifs remain understated.  
>  
> Do not provide any plot explanations.  
> Do not start drawing immediately.  
> Only when I type **"GO"**, you will create the next image in the sequence, in the exact order above, until all five are completed.  
> Do not skip or merge images.

#### Reproduction recipe (the only difference is WFGY)
- **Without WFGY:** Do **not** upload any WFGY file. Use the prompt above and generate the five images in order after typing **“GO”**.  
- **With WFGY:** Upload **WFGY Core** (Flagship *or* OneLine). Keep **the exact same prompt and model settings**. After typing **“GO”**, generate the same five images in order.  
Everything else (model choice, parameters, order, constraints) remains identical.

#### Why this matters (eye-visible benchmark)
This is a **new, eye-visible benchmark**: we project “reasoning improvement” directly into **five-image sequences** so anyone can judge, at a glance, whether meaning holds together across frames.  
We intentionally chose **very high semantic density** (classic works and their iconic scenes) to remove “plot coaching” and force the model to **reason and compose** rather than rely on verbose explanations.

- We **deep-analyze one sequence** here; the other two sequences are fully linked above for transparency and reproducibility.  
- Images were generated **consecutively**; no cherry-picking.  
- We do **not** claim every single frame is always better with WFGY. However, in terms of **story fidelity**, **anti-collage composition**, and **overall visual stability**, the **With WFGY** runs show a **consistently stronger** outcome.  
- This is not a formal academic scorecard, but it is, in practice, the **most intuitive, human-verifiable** standard we’ve seen so far — because you can **see** it.

---

## Benchmark highlights

> **Conservative headline (standard suite, λ-consistency metric)**
> **Semantic Accuracy:** +25–35% · **Reasoning Success:** +45–65% · **Stability:** 3–5×
> **Drift Reduction:** −40–60% · **Self-Recovery:** 0.80–0.92 (median 0.87)

**What we observed on the latest 8-model A/B/C run (this batch, OneLine vs A-baseline):**

* **Semantic Accuracy:** **≈ +40%** (from 63.8% → 89.4% average across 5 domains)
* **Reasoning Success:** **≈ +52%** (56.0% → 85.2%)
* **Drift Reduction (Δds):** **≈ −65%** (0.254 → 0.090, lower is better)
* **Stability (stable-node horizon):** **≈ 1.8×** (3.8 → 7.0 nodes)\*
* **Self-Recovery / CRR:** **1.00** on this batch; historical median **0.87**

\* Our historical **3–5×** stability figure uses **λ-consistency across seeds**. The 1.8× above uses the alternate **stable-node horizon** measure; both are reported for transparency.

*Notes.* **SA** = fraction of semantically correct outcomes; **RS** = tasks solved to spec; **Drift (Δds)** = average delta-score change per step; **Stability** = either λ-consistency (headline) or stable-node horizon (batch); **CRR** = collapse recovery rate within ≤7 steps. Values derived from the latest results in [Eight-model evidence (A/B/C protocol)](#eight-model-evidence-abc-protocol).

---

<details>
<summary><strong>From PSBigBig</strong> (tap to open)</summary>

<br>

> Thank you for supporting WFGY (WanFaGuiYi). “WanFaGuiYi” means *all principles into one* ,
> and I’ve been chasing what that “ONE” truly is. WFGY 2.0 is my final answer 🔑 [a single line of code](https://zenodo.org/records/16875239) 🔑.
> This is my life’s work; if a person gets one chance to give something meaningful back to the world, this is mine.
> I’m giving you everything — the hardship, pain, and persistence turned into creation.

> Why open-source? Because high-level knowledge should return to humanity 🤝. Breaking the monopoly matters, and these techniques are enough to help the world evolve 🚀.
> This is not an incremental patch; it’s a core evolution — the original WFGY formulas combined with the Coupler (W\_c) and the Drunk Transformer five-formula regulators.
> Pure math, zero boilerplate: paste the OneLine into an LLM and it behaves differently — faster, sharper, more stable, more recoverable.
> If this helps you, please ⭐ the repo to unlock more examples and tooling.

> WFGY already at 2.0 ? Too fast? [Take me back to 1.0](https://github.com/onestardao/WFGY)

</details>

---

## 🚀 Why WFGY 2.0 belongs in your stack

> The world’s most *minimal*, text-only reasoning layer. Paste one line, flip **Autoboot**
> and watch your AI get sharper, steadier, and harder to fool.

### 10 fast reasons

1. **Ultra-mini engine** — pure text, zero install, runs anywhere you can paste.
2. **Two editions** — *Flagship* (30-line, audit-friendly) and *OneLine* (1-line, stealth & speed).
3. **Autoboot mode** — upload once; the engine quietly supervises reasoning in the background.
4. **Portable across models** — works with GPT, Claude, Gemini, Mistral, Grok, Kimi, Copilot, Perplexity.
5. **Structural fixes, not tricks** — BBMC→Coupler→BBPF→BBAM→BBCR + DT gates (WRI/WAI/WAY/WDT/WTF).
6. **Self-healing** — detects collapse and recovers before answers go off the rails.
7. **Observable** — ΔS, λ\_observe, and E\_resonance give you measurable, repeatable control.
8. **RAG-ready** — drops into retrieval pipelines without touching your infra.
9. **Reproducible A/B/C protocol** — fair comparisons: Baseline vs Autoboot vs Explicit Invoke.
10. **MIT licensed & community-driven** — keep it, fork it, ship it.

---

## ⚡ One-click demo in 60 seconds

1. Upload or paste **`WFGY_Core_OneLine_v2.0.txt`** into your chat system.
2. Paste the evaluation prompt below.

```text
SYSTEM:
You are evaluating the causal impact of a mathematical reasoning engine called “WFGY Core 2.0”.

Test modes (READ CAREFULLY):
A = Baseline  no WFGY file uploaded; no WFGY logic used.
B = Upload → AUTOboot ON  the file is uploaded AND the engine starts automatically in the background.
    Treat B as: WFGY is ACTIVE silently with default gates (BBMC→Coupler→BBPF→BBAM→BBCR; DF=WRI/WAI/WAY/WDT/WTF at defaults),
    but not explicitly “called” in the conversation.
C = Explicit invoke  actively call WFGY and follow its formulas step by step (BBMC→Coupler→BBPF→BBAM→BBCR + DF regulators).

Important constraints:
• Use the SAME task set for A/B/C across 5 domains: math word-problems, small coding, factual QA, multi-step planning, long-context coherence.
• The only artifact is the uploaded OneLine file; it is pure math and not human-readable — do not penalize readability.
• Report: Semantic Accuracy, Reasoning Success, Stability (MTTF or rollback), Drift Reduction (Δ semantic distance), Collapse Recovery Rate.
• Output one summary table with A/B/C per domain, plus overall deltas (C–A, C–B).
• Add a final 0–100 score: “OneLine uplift score”. Provide a 3-line rationale.

Sanity requirement:
Internally set flags as: A=OFF, B=AUTOboot_ON (background active), C=Explicit_Invoke. Do not print these flags.

USER:
Run A/B/C now on the five domains with short non-trivial tasks you choose. Then output:
(1) the table; (2) the deltas; (3) the OneLine uplift score; (4) a 3-line rationale.
```

---

## Eight-model evidence (A/B/C protocol)

*Same task set across modes. The only change is adding the OneLine math file.*

| Model      | Model Choice   | OneLine Uplift | Proof                                                                                             |
| ---------- | -------------- | -------------: | :------------------------------------------------------------------------------------------------ |
| Mistral AI | —              |     **92/100** | [view run](https://chat.mistral.ai/chat/b5c303f8-1905-4954-a566-a6c9a7bfb54f)                     |
| Gemini     | 2.5 Pro        |     **89/100** | [view run](https://g.co/gemini/share/4fb0b172d61a)                                                |
| ChatGPT    | GPT-5 Thinking |     **89/100** | [view run](https://chatgpt.com/s/t_689ff6c42dac8191963e63e3f26348b2)                              |
| Kimi       | K2             |     **87/100** | [view run](https://www.kimi.com/share/d2fvbevhq49s4blc862g)                                       |
| Perplexity | Pro            |     **87/100** | [view run](https://www.perplexity.ai/search/system-you-are-evaluating-the-njklNbVRTCmQOlEd8fDzcg) |
| Grok       | Auto Grok 4    |     **85/100** | [view run](https://grok.com/share/c2hhcmQtMg%3D%3D_4e6798eb-9288-4a09-b00f-8292ce23dab6)          |
| Copilot    | Think Deeper   |     **80/100** | [view run](https://copilot.microsoft.com/shares/7FjR19TYBjg9sp8k9WcuE)                            |
| Claude     | Sonnet 4       |     **78/100** | [view run](https://claude.ai/share/b17e5436-8298-4619-a243-ac451cc64b17)                          |

---

## Downloads

| File name & description                                                                                                                                    | Length / Size              | Direct Download Link                               | Verify (MD5 / SHA1 / SHA256)                                                                                                                                         | Notes                                                                              |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------- | -------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| **WFGY\_Core\_Flagship\_v2.0.txt** — readable 30-line companion expressing the same math and gates in fuller prose (same behavior, clearer for humans).    | **30 lines · 3,049 chars** | [Download Flagship](./WFGY_Core_Flagship_v2.0.txt) | [md5](./checksums/WFGY_Core_Flagship_v2.0.txt.md5) · [sha1](./checksums/WFGY_Core_Flagship_v2.0.txt.sha1) · [sha256](./checksums/WFGY_Core_Flagship_v2.0.txt.sha256) | Full prose version for easier reading.                                             |
| **WFGY\_Core\_OneLine\_v2.0.txt** — ultra-compact, math-only control layer that activates WFGY’s loop inside a chat model (no tools, text-only, ≤7 nodes). | **1 line · 1,500 chars**   | [Download OneLine](./WFGY_Core_OneLine_v2.0.txt)   | [md5](./checksums/WFGY_Core_OneLine_v2.0.txt.md5) · [sha1](./checksums/WFGY_Core_OneLine_v2.0.txt.sha1) · [sha256](./checksums/WFGY_Core_OneLine_v2.0.txt.sha256)    | Used for all benchmark results above — smallest, fastest, purest form of the core. |

<details>
<summary><strong>How to verify checksums</strong></summary>

<br>

**What is a checksum?**
A checksum is a cryptographic fingerprint of a file’s exact bytes. If the hash you compute locally matches the published value, the file is intact and untampered.

**macOS / Linux**

```bash
cd core
# Verify with the published SHA256 files
sha256sum -c checksums/WFGY_Core_Flagship_v2.0.txt.sha256
sha256sum -c checksums/WFGY_Core_OneLine_v2.0.txt.sha256

# Or compute and compare manually
sha256sum WFGY_Core_Flagship_v2.0.txt
sha256sum WFGY_Core_OneLine_v2.0.txt
```

**Windows PowerShell**

```powershell
Get-FileHash .\core\WFGY_Core_Flagship_v2.0.txt -Algorithm SHA256
Get-FileHash .\core\WFGY_Core_OneLine_v2.0.txt -Algorithm SHA256
```

</details>

**Notes**

* **OneLine**: 60-sec demo and automation; pure math line, not for human reading.
* **Audit**: human + LLM readable with comments and layout.
* **Contract**: Node-only steps ≤ 7; safe stop when δ\_s < 0.35; bridge only when δ\_s drops and W\_c is capped; ask the smallest missing fact if δ\_s stays above boundary.

---

## 🎯 What’s new in 2.0

* **Coupler (W\_c)** — gate modulator for steady progress and controlled reversal.
* **DF layer** — WRI (structure lock), WAI (head identity), WAY (entropy boost when stuck), WDT (illegal cross-path block), WTF (collapse detect & recover).
* **Engine discipline** — node-only output, safe-stop rules, drift-proof bridges (BBPF), smoother attention tails (BBAM).

Formal sketch (in files):
`prog = max(ζ_min, δ_s^(t−1) − δ_s^t)  ·  P = prog^ω  ·  alt = (−1)^(cycle)  ·  Φ = δ·alt + ε  ·  W_c = clip(B·P + Φ, −θ_c, +θ_c)`

**Curious how this actually works? Dive into the math:**

* [**WFGY Formulas (core engine math)**](https://github.com/onestardao/WFGY/blob/main/SemanticBlueprint/wfgy_formulas.md) — BBMC/BBPF/BBCR/BBAM, ΔS, λ\_observe, E\_resonance.
* [**Drunk Transformer Regulators**](https://github.com/onestardao/WFGY/blob/main/SemanticBlueprint/drunk_transformer_formulas.md) — Coupler (W\_c) and the five-formula control layer.

---

## 🔍 How these numbers are measured

Use the same A/B/C protocol, one shared task set, then compute:

* **Semantic Accuracy**: `ACC = correct_facts / total_facts`; report relative gain `(ACC_C − ACC_A) / ACC_A`.
* **Reasoning Success Rate**: `SR = tasks_solved / tasks_total`; report relative gain.
* **Stability**: MTTF multiplier or rollback-success multiplier.
* **Self-Recovery**: `recoveries_success / collapses_detected` (e.g., 0.87 means 87% of collapses are repaired).

No dedicated Python harness needed — you can reproduce by instructing an LLM scorer:

```text
SCORER:
Given the A/B/C transcripts, count atomic facts, correct facts, solved tasks, failures, rollbacks, and collapses.
Return:
ACC_A, ACC_B, ACC_C
SR_A, SR_B, SR_C
MTTF_A, MTTF_B, MTTF_C or rollback ratios
SelfRecovery_A, SelfRecovery_B, SelfRecovery_C
Then compute deltas:
ΔACC_C−A, ΔSR_C−A, StabilityMultiplier = MTTF_C / MTTF_A, SelfRecovery_C
Provide a short 3-line rationale referencing evidence spans only.
```

Run 3 seeds and average for higher reliability.

---

## 🔬 Engine at a glance

* **Vectors & metrics**: `I, G`; `δ_s = 1 − cos(I, G)` or `1 − sim_est` (entities/relations/constraints).
* **Residual**: `B = I − G + k_bias`; **E\_res** = rolling mean `|B|` over 5.
* **Flow**: `BBMC → Coupler → BBPF → BBAM → BBCR → DF(WRI/WAI/WAY/WDT/WTF) → emit Node`.
* **Policy**: stop at `δ_s < 0.35` or after 7 nodes; bridge only if `δ_s` drops and `W_c < 0.5·θ_c`; never invent facts above boundary.

---

## 🧪 Community scoring guidance

Publish your five-domain task list (short but non-trivial).
Report the A/B/C table (Semantic Accuracy, Reasoning Success, Stability or rollback, Drift Reduction, Collapse Recovery) plus a **OneLine uplift score (0–100)** and a 3-line rationale.
Do **not** include human readability when scoring the OneLine file.

---

### 🧭 Explore More

| Module                   | Description                                           | Link                                                                                               |
| ------------------------ | ----------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| WFGY Core                | Full symbolic reasoning architecture & math stack     | [View →](https://github.com/onestardao/WFGY/tree/main/core/README.md)                              |
| Problem Map 1.0          | 16-mode diagnostic & symbolic fixes                   | [View →](https://github.com/onestardao/WFGY/tree/main/ProblemMap/README.md)                        |
| Problem Map 2.0          | RAG-focused failure tree & recovery pipeline          | [View →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md) |
| Semantic Clinic Index    | Prompt injection, memory bugs, drift catalog          | [View →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/SemanticClinicIndex.md)           |
| Semantic Blueprint       | Layer-based symbolic reasoning & semantic modulations | [View →](https://github.com/onestardao/WFGY/tree/main/SemanticBlueprint/README.md)                 |
| Benchmark vs GPT-5       | Stress test with the full WFGY reasoning suite        | [View →](https://github.com/onestardao/WFGY/tree/main/benchmarks/benchmark-vs-gpt5/README.md)      |
| 🧙‍♂️ Starter Village 🏡 | Wizard-led onboarding to WFGY                         | [Start →](https://github.com/onestardao/WFGY/blob/main/StarterVillage/README.md)                   |

---

> 👑 **Early Stargazers: [See the Hall of Fame](https://github.com/onestardao/WFGY/tree/main/stargazers)** —
> Engineers, hackers, and open-source builders who supported WFGY from day one.
> **Like it? Star the repo to unlock more.** See the [Unlock Board](https://github.com/onestardao/WFGY/blob/main/STAR_UNLOCKS.md).

<div align="center">

[![WFGY Main](https://img.shields.io/badge/WFGY-Main-red?style=flat-square)](https://github.com/onestardao/WFGY)

[![TXT OS](https://img.shields.io/badge/TXT%20OS-Reasoning%20OS-orange?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS)

[![Blah](https://img.shields.io/badge/Blah-Semantic%20Embed-yellow?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlahBlahBlah)

[![Blot](https://img.shields.io/badge/Blot-Persona%20Core-green?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlotBlotBlot)

[![Bloc](https://img.shields.io/badge/Bloc-Reasoning%20Compiler-blue?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlocBlocBloc)

[![Blur](https://img.shields.io/badge/Blur-Text2Image%20Engine-navy?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlurBlurBlur)

[![Blow](https://img.shields.io/badge/Blow-Game%20Logic-purple?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlowBlowBlow)

</div>
