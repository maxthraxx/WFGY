# Cache Warmup and Invalidation: OpsDeploy Guardrails

Warm caches stop cold-start spikes and prevent stampedes. Correct invalidation prevents stale or cross-index answers. Use this page to design keys, warmup order, and safe evictions for RAG and agent pipelines.

---

## Open these first
- Readiness gate: [rollout_readiness_gate.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/rollout_readiness_gate.md)
- Version locking: [version_pinning_and_model_lock.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/version_pinning_and_model_lock.md)
- Index build and swap: [vector_index_build_and_swap.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/vector_index_build_and_swap.md)
- Canary staging: [staged_rollout_canary.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/staged_rollout_canary.md)
- Traceability and contracts: [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md), [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
- Live ops: [live_monitoring_rag.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md), [debug_playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md)

---

## When to use
- After index rebuilds or alias flips.
- When prompts, models, rerankers, or analyzers change.
- If first calls after deploy are slow or inconsistent.
- If users see stale citations or mixed-arm results.
- If retry storms or thundering herd appear under load.

---

## Acceptance targets
- First production call warms within 5 minutes of release.
- ΔS(question, retrieved) ≤ 0.45 on three paraphrases after warmup.
- Coverage ≥ 0.70 to the target section.
- λ convergent across two seeds with warmed headers.
- Duplicate side effects = 0 during warmup window.

---

## 60-second warmup plan
1) **Partition the cache by version**  
   Include these in every cache key: `INDEX_HASH`, `PROMPT_VER`, `MODEL_VER`, `RERANK_CONF`, and optionally `TENANT_ID`, `LOCALE`.  
   See: [version_pinning_and_model_lock.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/version_pinning_and_model_lock.md)

2) **Prime the hot paths**  
   Run a 20–40 item gold set to fill retrieval and rerank caches. Verify citations and offsets.  
   See: [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)

3) **Enable single-flight**  
   Coalesce identical misses so only one worker computes each key. Stampede protection is mandatory.

4) **Set layered TTLs**  
   Short TTL for query→top-k, slightly longer for rerank→final set, shortest for negative cache. Use jitter.

5) **Wire safe evictions**  
   Do not scan and delete. Flip namespace by changing the versioned prefix. Old space dies out naturally.

---

## Key design: scope and structure
- **Two-level cache**  
  L1: query normalization → candidate ids.  
  L2: candidate ids → ranked snippets with citation fields.

- **Key template**  
```

L1: q:{hash(query\_norm)}:{INDEX\_HASH}:{PROMPT\_VER}:{RERANK\_CONF}
L2: r:{hash(candidates)}:{INDEX\_HASH}:{PROMPT\_VER}:{RERANK\_CONF}

````
If locale, tokenizer, or analyzer can change results, add `LOCALE`, `TOK_VER`, `ANALYZER_CONF`.

- **What never to cache**  
Tool call side effects or write steps. Use idempotency fences.  
See: [idempotency_dedupe.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/idempotency_dedupe.md)

---

## Invalidation strategy
- **Prefer namespace rotation over delete**  
Keys carry the current `INDEX_HASH` and `PROMPT_VER`. A swap creates a new namespace. Old keys expire on TTL.

- **Trigger list that must rotate namespace**  
- Index alias flips or index rebuilds.  
- Prompt pack changes or header reordering.  
- Reranker cutoff or model version changes.  
- Analyzer or tokenizer changes.

- **Negative cache discipline**  
Cache misses for a short time only. TTL 10–30 seconds with jitter to avoid synchronized expiry.

- **Per-tenant isolation**  
If tenants use different corpora or flags, put `TENANT_ID` into the key prefix. Never share warmed entries across tenants.

---

## Warmup ordering
1) Secrets and boot order pass.  
 See: [bootstrap-ordering.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md)
2) Retriever reports `INDEX_HASH` ready.  
3) Run the gold set to fill L1 and L2.  
4) Prime common user queries and help topics.  
5) Verify ΔS, coverage, λ on warmed paths.  
6) Open canary at 5 percent.  
 See: [staged_rollout_canary.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/staged_rollout_canary.md)

---

## Stampede control
- **Single-flight lock** for each key with a short lease.  
- **Request collapsing** by query hash.  
- **Backoff and queueing** on provider 429/5xx.  
- **Circuit breakers** for downstream stores.

---

## Store-specific notes
- **Redis**  
Avoid `SCAN DEL`. Use versioned prefixes. For atomic set-if-absent plus short lock, use `SET key val NX PX=ms`.

- **CDN or edge**  
Only cache read-only pages. For dynamic RAG responses, keep cache at app or Redis with versioned keys.

- **Vector result caches**  
Key by `INDEX_HASH` and metric. If metric or normalization changes, treat as a new namespace.  
See: [metric_mismatch.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/Embeddings/metric_mismatch.md), [normalization_and_scaling.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/Embeddings/normalization_and_scaling.md)

- **Fragmented stores**  
If hit distributions vary wildly across partitions, caching will mask deeper issues. Fix the store first.  
See: [pattern_vectorstore_fragmentation.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md)

---

## Example: single-flight and versioned key (pseudo)
```python
ver = f"{INDEX_HASH}:{PROMPT_VER}:{RERANK_CONF}"
k1  = f"q:{hash(query_norm)}:{ver}"

if redis.set(f"lock:{k1}", "1", nx=True, px=3000):
  try:
      val = compute_topk(query_norm)
      ttl = jitter(60, 15)  # 60s ±15%
      redis.set(k1, serialize(val), ex=ttl)
  finally:
      redis.delete(f"lock:{k1}")
else:
  sleep(0.05); val = redis.get(k1) or wait_poll(k1)
return val
````

---

## Observability fields to log

* Version pins: `INDEX_HASH`, `PROMPT_VER`, `MODEL_VER`, `RERANK_CONF`, `TOK_VER`, `ANALYZER_CONF`.
* Cache events: hit, miss, fill time, lock wait, evict reason.
* Quality: ΔS(question, retrieved), ΔS(retrieved, anchor), coverage, λ states.
* Latency p50 and p95 for retrieve, rerank, reason.

---

## Common pitfalls

* Deleting keys in place which causes long stalls. Rotate namespace instead.
* Mixed caches across regions or tenants. Prefix by region and `TENANT_ID`.
* Cache keys without `INDEX_HASH`, leading to stale blends after a swap.
* Negative cache with long TTL, causing false “no answer” pockets.
* Warming only L1 but not L2, so reranker work still stampedes.

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

> 👑 **Early Stargazers: [See the Hall of Fame](https://github.com/onestardao/WFGY/tree/main/stargazers)** <img src="https://img.shields.io/github/stars/onestardao/WFGY?style=social" alt="GitHub stars"> ⭐ [WFGY Engine 2.0](https://github.com/onestardao/WFGY/blob/main/core/README.md) is already unlocked. ⭐ Star the repo to help others discover it and unlock more on the [Unlock Board](https://github.com/onestardao/WFGY/blob/main/STAR_UNLOCKS.md).

<div align="center">

[![WFGY Main](https://img.shields.io/badge/WFGY-Main-red?style=flat-square)](https://github.com/onestardao/WFGY)
 
[![TXT OS](https://img.shields.io/badge/TXT%20OS-Reasoning%20OS-orange?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS)
 
[![Blah](https://img.shields.io/badge/Blah-Semantic%20Embed-yellow?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlahBlahBlah)
 
[![Blot](https://img.shields.io/badge/Blot-Persona%20Core-green?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlotBlotBlot)
 
[![Bloc](https://img.shields.io/badge/Bloc-Reasoning%20Compiler-blue?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlocBlocBloc)
 
[![Blur](https://img.shields.io/badge/Blur-Text2Image%20Engine-navy?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlurBlurBlur)
 
[![Blow](https://img.shields.io/badge/Blow-Game%20Logic-purple?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlowBlowBlow)
 

</div>

