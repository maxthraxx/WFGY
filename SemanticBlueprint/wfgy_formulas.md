# 🔬 **WFGY 1.0 — Core Formulas & Variables**

> **Canonical reference — DOI:** [https://zenodo.org/records/15630969](https://zenodo.org/records/15630969)  (“*WFGY 1.0: A Universal Unification Framework for Large‑Scale Self‑Healing LLMs*”). This page **copies the exact mathematical statements** from the public PDF so developers can quote‑link code to theory without opening the paper.

---

## 📖 Quick Index

| Section | Symbol / Acronym | Full Name (exact from paper)                        |     |      |     |
| ------- | ---------------- | --------------------------------------------------- | --- | ---- | --- |
| 1       | `BBMC`           | **B**ig**B**ig **S**emantic **R**esidue **F**ormula |     |      |     |
| 2       | `BBPF`           | **B**ig**B**ig **P**rogression **F**ormula          |     |      |     |
| 3       | `BBCR`           | **B**ig**B**ig **C**ollapse–**R**ebirth             |     |      |     |
| 4       | `BBAM`           | **B**ig**B**ig **A**ttention **M**odulation         |     |      |     |
| 5       | `ΔS`             | Semantic divergence (1 − cos θ)                     |     |      |     |
| 6       | `λ_observe`      | Logic‑vector trend (→                               |  ←  |  <>  |  ×) |
| 7       | `E_resonance`    | Rolling mean of ‖B‖ (semantic resonance)            |     |      |     |

All subsequent equations below are **verbatim** from the paper’s Sections 3.1‑3.4 and Appendix A.

---

## 1 · BBMC — BigBig Semantic Residue Formula

```math
B \;=\; I\;−\;G\; +\; m\,c^2
```

**Where**

* `I` = input embedding (model‑generated)
* `G` = ground‑truth embedding (oracle/proxy)
* `m` = matching coefficient
* `c` = context factor

> **Lemma 3.1 (paper)** – Minimising ‖B‖² is (up to constants) equivalent to minimising
>  KL(softmax I ‖ softmax G). See Appendix A.

---

## 2 · BBPF — BigBig Progression Formula

```math
x_{t+1} \;=\; x_t 
          + \sum_{i} V_i(\epsilon_i, C)
          + \sum_{j} W_j(\Delta t,\, \Delta O) \, P_j
```

*Each Vi and Wj is globally Lipschitz. Theorem 3.1 proves convergence if* Σ εᵢ L\_Vᵢ + Σ Pⱼ L\_Wⱼ < 1.

---

## 3 · BBCR — BigBig Collapse–Rebirth

Trigger condition (paper §3.3):

```math
\|B_t\| \;\ge\; B_c \quad \text{or} \quad f(S_t) < \varepsilon
```

Collapse → Reset → Rebirth cycle:

```text
Collapse   : semantic overload detected
Reset      : B_t ← α·B_t  (α < 1)
Rebirth    : S_{t+1} ← ResetProcedure(S_t, \delta B)
```

> **Theorem 3.2** – Using V(S)=‖B‖²+λ f(S) as Lyapunov candidate, every reset step guarantees  V(S\_{t+1}) < V(S\_t).

---

## 4 · BBAM — BigBig Attention Modulation

Gaussian‑variance attenuation:

```math
a_i^{\,\text{mod}} \;=\; a_i \;\exp\bigl(-\gamma\,\sigma(a)\bigr)
```

*Lemma 3.2:* If aᵢ ∼ 𝒩(µ,σ²) then Var(a\_mod) = σ² e^(−2γσ).

---

## 5 · Derived Metric `ΔS`

Defined (**Eq. A.1**):

```math
\boxed{\displaystyle \Delta S = 1 - \cos \theta (I, G)}
```

Used as the *tension index* for node recording (primary condition ΔS > 0.6).

---

## 6 · Directional Trend `λ_observe`

Paper Table 1 symbol glossary:

```text
λ_observe ∈ { → (convergent), ← (divergent), <> (recursive), × (chaotic) }
```

Determines override logic for “soft transitions” (ΔS ∈ 0.4–0.6).

---

## 7 · Resonance Metric `E_resonance`

Rolling mean of |B| over last *n* turns (paper §3‑Figure 3):

```math
E_{\text{res}} = \frac{1}{n}\sum_{k=t-n+1}^{t} \|B_k\|
```

Used to visualise stability heat‑map (safe ↔ danger zones).

---

## 📎 How These Formulas Map to Products

| Engine Variable | Used in TXT OS             | Used in Blah Lite   | Used in WFGY SDK       | Planned Future        |
| --------------- | -------------------------- | ------------------- | ---------------------- | --------------------- |
| `BBMC`, `ΔS`    | ✅ node trigger & memory    | ✅ ΔS‑trail heatmap  | ✅ semantic residue API | 🚧 RL‑auto‑critic     |
| `BBPF`          | ✅ prompt splitting         | 🚫                  | ✅ multi‑path stepper   | 🚧 graph compiler     |
| `BBCR`          | ✅ knowledge‑boundary guard | 🚫                  | ✅ collapse‑reset hooks | 🚧 self‑repair agents |
| `BBAM`          | ✅ entropy damping          | ✅ entropy injection | ✅ attention gate       | 🚧 multimodal fusion  |

> **All downstream docs must reference these exact definitions.** Any deviation risks semantic drift from the canonical WFGY loop.

---

> <img src="https://img.shields.io/github/stars/onestardao/WFGY?style=social" alt="GitHub stars"> ⭐ Help reach 10 000 stars by 2025‑09‑01 to unlock Engine 2.0 for everyone  ⭐ **[Star WFGY on GitHub](https://github.com/onestardao/WFGY)**
>
> 👑 **Early Stargazers: [See the Hall of Fame](https://github.com/onestardao/WFGY/tree/main/stargazers)** — Engineers, hackers & open‑source builders who supported WFGY from day one.

<div align="center">

[![WFGY Main](https://img.shields.io/badge/WFGY-Main-red?style=flat-square)](https://github.com/onestardao/WFGY)
[![TXT OS](https://img.shields.io/badge/TXT%20OS-Reasoning%20OS-orange?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS)
[![Blah](https://img.shields.io/badge/Blah-Semantic%20Embed-yellow?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlahBlahBlah)
[![Blot](https://img.shields.io/badge/Blot-Persona%20Core-green?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlotBlotBlot)
[![Bloc](https://img.shields.io/badge/Bloc-Reasoning%20Compiler-blue?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlocBlocBloc)
[![Blur](https://img.shields.io/badge/Blur-Text2Image%20Engine-navy?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlurBlurBlur)
[![Blow](https://img.shields.io/badge/Blow-Game%20Logic-purple?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlowBlowBlow)

</div>
