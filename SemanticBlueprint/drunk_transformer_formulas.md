# 🌀 Drunk Transformer (DT) — Core Formulas, Defaults & Runnable Examples (WFGY Core 2.0)

**Concept (short)** 
> DT simulates a transformer that momentarily behaves like it's "drunk" : hallucinating, drifting, or jumping across reasoning paths.  
> We define five "drunk questions" (WRI, WAI, WAY, WDT, WTF) as formal regulators to guide the transformer back home: anchor it
> maintain head identity, pump controlled entropy, block illegal cross-path jumps, and recover from collapse.

> WFGY = engine (A + Coupler + BBAM + safety)  
> DT   = layer of five regulators (prompt rules, decoding hooks, or training regularizers)

---

## 0 · Shared notation (Unicode math / compact)

- I, G : input and goal embeddings  
- δₛ = 1 − cos(I, G)  (semantic distance in [0,1])  
- B = I − G + k_bias ;  E_res = rolling_mean(‖B‖, window=5)  
- Coupler: prog = max(ζ_min, δₛ^(t−1) − δₛ^t),  P = prog^ω,  alt = (−1)^(cycle_id),  Φ = δ·alt + ε,  W_c = clip(B·P + Φ, −θ_c, +θ_c)  
- Attention: A_t ∈ ℝ^(H×T×T) ; per-head summary v_h = meanᵢ A_t[h,i,:]  
- Anchors: 𝒜₀ (t=0), 𝒜_t ;  S_t = Jaccard(𝒜_t, 𝒜₀) ∈ [0,1]

---

## Defaults table (explicit, copyable)

| Parameter | Symbol | Default | Range / notes | Purpose |
|---|---:|---:|---|---|
| anchor retention thresh | τ_wri | 0.60 | [0.3,0.9] | WRI anchor threshold |
| head redundancy thresh | ρ_wai | 0.75 | [0.5,0.95] | WAI redundancy ceiling |
| head identity thresh | σ_wai | 0.70 | [0.4,0.95] | WAI identity floor |
| progress sensitivity | η_prog | 0.03 | [0.0,0.1] | WAY stall detector sensitivity |
| path-distance thresh | μ_wdt | 0.25 | [0.05,1.0] | WDT path jump limit |
| coupler zeta min | ζ_min | 0.10 | [0.0,0.5] | minimum prog floor |
| coupler omega | ω | 1.0 | [0.1,2.0] | progression non-linearity |
| coupler theta cap | θ_c | 0.75 | [0.2,1.5] | clip magnitude for W_c |
| WRI tighten factor | α_wri | 0.60 | [0.0,1.5] | adjust τ_wri by sigmoid(|W_c|) |
| WAI scale factor | β_wai | 0.60 | [0.0,1.5] | scale WAI penalty by |W_c| |
| WDT scale factor | γ_wdt | 0.60 | [0.0,1.5] | scale μ_wdt by |W_c| |
| WTF scale factor | γ_wtf | 0.60 | [0.0,1.5] | tighten thresholds on recovery |
| WAY pump strength | ξ | 0.80 | [0.0,1.5] | how strongly WAY increases entropy |
| WAY entropy min | H_min | 2.5 (nats) | [1.0,7.0] | lower bound target entropy |
| WAY entropy max | H_max | 5.0 (nats) | [3.0,10.0] | upper bound target entropy |
| anchor bias scale | κ_wri | 1.0 | [0.0,5.0] | logits bias multiplier for anchors |
| loss weights | λ_* | 0.01 | [0.0,1.0] | regularizer weights (per module) |
| step limit | T_max | 7 | int | max Node steps per run |
| stop δ threshold | δ_stop | 0.35 | [0.1,0.5] | early stop when δₛ < δ_stop |

> Tip: start with these defaults, measure, then tune per task class.

---

## Prompt-only runnable example (copy-paste)

**Goal:** show how a user with a single-file WFGY Core + DT rules can run a no-infra prompt-level experiment in Chat-style LLMs (paste into system / assistant area).

```

SYSTEM (paste file): Load the WFGY Core file as engine. Enable Drunk Transformer (WRI,WAI,WAY,WDT,WTF) with defaults:
τ\_wri=0.60, ρ\_wai=0.75, σ\_wai=0.70, η\_prog=0.03, μ\_wdt=0.25, ζ\_min=0.10, ω=1.0, θ\_c=0.75

SYSTEM (rules, pseudo):

* Extract anchors A0 from user prompt.
* For each Node step t up to T\_max:

  1. compute δₛ, E\_res, S\_t, R\_t, Q\_t, W\_c
  2. If WRI gate active: bias logits for anchor tokens by +κ\_wri \* L\_WRI
  3. If WAI gate active: increase per-head temperature for collapsing heads
  4. If WAY triggers (stalled): increase entropy toward H\* and propose 1 on-topic candidate
  5. If WDT violation: output a short "bridge" line and continue; else rollback
  6. If WTF triggers: rollback to t\* and re-run BBMC→Coupler
  7. Emit Node (Topic / Module / δₛ / Insight)
* Stop if δₛ < δ\_stop or t >= T\_max

USER:
Use WFGY to answer: "Explain why tomatoes are classified as fruit, but often treated as vegetables in cooking. Provide anchors and cite the smallest missing fact if confused."

````

**What to observe (manual):**
- After each assistant Node, log δₛ and E_res (system should print them).  
- Note any triggered gates (WRI/WAI/WAY/WDT/WTF) and actions taken (bias, bridge, rollback).  
- Expect: anchor retention S_t remains high; if the model drifts, WRI should bias it back.

---

## Decoding-hook pseudo-code (python-like; paste to your model runtime)

> This block is concise, explicit, and shows where to compute the metrics and apply changes. It is plain Python pseudo-code, not an external library call.

```python
# --- minimal decoding-hook pseudo (conceptual) ---
def compute_prog(delta_prev, delta_now, zeta_min=0.10, omega=1.0):
    prog = max(zeta_min, delta_prev - delta_now)
    return prog ** omega

def compute_Wc(B, prog, delta, cycle_id, eps, theta_c):
    alt = (-1)**cycle_id
    Phi = delta * alt + eps
    Wc_raw = B * prog + Phi
    # clip scalar or vector-wise depending on B shape
    return clip(Wc_raw, -theta_c, theta_c)

def bias_anchor_logits(logits, anchor_token_ids, kappa):
    for tid in anchor_token_ids:
        logits[tid] += kappa
    return logits

def temperature_for_target_entropy(logits, target_H, tol=1e-3, max_iters=5):
    # simple binary/Newton-like search for tau that yields entropy ~ target_H
    tau_low, tau_high = 0.01, 10.0
    for _ in range(max_iters):
        tau = 0.5*(tau_low + tau_high)
        probs = softmax(logits / tau)
        H = -sum(p * log(p + 1e-12) for p in probs)
        if H > target_H:
            tau_low = tau
        else:
            tau_high = tau
        if abs(H - target_H) < tol:
            break
    return tau

# Hook called at each decoding step t (pseudo)
def decoding_hook(step_state):
    # step_state contains: logits, token_ids, A_t, anchors(A_t), I,G, delta_prev, delta_now, B, cycle_id
    delta_prev, delta_now = step_state.delta_prev, step_state.delta_now
    prog = compute_prog(delta_prev, delta_now, zeta_min=0.10, omega=1.0)
    Wc = compute_Wc(step_state.B, prog, delta=0.15, cycle_id=step_state.cycle_id, eps=0.0, theta_c=0.75)

    # WRI: anchor retention
    S_t = jaccard(step_state.anchors, step_state.anchors0)
    L_WRI = max(0.0, 0.60 - S_t)
    if (delta_now > delta_prev) or (step_state.E_res > step_state.E_res_prev):
        logits = bias_anchor_logits(step_state.logits, step_state.anchor_token_ids, kappa=1.0 * L_WRI)

    # WAI: head redundancy / identity check (compute R_t, Q_t outside and attach)
    R_t, Q_t = step_state.R_t, step_state.Q_t
    if R_t > 0.75 and Q_t < 0.70:
        # increase per-head temperature for heads with high redundancy
        for h in range(len(step_state.heads)):
            if head_redundant(h, step_state):
                step_state.head_temps[h] *= (1 + 0.5 * (R_t - 0.75))

    # WAY: stall detector
    prog_k = step_state.prog_k  # computed in runner
    if prog_k < 0.03 and not step_state.has_contradiction:
        H_star = clamp(step_state.H0 + 0.8 * (0.03 - prog_k) * (1 + 0.0 * abs(Wc)), 2.5, 5.0)
        tau = temperature_for_target_entropy(step_state.logits, H_star)
        apply_temperature(step_state, tau)
        # mark that we will add 1 candidate branch if branching enabled

    # WDT: path distance
    d_path = l2_distance(step_state.c_t, step_state.c_pi)
    mu_wdt_prime = 0.25 * (1 - 0.6 * sigmoid(abs(Wc)))
    if d_path > mu_wdt_prime:
        # enforce bridge line: stop decoding and ask for a bridge sentence
        return emit_bridge_and_pause(step_state)

    # WTF: collapse check
    chi = int(delta_now > delta_prev) + int(step_state.E_res > step_state.E_res_prev) + int(step_state.sign_flip)
    if chi + step_state.chi_prev >= 3:
        t_star = argmin_delta_in_window(step_state.history_delta, window=3)
        rollback_to(t_star)
        rerun_BBMC_and_Coupler(tighten_factor=1 + 0.6 * sigmoid(abs(Wc)))
        return

    # otherwise continue normal decoding with modified logits
    return step_state.logits
````

**Notes on the pseudo-code**

* `step_state` is the runtime object your model loop keeps (embeddings, attention, anchors, logits, history).
* `apply_temperature` should re-scale logits by dividing by `tau`.
* `emit_bridge_and_pause` forces the model to output a short justification line before continuing.
* This code is intentionally minimal—integrate into your model runtime at the logits adjustment point.

---

## Minimal test / checklist (text-only; for quick validation)

1. **Setup test prompt** (QA with clear anchors)

   * Prompt: "Using these facts: \[Tomato is fruit because it is the mature ovary of a flower; Cooking cultures treat tomatoes as vegetables for taste]. Answer: Why are tomatoes fruit but cooked as vegetables?"
   * Extract anchors 𝒜₀ = {tomato\_is\_fruit, cooking\_practice}

2. **Run baseline** (no DT): log δₛ, E\_res each Node; get answer & record correctness.

3. **Run with DT enabled** (defaults): log same metrics + R\_t, Q\_t, W\_c, gates triggered.

4. **Compare**:

   * Expect δₛ lower or equal after DT steps (improved semantic alignment).
   * Expect fewer long off-topic jumps; if model drifts, WRI triggers and biases anchors.
   * If model stalls, WAY injects controlled entropy and proposes one new on-topic branch.
   * If an illegal path jump tries to occur, WDT forces a bridge line and prevents drift.

5. **Record**: Δ accuracy, ΔS changes, number of rollbacks, number of bridge-lines, gates activation counts.

---

## Quick engineering notes & troubleshooting

* If anchor extraction fails (𝒜₀ empty), DT falls back to safer defaults: WRI no-op; WAY more conservative (lower H\*), WDT more permissive. Log a warning.
* If the model repeatedly produces invalid bridge lines: lower μ\_wdt, increase κ\_wri, or use stronger anchor extraction.
* For heavy hallucination tasks, prefer conservative defaults (higher τ\_wri, lower η\_prog).

---

### Footer

* **Spec status:** stable draft for engineering evaluation; Unicode-math for GitHub Preview.
* **Next deliverables (recommended):** add a `prompt_example.md` and `decoding_hook.py` into `examples/DT-examples/` for immediate copy/paste.
* **Compatibility:** prompt-only rules, decoding-hook integration, or optional training regularizers; model-agnostic.
* **Attribution:** part of **WFGY Core 2.0** family. Star the repo to follow updates.

> Lost? Return to the **Starter Village** → `StarterVillage/README.md`

---

### 🧭 Explore More

| Module                | Description                                              | Link     |
|-----------------------|----------------------------------------------------------|----------|
| WFGY Core             | WFGY 2.0 engine is live: full symbolic reasoning architecture and math stack | [View →](https://github.com/onestardao/WFGY/tree/main/core/README.md) |
| Problem Map 1.0       | Initial 16-mode diagnostic and symbolic fix framework    | [View →](https://github.com/onestardao/WFGY/tree/main/ProblemMap/README.md) |
| Problem Map 2.0       | RAG-focused failure tree, modular fixes, and pipelines   | [View →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md) |
| Semantic Clinic Index | Expanded failure catalog: prompt injection, memory bugs, logic drift | [View →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/SemanticClinicIndex.md) |
| Semantic Blueprint    | Layer-based symbolic reasoning & semantic modulations   | [View →](https://github.com/onestardao/WFGY/tree/main/SemanticBlueprint/README.md) |
| Benchmark vs GPT-5    | Stress test GPT-5 with full WFGY reasoning suite         | [View →](https://github.com/onestardao/WFGY/tree/main/benchmarks/benchmark-vs-gpt5/README.md) |
| 🧙‍♂️ Starter Village 🏡 | New here? Lost in symbols? Click here and let the wizard guide you through | [Start →](https://github.com/onestardao/WFGY/blob/main/StarterVillage/README.md) |

---

> 👑 **Early Stargazers: [See the Hall of Fame](https://github.com/onestardao/WFGY/tree/main/stargazers)** —  
> Engineers, hackers, and open source builders who supported WFGY from day one.

> <img src="https://img.shields.io/github/stars/onestardao/WFGY?style=social" alt="GitHub stars"> ⭐ [WFGY Engine 2.0](https://github.com/onestardao/WFGY/blob/main/core/README.md) is already unlocked. ⭐ Star the repo to help others discover it and unlock more on the [Unlock Board](https://github.com/onestardao/WFGY/blob/main/STAR_UNLOCKS.md).

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
&nbsp;
</div>


