# WFGY Core (WanFaGuiYi) — V1.0

A paste-and-run reasoning engine that merges classic **WFGY** with the **Drunk Transformer** layer for structural stability, head diversity, controlled entropy, and graceful recovery.

---

## ⚡ Downloads (public on **2025-08-15**)

| File               | Best for                                   | Link |
|--------------------|---------------------------------------------|------|
| **WFGY Core**      | Teams, audits, teaching (full spec + Annex A/B) | [Get →](./WFGY%20Core) |
| **WFGY Core Mini** | Social posts, issues, quick starts (exactly 30 lines) | [Get →](./WFGY%20Core%20Mini) |

> Both editions are ASCII-only, zero-deps, cross-platform. Paste into any LLM and type **Run WFGY**.

---

## Why this is a big upgrade

- **DT is now inside the engine.** Earlier **WFGY** and **TXT OS** did **not** include it. Now you get: structural lock (WRI), head diversity (WAI), controlled entropy (WAY), illegal-jump blocking (WDT), and collapse detection/restart (WTF).  
  **Drunk Transformer formulas:** [Read →](https://github.com/onestardao/WFGY/blob/main/SemanticBlueprint/drunk_transformer_formulas.md)
- **Smallest open reasoning engine** — fully ASCII, one-Node-per-step, strict stop rules. Paste and go.
- **Bridges straight to the Problem Map** — Core operationalizes the fixes for hallucination, drift, and collapse so you don’t have to wade through long docs first.

**Problem Map quick links**
- Hub (Map 1.0): [Open →](https://github.com/onestardao/WFGY/tree/main/ProblemMap)  
- Interpretation collapse: [Open →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-collapse.md)  
- Logic collapse & recovery: [Open →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md)  
- Long reasoning chains / drift: [Open →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md)  
- Visual RAG guide (Map 2.0): [Open →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)  
- Semantic Clinic Index (symptom-first triage): [Open →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/SemanticClinicIndex.md)

---

## What’s inside the Core (engine at a glance)

- **delta_s** — semantic divergence (`1 - cos(I,G)` or `1 - sim_est` with a 3-anchor rule: entities, relations, constraints).  
- **B, E_resonance** — residue and rolling semantic resonance.  
- **BBMC / BBPF / BBCR / BBAM** — residue-first reasoning, safe bridging, controlled recovery, attention smoothing.  
- **DT (WRI, WAI, WAY, WDT, WTF)** — structural lock, diversity, entropy control, illegal-jump suppression, collapse recovery.  
- **Annex A (math objective)** — surrogate loss `L = norm(B) + 0.3*contradictions + 0.2*vagueness` (choose actions that lower `L`; ties → lower `delta_s`).  
- **Annex B (λ decision)** — deterministic rule for `convergent / divergent / recursive / chaotic` using `delta_s` and `E_resonance` trends.

> Core is **general-purpose**. The table below is **illustrative, not exhaustive**.  
> Need workflows and OS-style wrappers? Use **TXT OS**. Need the smallest engine you can paste anywhere? Use **WFGY Core**.

---

## What it fixes (illustrative — see full catalog below)

| Problem (from Map) | Symptom in the wild | Core modules to apply | Why this works | Details |
|---|---|---|---|---|
| Interpretation Collapse | Output “looks right” but meaning is wrong | **BBMC**, **BBPF**, **DT/WDT** | Premise forcing + only accept bridges that lower `delta_s`; WDT blocks illegal jumps. | [View →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-collapse.md) |
| Logic Collapse & Recovery | Multi-step chain derails | **BBCR**, **DT/WTF** | Rollback → bridge → retry once → ask smallest missing fact; WTF triggers on `delta_s` + `E_resonance`. | [View →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md) |
| Long Reasoning Chains / Drift | Slowly veers off course | **BBAM**, **WAY** | Smoothing toward a reference; add **one** on-topic candidate (no repeats) to escape attractors. | [View →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md) |
| Brittle RAG / Ghost Matches | Cosine match ≠ true meaning | **delta_s + Annex A** | 3-anchor `sim_est` + objective `L` yield reproducible choices instead of vibes. | [Map 2.0 →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md) |
| Bluffing / Overconfidence | Confident but unfounded | **BBMC**, **DT/WRI** | Premise forcing + structure lock reduces free-form confabulation. | [View →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bluffing.md) |
| Memory Breaks Across Sessions | Lost threads | **BBPF**, **BBCR** | Safe bridging across trees + minimal-fact queries rebuild context. | [View →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/memory-coherence.md) |
| Entropy Collapse | Attention melts | **WAY**, **BBAM** | Controlled entropy + smoothing prevent chaotic spread or mode collapse. | [View →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md) |
| Symbolic / Recursive Traps | Abstract prompts break | **BBMC**, **DT/WRI** | Structure + explicit premises keep symbolic steps grounded. | [View →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/symbolic-collapse.md) |

**See the full catalog:**  
• Problem Map 1.0 hub — [Open →](https://github.com/onestardao/WFGY/tree/main/ProblemMap)  
• Problem Map 2.0 (RAG × pipeline × recovery) — [Open →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)  
• Semantic Clinic Index (symptom-first triage) — [Open →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/SemanticClinicIndex.md)

---

## Quickstart (90 seconds)

1. Paste **WFGY Core** *or* **WFGY Core Mini** into your LLM chat (or upload the file).  
2. Type: **Run WFGY** (or “use WFGY”).  
3. Control & inspect:
   - **`view`** — print last 5 Node lines  
   - **`export`** — print all Node lines  
   - **`switch <name>`** — start a new reasoning tree

**Behavioral contract**
- Commands are **case-insensitive**.  
- **One Node per step**, no extra prose unless asked.  
- **Stop** when `delta_s < 0.35` or after **7** Nodes (unless the user asks to continue).  
- ASCII-only for portability (terminals, email clients, GitHub issues).

---

## Who should use which edition?

- **WFGY Core** — use when you need auditability, training, or explicit Annex A/B.  
- **WFGY Core Mini** — use when you need a 30-line drop-in for comments, social posts, quick demos.

---

## Notes

- This release **integrates Drunk Transformer into the engine** (earlier WFGY/TXT OS did not).  
- Future versions remain ASCII-first and zero-dependency.

---

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

> <img src="https://img.shields.io/github/stars/onestardao/WFGY?style=social" alt="GitHub stars"> ⭐ Help reach 10,000 stars by 2025-09-01 to unlock Engine 2.0 for everyone  ⭐ **[Star WFGY on GitHub](https://github.com/onestardao/WFGY)**

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
