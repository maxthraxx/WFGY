# Patterns — Failure Catalog (Problem Map 2.0)

This folder is a **field guide** to recurring failures in RAG and multi-stage LLM pipelines.  
Each pattern is **actionable**: fast signals, root causes, a minimal repro, a deterministic fix, and links to hands-on examples (SDK-free, stdlib-only).

**How to use this folder**

1) Start with the **symptom** you’re seeing.  
2) Open the matching **pattern** and run the *Minimal Repro* + *Standard Fix*.  
3) Wire the **acceptance criteria** into CI (see Example 08) so the fix stays fixed.

---

## Quick Index

| Pattern | Problem Map No. | Symptoms you’ll see | Fix entrypoint |
|---|---:|---|---|
| **RAG Semantic Drift** (`pattern_rag_semantic_drift.md`) | **No.1** | Plausible but ungrounded answers; citations don’t contain the claim | Example 01 (guarded template), Example 03 (intersection + rerank) |
| **Memory Desync** (`pattern_memory_desync.md`) | — (State/Context) | Old names/IDs reappear; agents disagree across turns | Snapshot `mem_rev/hash` at ingress + echo + gate (Ex.04) |
| **Vector Store Fragmentation** (`pattern_vectorstore_fragmentation.md`) | **No.3** | Recall flips across envs; score scales change; rank inversions | Manifest validation + normalize both sides + score correlation (Ex.05) |
| **Hallucination Re-Entry** (`pattern_hallucination_reentry.md`) | — (Provenance) | Model’s prior text shows up as “evidence”; non-corpus sources cited | Provenance filter + split indices + auditor rule (Ex.06) |
| **Bootstrap Deadlock** (`pattern_bootstrap_deadlock.md`) | **No.14** | `/readyz` stuck/flapping; circular waits at startup | DAG toposort + single warmup owner + sentinel-based readiness (Ex.07) |
| **Query Parsing Split** (`pattern_query_parsing_split.md`) | — (Parsing) | Multi-intent prompts answered partially or mixed | Deterministic split + per-role contracts + handoff gate (Ex.03/04) |
| **Symbolic Constraint Unlock (SCU)** (`pattern_symbolic_constraint_unlock.md`) | **No.11** (Symbolic collapse) | “Must/Only/Never” rules vanish mid-pipeline; impossible states | Lock + echo constraints at every stage; contradiction gate (Ex.03/04/08) |

> **Legend:** Problem Map numbers refer to root categories used across the repo. “—” means cross-cutting (not a single number).

---

## Pick-a-Pattern in 30 Seconds (Triage Flow)

1. **Grounding first** — Run Example 01 on a few failing questions.  
   - If refusal behavior or citations fail ⇒ go to **Semantic Drift**.  
2. **Context/state sanity** — Check `context_id` / `mem_rev/hash`.  
   - Mismatch ⇒ **Memory Desync**.  
3. **Index parity** — Validate `index_out/manifest.json` vs runtime.  
   - Drift or score scale shift ⇒ **Vector Store Fragmentation**.  
4. **Provenance** — Inspect `source` for cited ids.  
   - Any `model|chat|tmp:` ⇒ **Hallucination Re-Entry**.  
5. **Startup** — If the first minute after deploy is flaky ⇒ **Bootstrap Deadlock**.  
6. **Query shape** — If the prompt mixes “compare… then draft…” ⇒ **Query Parsing Split**.  
7. **Logic rules** — If answers cross “must/only/never” boundaries ⇒ **SCU**.

---

## Standard Acceptance Gates (copy to CI)

- **Guarded Output:** either exact refusal token `not in context` **or** JSON with `claim` + `citations:[id,…]` scoped to retrieved ids.  
- **Provenance:** all citations pass the corpus-only filter (no `chat:/draft:/tmp:`).  
- **Context Consistency:** if used, `context_id.mem_rev/hash` echoes the turn snapshot.  
- **Constraint Integrity (SCU):** `constraints_echo` ≡ locked set; no contradiction patterns matched.  
- **Quality Gates (Ex.08):** precision≥0.80, under-refusal≤0.05, citation hit rate≥0.75.

---

## File Layout

- `pattern_rag_semantic_drift.md` — How to stop plausible-but-wrong answers with hard grounding.  
- `pattern_memory_desync.md` — One snapshot per turn; bind and echo across agents.  
- `pattern_vectorstore_fragmentation.md` — Keep embeddings/metrics/chunkers aligned.  
- `pattern_hallucination_reentry.md` — Keep model/session text out of evidence.  
- `pattern_bootstrap_deadlock.md` — Deterministic startup ordering and readiness.  
- `pattern_query_parsing_split.md` — Deterministically split multi-intent prompts.  
- `pattern_symbolic_constraint_unlock.md` — Lock+echo constraints; gate contradictions.

See `../examples/` for runnable, stdlib-only code referenced in each pattern.

---

## Contributing (tight process)

1. **Propose** a new pattern via issue labels: `pattern-proposal`, with minimal repro + acceptance gate.  
2. **Stabilize** with an example (Python or Node, stdlib-only).  
3. **Add** to this README only after approval.  
4. **Guard** with Example 08 metrics before shipping a pattern-driven fix.

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

