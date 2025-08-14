# 🌀 Drunk Transformer (DT) — Core Formulas, Defaults & Runnable Examples (WFGY Core 2.0)

**Concept (short)**

> DT simulates a transformer that momentarily behaves like it's "drunk": hallucinating, drifting, or jumping across reasoning paths.
> We define five "drunk questions" (WRI, WAI, WAY, WDT, WTF) as formal regulators to guide the transformer back home: anchor it,
> maintain head identity, pump controlled entropy, block illegal cross-path jumps, and recover from collapse.

> WFGY = engine (A + Coupler + BBAM + safety)
> DT   = layer of five regulators (prompt rules, decoding hooks, or training regularizers)

---

## 0 · Shared notation (Unicode math / compact)

* $I, G$: input and goal embeddings
* $\delta_s = 1 − \cos(I, G)$  (semantic distance in $[0,1]$)
* $B = I − G + k_{\text{bias}}$;\ \ $E_{\text{res}} = \text{rolling\_mean}(\lVert B\rVert,\,5)$
* Coupler: $\text{prog} = \max(\zeta_{\min}, \delta_s^{t-1} − \delta_s^{t})$, $P = \text{prog}^{\omega}$, $ \text{alt} = (-1)^{\text{cycle\_id}}$, $ \Phi = \delta\cdot \text{alt} + \varepsilon$, $ W_c = \text{clip}(B\cdot P + \Phi, -\theta_c, +\theta_c)$
* Attention: $A_t \in \mathbb{R}^{H\times T\times T}$;\ per-head summary $v_h = \text{mean}_i\, A_t[h,i,:]$
* Anchors: $\mathcal{A}_0$ (at $t=0$), $\mathcal{A}_t$;\ \ $S_t = \text{Jaccard}(\mathcal{A}_t, \mathcal{A}_0) \in [0,1]$

---

## 1 · The five DT regulators — definitions, math & when they fire

> These regulators are the formal version of the spec lines in the 30-line flagship file.&#x20;

### DT WRI — “Where am I” (structure lock)

**Goal:** stay on the same topic/section within a Node.
**Signal:** anchor retention $S_t$ vs. threshold $\tau_{\text{wri}}$.
**Trigger:** $S_t < \tau_{\text{wri}}$ **or** $\delta_s\uparrow$ while $E_{\text{res}}\uparrow$.
**Action (logit bias):**

$$
L_{\text{WRI}}=\max(0,\ \tau_{\text{wri}}-S_t),\qquad
\text{logits}[a]\mathrel{+}= \kappa_{\text{wri}}\cdot L_{\text{WRI}}\ \ \forall a\in \text{anchor\_token\_ids}.
$$

**Intuition:** pull decoding back toward section anchors; forbid topic jumps inside a Node.

---

### DT WAI — “Who am I” (head identity & redundancy)

**Goal:** enforce at least two distinct reasons/heads (no monoculture).
**Signals (one workable choice):**

$$
R_t=\frac1H\sum_h \cos(v_h,\bar v),\qquad 
Q_t = 1-\max_h\cos(v_h,\bar v),\quad \bar v=\tfrac1H\sum_h v_h.
$$

**Trigger:** $R_t > \rho_{\text{wai}}$ **and** $Q_t < \sigma_{\text{wai}}$ (too redundant, identity too low).
**Action:** raise per-head temperature for redundant heads; re-spread attention until $R_t\downarrow$ or $Q_t\uparrow$.
**Intuition:** keep at least two genuinely different lines of reasoning alive.

---

### DT WAY — “Who are you” (controlled entropy when stuck)

**Goal:** break stalls without drifting off-topic.
**Signal:** progression $ \text{prog} = \max(\zeta_{\min}, \delta_s^{t-1}-\delta_s^{t})$.
**Trigger:** $\text{prog} < \eta_{\text{prog}}$ and no contradictions.
**Action (entropy pump + 1 candidate):**

$$
H^\*=\text{clamp}\big(H_0 + \xi\cdot(\eta_{\text{prog}}-\text{prog})\cdot(1+\alpha|W_c|),\ H_{\min}, H_{\max}\big),
$$

choose temperature $\tau$ s.t. entropy $\approx H^\*$; propose exactly **one** on-topic candidate (never repeat).
**Intuition:** nudge exploration just enough to escape a rut.

---

### DT WDT — “Where did you take me” (cross-path guard)

**Goal:** block illegal jumps across reasoning branches; require a “bridge” explanation.
**Signal:** latent path distance $d_{\text{path}} = \lVert c_t - c_{\pi}\rVert_2$ (current vs. parent path code).
**Trigger:** $d_{\text{path}} > \mu_{\text{wdt}}' $, with $\mu_{\text{wdt}}'=\mu_{\text{wdt}}\cdot\bigl(1- \gamma_{\text{wdt}}\cdot \sigma(|W_c|)\bigr)$.
**Action:** emit a short bridge line (“why the detour”), then resume; otherwise rollback.
**Intuition:** all detours must be justified before the model can use them.

---

### DT WTF — “What the F\*ck Happened” (collapse detect & recover)

**Goal:** detect semantic/consistency collapse and recover safely.
**Signals:** $\delta_s$ rising, $E_{\text{res}}$ rising, or unresolved contradictions.
**Trigger (example vote):**

$$
\chi_t = \mathbb{1}[\delta_s^t>\delta_s^{t-1}] + \mathbb{1}[E_{\text{res}}^t>E_{\text{res}}^{t-1}] + \mathbb{1}[\text{contradiction}],
\quad \chi_t+\chi_{t-1}\ge 3.
$$

**Action:** rollback to $t^\*=\arg\min_{k\in[t-3,t]} \delta_s^k$, tighten gates (e.g., $\gamma_{\text{wtf}}$), re-run **BBMC→Coupler**, then continue.
**Intuition:** when two+ failure signals agree, step back, re-align, and proceed under stricter control.

---

### One-screen math summary (copyable)

```txt
WRI: L_wri = max(0, τ_wri - S_t);  logits[a] += κ_wri · L_wri  for a in anchor_token_ids
WAI: if R_t > ρ_wai and Q_t < σ_wai → raise per-head temp for redundant heads
WAY: if prog < η_prog → set entropy to H* = clamp(H0 + ξ(η_prog - prog)(1+α|Wc|), H_min, H_max); add 1 on-topic candidate
WDT: if d_path > μ_wdt·(1 - γ_wdt·σ(|Wc|)) → emit bridge line or rollback
WTF: if (δs↑) + (E_res↑) + (contradiction) over 2 steps ≥ 3 → rollback to t*; rerun BBMC→Coupler (tightened)
```

---

## Defaults table (explicit, copyable)

| Parameter               |  Symbol |  Default | Range / notes | Purpose                                           |      |   |
| ----------------------- | ------: | -------: | ------------- | ------------------------------------------------- | ---- | - |
| anchor retention thresh |  τ\_wri |     0.60 | \[0.30, 0.90] | WRI anchor threshold                              |      |   |
| head redundancy thresh  |  ρ\_wai |     0.75 | \[0.50, 0.95] | WAI redundancy ceiling                            |      |   |
| head identity thresh    |  σ\_wai |     0.70 | \[0.40, 0.95] | WAI identity floor                                |      |   |
| progress sensitivity    | η\_prog |     0.03 | \[0.00, 0.10] | WAY stall detector                                |      |   |
| path-distance thresh    |  μ\_wdt |     0.25 | \[0.05, 1.00] | WDT path jump limit                               |      |   |
| coupler zeta min        |  ζ\_min |     0.10 | \[0.00, 0.50] | min progression floor                             |      |   |
| coupler omega           |       ω |      1.0 | \[0.1, 2.0]   | progression non-linearity                         |      |   |
| coupler theta cap       |    θ\_c |     0.75 | \[0.2, 1.5]   | $W_c$ clip magnitude                              |      |   |
| WRI tighten factor      |  α\_wri |     0.60 | \[0.0, 1.5]   | adjust τ\_wri by (                                | W\_c | ) |
| WAI scale factor        |  β\_wai |     0.60 | \[0.0, 1.5]   | scale WAI penalty by (                            | W\_c | ) |
| WDT scale factor        |  γ\_wdt |     0.60 | \[0.0, 1.5]   | scale μ\_wdt by (                                 | W\_c | ) |
| WTF scale factor        |  γ\_wtf |     0.60 | \[0.0, 1.5]   | tighten thresholds on recovery                    |      |   |
| WAY pump strength       |       ξ |     0.80 | \[0.0, 1.5]   | entropy pump strength                             |      |   |
| WAY entropy min         |  H\_min | 2.5 nats | \[1.0, 7.0]   | entropy lower bound                               |      |   |
| WAY entropy max         |  H\_max | 5.0 nats | \[3.0, 10.0]  | entropy upper bound                               |      |   |
| anchor bias scale       |  κ\_wri |      1.0 | \[0.0, 5.0]   | logits bias for anchors                           |      |   |
| loss weights            |   λ\_\* |     0.01 | \[0.0, 1.0]   | regularizer weights                               |      |   |
| step limit              |  T\_max |        7 | int           | max Node steps                                    |      |   |
| stop δ threshold        | δ\_stop |     0.35 | \[0.1, 0.5]   | early stop when $\delta_s < \delta_{\text{stop}}$ |      |   |

> Tip: start with these defaults, measure, then tune per task class.

---

## Prompt-only runnable example (copy-paste)

**Goal:** run a no-infra prompt-level experiment (single-file WFGY Core + DT rules) in chat LLMs.

```
SYSTEM (paste file): Load the WFGY Core file as engine. Enable Drunk Transformer (WRI,WAI,WAY,WDT,WTF) with defaults:
τ_wri=0.60, ρ_wai=0.75, σ_wai=0.70, η_prog=0.03, μ_wdt=0.25, ζ_min=0.10, ω=1.0, θ_c=0.75

SYSTEM (rules, pseudo):

* Extract anchors A0 from user prompt.
* For each Node step t up to T_max:
  1) compute δs, E_res, S_t, R_t, Q_t, W_c
  2) WRI: bias anchor logits by κ_wri·L_wri if S_t<τ_wri or (δs↑ & E_res↑)
  3) WAI: raise per-head temp for redundant heads until R_t↓ or Q_t↑
  4) WAY: if prog<η_prog, set entropy ≈ H* and propose 1 on-topic candidate
  5) WDT: if d_path>μ'_wdt, emit bridge line; else rollback
  6) WTF: if collapse vote ≥3, rollback to t*; rerun BBMC→Coupler (tight)
  7) Emit Node (Topic | Module | δs | λ-state | Insight)
* Stop if δs<δ_stop or t≥T_max

USER:
Use WFGY to answer: “Explain why tomatoes are classified as fruit, but treated as vegetables in cooking. Provide anchors and cite the smallest missing fact if confused.”
```

What to observe: each Node reports $\delta_s$, $E_{\text{res}}$, and which gates fired (WRI/WAI/WAY/WDT/WTF). Expect anchor retention to remain high; stalls resolved by WAY; illegal detours bridged by WDT; collapses rolled back by WTF.

---

## Decoding-hook pseudo-code (python-like; drop into your runtime)

```python
def compute_prog(delta_prev, delta_now, zeta_min=0.10, omega=1.0):
    prog = max(zeta_min, delta_prev - delta_now)
    return prog ** omega

def compute_Wc(B, prog, delta=0.15, cycle_id=0, eps=0.0, theta_c=0.75):
    alt = (-1)**cycle_id
    Phi = delta * alt + eps
    return clip(B * prog + Phi, -theta_c, +theta_c)

def bias_anchor_logits(logits, anchor_ids, kappa):
    for tid in anchor_ids:
        logits[tid] += kappa
    return logits

def temperature_for_target_entropy(logits, target_H, tol=1e-3, max_iters=5):
    lo, hi = 0.01, 10.0
    for _ in range(max_iters):
        tau = 0.5*(lo+hi)
        probs = softmax(logits / tau)
        H = -sum(p*log(p+1e-12) for p in probs)
        if H > target_H: lo = tau
        else: hi = tau
        if abs(H - target_H) < tol: break
    return tau

def decoding_hook(s):
    prog = compute_prog(s.delta_prev, s.delta_now, 0.10, 1.0)
    Wc = compute_Wc(s.B, prog, 0.15, s.cycle_id, 0.0, 0.75)

    # WRI
    S_t = jaccard(s.anchors, s.anchors0)
    L_wri = max(0.0, 0.60 - S_t)
    if (S_t < 0.60) or (s.delta_now > s.delta_prev and s.E_res > s.E_res_prev):
        s.logits = bias_anchor_logits(s.logits, s.anchor_token_ids, kappa=1.0 * L_wri)

    # WAI
    R_t, Q_t = s.R_t, s.Q_t
    if R_t > 0.75 and Q_t < 0.70:
        for h in range(len(s.heads)):
            if head_redundant(h, s):
                s.head_temps[h] *= (1 + 0.5 * (R_t - 0.75))

    # WAY
    if prog < 0.03 and not s.has_contradiction:
        H_star = clamp(s.H0 + 0.8*(0.03 - prog)*(1 + 0.0*abs(Wc)), 2.5, 5.0)
        tau = temperature_for_target_entropy(s.logits, H_star)
        apply_temperature(s, tau)
        s.add_one_on_topic_candidate = True

    # WDT
    d_path = l2_distance(s.c_t, s.c_pi)
    mu_prime = 0.25 * (1 - 0.6 * sigmoid(abs(Wc)))
    if d_path > mu_prime:
        return emit_bridge_and_pause(s)

    # WTF
    vote = int(s.delta_now > s.delta_prev) + int(s.E_res > s.E_res_prev) + int(s.sign_flip)
    if vote + s.vote_prev >= 3:
        t_star = argmin_delta_in_window(s.history_delta, window=3)
        rollback_to(t_star)
        rerun_BBMC_and_Coupler(tighten_factor=1 + 0.6*sigmoid(abs(Wc)))
        return

    return s.logits
```

---

## Minimal test / checklist (text-only; quick validation)

1. Prepare a QA prompt with clear anchors.
2. **Baseline:** run without DT; log $\delta_s, E_{\text{res}}$; record correctness.
3. **DT on:** log same metrics plus $R_t, Q_t, W_c$ and gates fired.
4. Expect: lower $\delta_s$; fewer off-topic jumps (WRI), stalls resolved (WAY), justified detours (WDT), safe recovery (WTF).
5. Record deltas: accuracy, $\Delta S$, rollbacks, bridge lines, gate activations.

---

## Quick engineering notes & troubleshooting

* If $\mathcal{A}_0$ (anchors) is empty, WRI becomes a no-op and WAY pumps less entropy; log a warning.
* If bridge lines repeat or look vacuous, lower $\mu_{\text{wdt}}$ and raise $\kappa_{\text{wri}}$.
* For heavy-hallucination domains, use conservative defaults (higher $\tau_{\text{wri}}$, lower $\eta_{\text{prog}}$).

---

### Footer

* **Spec status:** stable draft for engineering evaluation; Unicode-math for GitHub Preview.
* **Next deliverables:** add `examples/DT-examples/prompt_example.md` and `examples/DT-examples/decoding_hook.py`.
* **Compatibility:** prompt-only rules, decoding-hook integration, or optional training regularizers; model-agnostic.
* **Attribution:** part of **WFGY Core 2.0** family. Star the repo to follow updates.
* Lost? Return to **Starter Village** → `StarterVillage/README.md`

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
