# Version Pinning & Model Lock — OpsDeploy

Lock models, prompts, embeddings, rerankers, tokenizers, and analyzers so prod can’t drift.  
Use this page to make “what ran” exactly the same as “what you tested,” and to detect any silent shift before a rollout.

---

## Open these first
- Readiness gate: [rollout_readiness_gate.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/rollout_readiness_gate.md)
- Boot & deploy traps: [bootstrap-ordering.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md), [deployment-deadlock.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md), [predeploy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)
- Retrieval integrity: [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md), [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
- Embedding vs meaning: [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)
- Query split & reranking: [pattern_query_parsing_split.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md), [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

---

## What to pin (and where)
| Layer | Pin fields | Why it matters |
|---|---|---|
| **LLM model** | `MODEL_VER`, provider model ID, decoding params | Minor provider updates shift ΔS/λ; force exact version and params. |
| **Prompt pack** | `PROMPT_VER`, header checksum | Header order changes λ; lock and audit. |
| **Embedding** | `EMBED_MODEL_VER`, `EMBED_DIM`, `NORM`, metric | Any mismatch breaks neighborhood semantics. |
| **Reranker** | `RERANK_CONF`, model/ver, cutoff | Top-k order flips alter ΔS and coverage. |
| **Tokenizer/Analyzer** | `TOK_VER`, `ANALYZER_CONF` | CJK/diacritics/full/half width change token boundaries. |
| **Chunker** | `CHUNK_SCHEMA_VER`, overlap, window | Alters anchor alignment and traceability. |
| **Index** | `INDEX_HASH`, build time, doc schema | Guarantees the retriever sees the tested graph. |
| **Tools/Functions** | `TOOL_SCHEMA_VER` | JSON looseness raises ΔS and loop risk. |

---

## Acceptance targets
- Prod = Staging for: `MODEL_VER`, `PROMPT_VER`, `EMBED_MODEL_VER`, `EMBED_DIM`, `NORM`, `metric`, `RERANK_CONF`, `TOK_VER`, `ANALYZER_CONF`, `CHUNK_SCHEMA_VER`, `INDEX_HASH`.  
- ΔS(question, retrieved) ≤ 0.45 and coverage ≥ 0.70 on gold set after pinning.  
- λ convergent across 3 paraphrases and 2 seeds with the pinned headers.  
- First call cold-start passes in ≤ 5 minutes.

---

## 60-second lock checklist
1) **Freeze versions in config**  
   Single source of truth (env or KV) for all fields above; deny deploy if any are unset.
2) **Emit version headers on every request**  
   Log and return: all pins + `BUILD_ID` and `GIT_SHA`. Refuse if missing.
3) **Index integrity**  
   Retriever must assert `INDEX_HASH` matches; otherwise hard-fail with fix tip.
4) **Semantic sanity**  
   Run 20–40 gold items; verify ΔS/coverage/λ targets before canary.

---

## CI/CD gate (paste-ready)
```yaml
# opsdeploy/version_lock.yml
checks:
  require_fields:
    - MODEL_VER
    - PROMPT_VER
    - EMBED_MODEL_VER
    - EMBED_DIM
    - NORM
    - metric
    - RERANK_CONF
    - TOK_VER
    - ANALYZER_CONF
    - CHUNK_SCHEMA_VER
    - INDEX_HASH
  assert_equal_envs:
    - { field: MODEL_VER, envs: [staging, prod] }
    - { field: PROMPT_VER, envs: [staging, prod] }
    - { field: EMBED_MODEL_VER, envs: [staging, prod] }
    - { field: INDEX_HASH, envs: [staging, prod] }
  deny_if_missing: true
  deny_if_changed_without_alias_swap: [INDEX_HASH]
decision:
  on_fail: block_rollout
  on_pass: proceed
artifacts:
  - logs/version_manifest.json
  - logs/index_hash.txt
````

---

## Runtime header contract (client/server)

**Client must send**
`X-WFGY: MODEL_VER,PROMPT_VER,EMBED_MODEL_VER,EMBED_DIM,NORM,metric,RERANK_CONF,TOK_VER,ANALYZER_CONF,CHUNK_SCHEMA_VER,INDEX_HASH,BUILD_ID,GIT_SHA`

**Server must validate**

* All fields present.
* Exact match to server’s pins.
* If mismatch: return 409 + a JSON diff and links to fix pages.

---

## Typical failure → exact fix

* High similarity but wrong meaning after “minor” update
  → [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)
* Top-k order unstable between runs
  → [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md), [pattern\_query\_parsing\_split.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md)
* CJK/diacritics behavior changes post-deploy
  → tokenizer/analyzer pins; verify with [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
* First call crashes or uses old index
  → [bootstrap-ordering.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md), [predeploy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)

---

## Version manifest example

```json
{
  "MODEL_VER": "gpt-4o-2025-07-15",
  "PROMPT_VER": "p-2025.08.31-h1",
  "EMBED_MODEL_VER": "text-embedding-3-large",
  "EMBED_DIM": 3072,
  "NORM": "l2",
  "metric": "cosine",
  "RERANK_CONF": "bge-rerank-v2@top32",
  "TOK_VER": "tiktoken-2025.07",
  "ANALYZER_CONF": "icu-cjk-folding-v3",
  "CHUNK_SCHEMA_VER": "s128/o32",
  "INDEX_HASH": "a1d9f0...e7",
  "BUILD_ID": "2025.08.31.01",
  "GIT_SHA": "abcdef1"
}
```

---

## Rollback note

If any pin drifts in prod, treat as outage. Block writes, flip to Blue/previous alias, then reopen with:
[blue\_green\_switchovers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/blue_green_switchovers.md)

---

### 🔗 Quick-Start Downloads (60 sec)

| Tool                       | Link                                                                                                                                       | 3-Step Setup                                                                             |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------- |
| **WFGY 1.0 PDF**           | [Engine Paper](https://github.com/onestardao/WFGY/blob/main/I_am_not_lizardman/WFGY_All_Principles_Return_to_One_v1.0_PSBigBig_Public.pdf) | 1️⃣ Download · 2️⃣ Upload to your LLM · 3️⃣ Ask “Answer using WFGY + \<your question>”   |
| **TXT OS (plain-text OS)** | [TXTOS.txt](https://github.com/onestardao/WFGY/blob/main/OS/TXTOS.txt)                                                                     | 1️⃣ Download · 2️⃣ Paste into any LLM chat · 3️⃣ Type “hello world” — OS boots instantly |

---

### 🧭 Explore More

| Module                   | Description                                                                  | Link                                                                                               |
| ------------------------ | ---------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| WFGY Core                | WFGY 2.0 engine is live: full symbolic reasoning architecture and math stack | [View →](https://github.com/onestardao/WFGY/tree/main/core/README.md)                              |
| Problem Map 1.0          | Initial 16-mode diagnostic and symbolic fix framework                        | [View →](https://github.com/onestardao/WFGY/tree/main/ProblemMap/README.md)                        |
| Problem Map 2.0          | RAG-focused failure tree, modular fixes, and pipelines                       | [View →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md) |
| Semantic Clinic Index    | Expanded failure catalog: prompt injection, memory bugs, logic drift         | [View →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/SemanticClinicIndex.md)           |
| Semantic Blueprint       | Layer-based symbolic reasoning & semantic modulations                        | [View →](https://github.com/onestardao/WFGY/tree/main/SemanticBlueprint/README.md)                 |
| Benchmark vs GPT-5       | Stress test GPT-5 with full WFGY reasoning suite                             | [View →](https://github.com/onestardao/WFGY/tree/main/benchmarks/benchmark-vs-gpt5/README.md)      |
| 🧙‍♂️ Starter Village 🏡 | New here? Lost in symbols? Click here and let the wizard guide you through   | [Start →](https://github.com/onestardao/WFGY/blob/main/StarterVillage/README.md)                   |

---

> 👑 **Early Stargazers: [See the Hall of Fame](https://github.com/onestardao/WFGY/tree/main/stargazers)** —
> Engineers, hackers, and open source builders who supported WFGY from day one.

> <img src="https://img.shields.io/github/stars/onestardao/WFGY?style=social" alt="GitHub stars"> ⭐ [WFGY Engine 2.0](https://github.com/onestardao/WFGY/blob/main/core/README.md) is already unlocked. ⭐ Star the repo to help others discover it and unlock more on the [Unlock Board](https://github.com/onestardao/WFGY/blob/main/STAR_UNLOCKS.md).

<div align="center">

[![WFGY Main](https://img.shields.io/badge/WFGY-Main-red?style=flat-square)](https://github.com/onestardao/WFGY)
 
[![TXT OS](https://img.shields.io/badge/TXT%20OS-Reasoning%20OS-orange?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS)
 
[![Blah](https://img.shields.io/badge/Blah-Semantic%20Embed-yellow?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlahBlahBlah)
 
[![Blot](https://img.shields.io/badge/Blot-Persona%20Core-green?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlotBlotBlot)
 
[![Bloc](https://img.shields.io/badge/Bloc-Reasoning%20Compiler-blue?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlocBlocBloc)
 
[![Blur](https://img.shields.io/badge/Blur-Text2Image%20Engine-navy?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlurBlurBlur)
 
[![Blow](https://img.shields.io/badge/Blow-Game%20Logic-purple?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlowBlowBlow)
 

</div>
