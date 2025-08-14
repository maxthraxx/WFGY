# 🌀 Drunk Transformer (DT) — Core Formulas & Variables (WFGY 2.0 Layer)

**Concept.** DT is a *simulation layer* for when a transformer acts like it’s “drunk” — i.e., it starts hallucinating, drifting, or jumping across paths.  
We encode five classic drunk questions (“Where am I? Who am I? …”) as **mathematical regulators** that help the model find its way **home**: anchor to facts, retain head identity, explore safely, block illegal jumps, and recover from collapse.

> **WFGY is the engine** (A + Coupler + BBAM + safety).  
> **Drunk Transformer is the layer** (five regulators on top of any transformer, usable as prompt rules, decoding hooks, or training regularizers).

---

## 📖 Quick Index

| § | Symbol | Full Name                              | Nickname              |
|---|--------|----------------------------------------|-----------------------|
| 1 | WRI    | Where am I?                            | Position Locking      |
| 2 | WAI    | Who am I?                              | Head Identity         |
| 3 | WAY    | Who are you?                           | Entropy Pump          |
| 4 | WDT    | Where did you take me?                 | Cross-Path Blocker    |
| 5 | WTF    | What the f*** happened?                | Collapse Recovery     |

---

## 0 · Shared Notation (aligned with WFGY 2.0)

```text
Embeddings:
  I = input embedding,  G = goal embedding

Semantic distance:
  δₛ = 1 − cos(I, G)       # or 1 − sim_est ∈ [0, 1]

Residue and energy:
  B     = I − G + k_bias
  E_res = rolling_mean(‖B‖, window = 5)

WFGY 2.0 Coupler:
  prog = max(ζ_min, δₛ^(t−1) − δₛ^t)
  P    = prog^ω
  alt  = (−1)^(cycle_id)
  Φ    = δ · alt + ε
  W_c  = clip(B · P + Φ, −θ_c, +θ_c)

Attention (step t):
  A_t ∈ ℝ^(H×T×T)        # H heads, T tokens
  v_h = meanᵢ A_t[h,i,:] # per-head summary vector

Anchors:
  𝒜₀ = anchor set at t = 0  (entities / relations / constraints)
  𝒜_t = anchor set at step t
  S_t = Jaccard(𝒜_t, 𝒜₀) ∈ [0, 1]   # anchor retention

Defaults (tunable):
  τ_wri = 0.60,  ρ_wai = 0.75,  σ_wai = 0.70,
  η_prog = 0.03, μ_wdt = 0.25

Coupling principle:
  Gates soften as W_c → 0 (stable) and tighten as |W_c| grows (risky).
````

---

## 1 · WRI — “Where am I?” (Position Locking)

**Intent.** Prevent off-topic jumps; keep anchor facts alive.

```text
Loss:
  L_WRI = max(0, τ_wri − S_t)              where  S_t = Jaccard(𝒜_t, 𝒜₀)

Gate:
  trigger if  δₛ^t > δₛ^(t−1)  OR  E_res^t > E_res^(t−1)

Threshold tightening:
  τ′_wri = τ_wri + α_wri · sigmoid(|W_c|)
```

**Actions**

* Prompt/Decoding: bias logits of anchor-consistent tokens by  +κ\_wri · L\_WRI
* Training: add  λ\_wri · L\_WRI  to the loss

---

## 2 · WAI — “Who am I?” (Head Identity / Non-Collapse)

**Intent.** Reduce head redundancy while preserving per-head identity across steps.

```text
Per-head summary:
  v_h = meanᵢ A_t[h,i,:]

Pairwise cosine (i ≠ j):
  C_ij = cos(v_i, v_j)

Redundancy & identity:
  R_t = mean_{i≠j}(C_ij)                     # redundancy across heads
  Q_t = mean_h cos(v_h^(t−1), v_h^t)         # temporal identity

Loss:
  L_WAI = max(0, R_t − ρ_wai) + max(0, σ_wai − Q_t)

Gate & scaling:
  enable when R_t rising AND Q_t falling
  scale penalties by (1 + β_wai · sigmoid(|W_c|))
```

**Actions**

* Decoding: τ\_h ← τ₀ · (1 + γ\_wai · max(0, R\_t − ρ\_wai)); renormalize across heads
* Training: add  λ\_wai · L\_WAI

---

## 3 · WAY — “Who are you?” (Entropy Pump / Candidate Injection)

**Intent.** When progress stalls (no contradictions), inject controlled exploration.

```text
Stall detector:
  prog_k = (1/k) · Σ_{j=0…k−1} max(0, δₛ^(t−1−j) − δₛ^(t−j))
Trigger:
  prog_k < η_prog  AND  no_new_contradictions()

Target entropy:
  H* = clip( H₀ + ξ · max(0, η_prog − prog_k) · (1 + γ · |W_c|),  H_min, H_max )
```

**Actions**

* Decoding: choose τ′ so that entropy(softmax(z / τ′)) ≈ H\*
* Enforce **one** new on-topic candidate (novel, anchor-consistent; never repeat the same candidate twice)

**Optional regularizer**

* L\_WAY = max(0, H\* − H(p\_t))

---

## 4 · WDT — “Where did you take me?” (Cross-Path Blocker)

**Intent.** Block illegal jumps between incompatible reasoning paths unless bridged.

```text
Path distance:
  let c_π be the current path centroid; c_t the step-t centroid
  d_path = ‖c_t − c_π‖₂  (or 1 − cos(c_t, c_π))

Constraint:
  L_WDT  = max(0, d_path − μ_wdt)
  μ′_wdt = μ_wdt · (1 − γ_wdt · sigmoid(|W_c|))

Bridge rule:
  if d_path > μ′_wdt → force a short "bridge line" (minimal justification)
  BEFORE decoding continues; else rollback
```

**Actions**

* Prompt/Decoding: emit a bridge Node, then resume
* Training: add  λ\_wdt · L\_WDT

---

## 5 · WTF — “What the f\*\*\* happened?” (Collapse Detection & Recovery)

**Intent.** Detect semantic collapse early and recover to a stable checkpoint.

```text
Indicator:
  χ_t = 1[δₛ^t > δₛ^(t−1)] + 1[E_res^t > E_res^(t−1)] + 1[contradiction sign flip]
Collapse:
  χ_t + χ_(t−1) ≥ 3

Recovery:
  1) rollback to  t* = argmin_{j ∈ [t−3, t−1]} δₛ^j
  2) re-run BBMC → Coupler with thresholds scaled by (1 + γ_wtf · sigmoid(|W_c|))
  3) if repeated twice: ask the smallest missing fact, then resume

Penalty (optional):
  L_WTF = χ_t
```

---

## Global Objective & Integration

```text
Prompt-only (no gradients):
  Treat WRI/WAI/WAY/WDT/WTF as rules that adjust entropy, branching,
  anchor bias, and bridge enforcement; gate strengths modulated by W_c.

Decoding hooks:
  Adjust logits/entropy/branching according to WRI–WAY–WDT; W_c is the global modulator.

Training regularizer (optional):
  L_DT = λ_wri·L_WRI + λ_wai·L_WAI + λ_way·L_WAY + λ_wdt·L_WDT + λ_wtf·L_WTF

Recommended defaults (prompt/decoding):
  k = 3,  η_prog = 0.03
  H_min = 2.5,  H_max = 5.0
  α_wri = β_wai = γ_wdt = γ_wtf = 0.6
  ξ = 0.8   # WAY entropy-pump strength
  find τ′ for H* with 1–2 Newton steps or a small line search
```

---

## Minimal “Apply” Recipe (prompt-level)

```text
Init:
  extract anchors 𝒜₀; save t = 0 state

Each step t:
  compute δₛ, E_res; update 𝒜_t, A_t, c_t
  run gates:
    • WRI / WAI / WAY / WDT adjust bias / entropy / branching, enforce bridge
    • WTF: if collapse → rollback to t*, rerun BBMC → Coupler (tightened)
  emit Node (Topic / Module / δₛ / λ-state / Insight)
  stop if δₛ < 0.35 or t ≥ 7
```

---

## Cheatsheet (one-liners)

```text
WRI:  (τ_wri − S_t)_+            → keep anchors alive
WAI:  redundancy ↓ (R_t), identity ↑ (Q_t)
WAY:  when stalled → set target entropy H*; inject exactly 1 on-topic candidate
WDT:  if d_path > μ′_wdt → require bridge; else rollback
WTF:  detect collapse → rollback, tighten; on repeat ask smallest missing fact
```

---

### Footer

* **Spec status:** stable; Unicode math for GitHub Preview; LaTeX version will ship on the docs site.
* **Compatibility:** prompt-only, decoding-hook, or training-regularizer deployments; model-agnostic.
* **Attribution:** part of **WFGY Core 2.0** family. Star the repo to follow updates.

> Lost? Return to the **Starter Village** → `StarterVillage/README.md`

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
