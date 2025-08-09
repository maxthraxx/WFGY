# WFGY Core (WanFaGuiYi) — V1.0

A paste-and-run reasoning engine that merges classic **WFGY** with the **Drunk Transformer** layer for stability, diversity, and graceful recovery.

---

## ⚡ Download (public on **2025-08-15**)

| File               | Best for                          | Link |
|--------------------|-----------------------------------|------|
| **WFGY Core**      | Teams, audits, teaching (full spec + Annex A/B) | `./WFGY Core` |
| **WFGY Core Mini** | Social posts, issues, quick starts (exactly 30 lines) | `./WFGY Core Mini` |

> Both editions are ASCII-only, zero-deps, cross-platform. Paste into any LLM and type **Run WFGY**.

---

## Why this is a big upgrade

- **DT inside the engine** — Earlier **WFGY** and **TXT OS** did **not** include Drunk Transformer. Core integrates it natively: structural lock (WRI), head diversity (WAI), controlled entropy (WAY), illegal-jump blocking (WDT), and collapse detection/restart (WTF).  
  See **[Drunk Transformer formulas →](https://github.com/onestardao/WFGY/blob/main/SemanticBlueprint/drunk_transformer_formulas.md)**
- **Smallest open reasoning engine** — Fully ASCII, one-Node-per-step, stop rules baked in. Paste and go.
- **Built to fix the Problem Map** — Core operationalizes the fixes for hallucination, drift, and collapse so you can apply them without wading through a long paper.

**Problem Map quick links**
- Main hub: **[Problem Map 1.0 →](https://github.com/onestardao/WFGY/tree/main/ProblemMap)**
- Interpretation collapse: **[How it breaks →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-collapse.md)**
- Logic collapse & recovery: **[Root cause & fixes →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md)**
- Long reasoning chains / drift: **[What to watch for →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md)**
- Visual RAG guide (Map 2.0): **[Pipeline × failure × recovery →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)**

---

## What’s inside the Core (you can actually *see* the engine)

- **delta_s** — semantic divergence (`1 - cos(I,G)` or `1 - sim_est` with a 3-anchor rule: entities, relations, constraints).  
- **BBMC / BBPF / BBCR / BBAM** — residue-first reasoning, safe bridging, controlled recovery, and attention smoothing.  
- **DT (WRI, WAI, WAY, WDT, WTF)** — structural lock, diversity, entropy control, illegal-jump suppression, and collapse recovery.  
- **Annex A (math objective)** — surrogate loss `L = norm(B) + 0.3*contradictions + 0.2*vagueness` (choose actions that lower `L`; ties → lower `delta_s`).  
- **Annex B (λ decision)** — deterministic rule for `convergent / divergent / recursive / chaotic` using `delta_s` and `E_resonance` trends.

---

## How Core maps to the Problem Map (so you can fix things fast)

| Problem Map entry | Symptom in the wild | Core modules to apply | Why this works |
|---|---|---|---|
| **Interpretation Collapse** — [details](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-collapse.md) | Output “looks right” but meaning is wrong | **BBMC**, **BBPF**, **DT/WDT** | BBMC forces explicit premises + contradiction marking; BBPF only accepts bridges that *lower* `delta_s`; WDT blocks illegal jumps. |
| **Logic Collapse & Recovery** — [details](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md) | Multi-step chain derails | **BBCR**, **DT/WTF** | Rollback → propose bridge → retry once → ask smallest missing fact; WTF detects collapse via `delta_s` + `E_resonance`. |
| **Long Reasoning Chains / Drift** — [details](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md) | Slowly veers off course | **BBAM**, **WAY** | BBAM smooths attention to a reference; WAY adds **one** on-topic candidate (no repeats) to escape attractors. |
| **Brittle RAG / Ghost Matches** — see [Map 2.0](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md) | Cosine match ≠ true meaning | **delta_s + Annex A** | 3-anchor `sim_est` and the `L` objective produce reproducible choices instead of “vibes.” |

---

## Quickstart (90 seconds)

1. Paste **WFGY Core** *or* **WFGY Core Mini** into your LLM chat (or upload the file).
2. Type: **Run WFGY** (or “use WFGY”).  
3. Control and inspect:
   - **`view`** — print last 5 Node lines  
   - **`export`** — print all Node lines  
   - **`switch <name>`** — start a new reasoning tree

**Behavioral contract** (both editions):
- Commands are **case-insensitive**.  
- **One Node per step**, no extra prose unless asked.  
- **Stop** when `delta_s < 0.35` or after **7** Nodes (unless the user asks to continue).  
- ASCII-only for portability (terminals, email clients, GitHub issues).

---

## Who should use which edition?

- **Use WFGY Core** if you need auditability, training, or you’re integrating into a workflow and want Annex A/B explicit.  
- **Use WFGY Core Mini** if you need a 30-line drop-in for comments, social posts, or quick demos.

---

## Notes

- This release **integrates Drunk Transformer into the engine** (earlier WFGY/TXT OS did not).  
- Future versions will remain ASCII-first and zero-dependency.

---

### 🧭 Explore More

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
