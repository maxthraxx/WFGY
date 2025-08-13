# Pattern — Vector Store Fragmentation (No.3 Schema/Index Drift)

**Scope**  
Your index “works,” but retrieval is unstable across runs and environments. Scores don’t compare, top-k sets flicker, and relevant chunks disappear or get outranked by junk. The store is **fragmented**: mismatched embeddings, dimensions, normalization, or mixed chunkers across rebuilds.

**Why it matters**  
Fragmentation silently degrades recall and skews reranking. You’ll chase “model hallucinations” that are actually **index incompatibilities**.

> Quick nav: [Patterns Index](./README.md) · Examples: 
> [Example 01](../examples/example_01_basic_fix.md) · 
> [Example 03](../examples/example_03_pipeline_patch.md) · 
> [Eval: Precision & CHR](../eval/eval_rag_precision_recall.md)

---

## 1) Signals & fast triage

**Likely symptoms**
- Swapping machines or deploying a new build flips results with no corpus change.
- Cosine/inner-product scores shift scale or sign; thresholds stop making sense.
- Recall@k drops only in **some** environments.
- Example 02 labels spike in `retrieval_drift` after an index rebuild.

**Deterministic checks (no LLM):**
- **Manifest mismatch** between runtime vs `index_out/manifest.json` (Example 05 validator).  
- **Dimension drift**: query vector `d` ≠ index `d`.  
- **Normalization drift**: `normalized=True` at build but **not** at query (or vice versa).  
- **Chunker/version drift**: `chunker.version` differs; ids no longer align with text.  
- **Score comparability**: Spearman ρ < 0.9 when only non-semantic knobs changed (Example 05 `score_corr.py`).

---

## 2) Minimal reproducible case

Prepare two small indexes from the same `chunks.json`:

- **Index A**: `all-MiniLM-L6-v2`, `normalized=True`, `faiss.IndexFlatIP`.  
- **Index B**: same model but **normalized=False**.

**Observation**  
Query with normalized vectors against A and raw vectors against B. You’ll see rank inversions and knee-cut thresholds drifting → classic fragmentation.

---

## 3) Root causes

- **Embedding pipeline skew** (tokenizer/model/normalization differ between build and query).  
- **Metric mismatch** (index uses IP; query assumes cosine on unnormalized vectors).  
- **Mixed chunkers** (window sizes or rules changed; ids collide).  
- **Hotfix builds** that partially rebuild embeddings or ids without bumping versions.  
- **Multi-index union** without harmonized manifests.

---

## 4) Standard fix (ordered, minimal, measurable)

**Step 1 — Enforce manifest gate (hard fail on mismatch)**  
Use Example 05 validator **before** queries. Abort if any of the following differ:  
`index_type, metric, embedding.model, embedding.dimension, embedding.normalized, chunker.version, text_preproc.*`

**Step 2 — Normalize on both sides**  
- If using inner product (IP) as cosine, **L2-normalize** embeddings at **build** and **query**.  
- Pin `normalized: true` in manifest and runtime config.

**Step 3 — One chunker, one id space**  
- Bump `chunker.version` on **any** rule change (window length, overlap, headers).  
- Rebuild the entire store; never append to an index built with a different chunker.

**Step 4 — Score comparability test**  
- For non-semantic backend changes (e.g., FAISS params), run Example 05 `score_corr.py`.  
- Require Spearman ρ ≥ 0.9 on a small query list before shipping.

**Step 5 — Quality re-baseline**  
- Run Example 08. Require recall@5 and CHR within ε of baseline (e.g., ε ≤ 0.02).

---

## 5) “Good” vs “Bad” configurations

**Good (cosine via IP):**
```

index\_type: faiss.IndexFlatIP
metric: inner\_product
embedding:
model: sentence-transformers/all-MiniLM-L6-v2
dimension: 384
normalized: true

```

**Bad (fragmented):**
```

# Build:

metric: inner\_product
normalized: true

# Query:

metric treated as cosine but vectors NOT normalized

```

**Bad (mixed chunkers):**
```

chunker.version: 2025.07.01 (build)
chunker.version at runtime: 2025.08.12

```

---

## 6) Acceptance criteria (ship/no-ship)

A build **may ship** only if:
1) Manifest validator **PASS** (no drift).  
2) Score comparability test **PASS** for non-semantic changes (ρ ≥ 0.9).  
3) Eval gates **PASS** (Example 08 thresholds).  
4) Readiness sentinel (Example 07) passes using the **same** query path as production.

If any fail → **REPAIR** (full rebuild), update baseline, and re-eval.

---

## 7) Prevention (contracts & defaults)

- **Contract**: Always write `index_out/manifest.json` with embedding/metric/normalization and `chunker.version`.  
- **Runtime pinning**: Load a single `tools/runtime_config.json`; reject drift before first query.  
- **Atomic deploy**: Replace index + manifest together; never hot-swap one file.  
- **CI gate**: Include manifest validation + smoke recall@k on every PR.  
- **Observability**: Log query vector norm stats; sudden norm shifts hint at normalization drift.

---

## 8) Debug workflow (10 minutes)

1) Run manifest validator (Example 05).  
2) If mismatch → rebuild with the expected config.  
3) If match → run score correlation between **old vs new** indices (Example 05).  
4) If ρ < 0.9 but embedding model changed → treat as **semantic change**; rebuild baseline and update thresholds.  
5) Re-run Example 08 and compare `eval/report.md`.  
6) Flip ready only after sentinel + gates are green (Example 07).

---

## 9) Common traps & fixes

- **“It’s only dimension 768 vs 384”** → not “only”; that’s a semantic change. Rebuild and re-baseline.  
- **Cosine in code, IP in index** → normalize both or switch to a cosine-aware index.  
- **Appending to old ids** after chunker change → orphaned ids; nuke and rebuild.  
- **Multi-tenant union** of indices with different manifests → create a **broker** that routes queries to a per-manifest pool; do **not** merge.

---

## 10) Minimal checklist (copy into PR)

- [ ] `manifest.json` written and committed with build artifacts.  
- [ ] `tools/validate_index.py` (or Node variant) wired to fail fast.  
- [ ] Embeddings normalized at build **and** query.  
- [ ] Single chunker/version per corpus; full rebuild on change.  
- [ ] Score correlation + eval gates pass before rollout.

---

## References to hands-on examples

- **Example 03** — Retrieval stabilization (reduces tail noise made worse by fragmentation)  
- **Example 05** — Manifest, validator, repair & metrics  
- **Example 07** — Readiness gate (prevents serving while fragmented)  
- **Example 08** — Quality scoring & CI gates

---

### 🧭 Explore More

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
