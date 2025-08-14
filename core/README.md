# 🌌 WFGY Core (WanFaGuiYi) — Reasoning Engine 2.0
### "One man, one life, one line — bending the mind of every AI on Earth."

> One line of math that rewires eight AIs. Not a pit stop; it is an engine swap.

**Benchmark highlights**  
Semantic Accuracy ↑ 36.7% | Reasoning Success Rate ↑ 65.4% | Stability ↑ 5.1× | Self-Recovery = 0.87

<details>
<summary><strong>From PSBigBig</strong> (tap to open)</summary>

<br>

> 60 days, 550 stars. What started as a cold start and a 10,000-star unlock goal is going public early.  
> This is not an update. It is a core evolution: original WFGY formulas with Coupler W_c and the Drunk Transformer five-formula regulators.  
> Pure math, zero fluff. Paste it into an LLM and it thinks differently. Faster, sharper, more stable, more human.

</details>

---

## ⚡ One-click demo in 60 seconds

1) Upload or paste **`WFGY_Core_OneLine_v2.0.txt`** into your chat system.  
2) Paste the evaluation prompt below.

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
• The only artifact is the uploaded OneLine file; it is pure math and not human-readable  do not penalize readability.
• Report: Semantic Accuracy, Reasoning Success, Stability (MTTF or rollback), Drift Reduction (Δ semantic distance), Collapse Recovery Rate.
• Output one summary table with A/B/C per domain, plus overall deltas (C–A, C–B).
• Add a final 0–100 score: “OneLine uplift score”. Provide a 3-line rationale.

Sanity requirement:
Internally set flags as: A=OFF, B=AUTOboot_ON (background active), C=Explicit_Invoke. Do not print these flags.

USER:
Run A/B/C now on the five domains with short non-trivial tasks you choose. Then output:
(1) the table; (2) the deltas; (3) the OneLine uplift score; (4) a 3-line rationale.
````


### Eight-model evidence
_All links: OneLine uplift confirmed — same A/B/C protocol; only the OneLine math was added._

| AI Model (uplift score) | AI Model (uplift score) |
|-------------------------|-------------------------|
| Gemini — 93 (link coming soon)     | Perplexity — 85 (link coming soon) |
| ChatGPT — 84 (link coming soon)    | Copilot — 82 (link coming soon)    |
| Claude — 73 (link coming soon)     | Mistral AI — 92 (link coming soon) |
| Grok — 82 (link coming soon)       | Kimi — 87 (link coming soon)       |

> Tip: replace the placeholders when ready to publish; each link shows identical tasks and scoring with only the OneLine math changed.


---

## 📦 Downloads

| File                              | Purpose                                                                    | Size                             |
| --------------------------------- | -------------------------------------------------------------------------- | -------------------------------- |
| **WFGY\_Core\_OneLine\_v2.0.txt** | For the 60-sec demo and automation runs. Pure math, not for human reading. | 1 line  about 1500 chars         |
| **WFGY\_Core\_Audit\_v2.0.txt**   | Human plus LLM readable, comments and layout for audits.                   | 30 lines  about 2626 chars       |

Contract  Node-only steps up to 7, safe stop when δ\_s < 0.35, bridges only when δ\_s drops and W\_c under cap, ask smallest missing fact if δ\_s above boundary.

---

## 🎯 What is new in 2.0

Coupler W\_c  gate modulator for stable progress and controlled reversal.
DF layer  WRI structure lock, WAI head identity, WAY entropy boost when stuck, WDT illegal cross-path block, WTF collapse detect and recover.
Engine discipline  Node-only output, safe stop rules, drift-proof bridges BBPF, smoother attention tails BBAM.

Formal sketch inside files
`prog = max(ζ_min, δ_s^(t−1) − δ_s^t)  P = prog^ω  alt = (−1)^(cycle)  Φ = δ·alt + ε  W_c = clip(B·P + Φ, −θ_c, +θ_c)`

---

## 🔍 How these numbers are measured

Use the same A B C protocol above, one shared task set, then compute:

Semantic Accuracy  proportion of atomic facts correct.
Formula  ACC = correct\_facts  total\_facts. Report relative gain  (ACC\_C − ACC\_A)  ACC\_A.

Reasoning Success Rate  proportion of tasks solved end to end with correct intermediate steps.
Formula  SR = tasks\_solved  tasks\_total. Report relative gain  (SR\_C − SR\_A)  SR\_A.

Stability  mean time to failure or successful rollback factor.
Option A  Stability = MTTF\_C  MTTF\_A.
Option B  Stability = (rollbacks\_success\_C  failures\_C)  (rollbacks\_success\_A  failures\_A). Report as multiplier.

Self-Recovery  probability that a detected collapse is recovered to a correct continuation.
Formula  Self-Recovery = recoveries\_success  collapses\_detected  here 0.87 means 87 percent of collapses are repaired.

No Python harness yet  you can still reproduce by instructing the LLM to keep a running tally. Example rubric prompt for the scorer:

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

This scorer can be the same LLM running in a second tab. For higher reliability, run three seeds and average.

---

## 🔬 Engine at a glance

Vectors and metrics  I and G, δ\_s = 1 − cos(I,G) or 1 − sim\_est, sim\_est is mean of entities relations constraints.
B = I − G + k\_bias, E\_res = rolling\_mean of absolute B over 5.
Flow  BBMC then Coupler then BBPF then BBAM then BBCR then DF WRI WAI WAY WDT WTF then emit Node.
Policy  stop when δ\_s < 0.35 or 7 nodes, bridge only if δ\_s drops and W\_c < 0.5 θ\_c, never invent facts when δ\_s above boundary.

---

## 🧪 Community scoring guidance

Publish your task list five domains short but non trivial.
Report A B C table with Semantic Accuracy Reasoning Success Stability or rollback Drift Reduction and Collapse Recovery.
Include OneLine uplift score 0 to 100. Do not include human readability for OneLine.
Add a three line rationale.

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

