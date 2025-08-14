# Live monitoring & alerting — RAG services

**Goal:** list of recommended metrics, alert rules and dashboard panels to keep RAG pipelines observable and actionable.

---

## Core metrics to collect (recommended names)

**Service-level**
- `rag_e2e_latency_seconds` (histogram) — E2E latency (request in → answer out)  
- `rag_error_count_total` — errors per endpoint  
- `rag_request_count_total` — total requests

**Retrieval-level**
- `retriever_qps_total`  
- `retriever_retrieved_docs_count` (per request)  
- `retriever_empty_result_count_total` — unexpected empty sets

**Vectorstore**
- `vectorstore_index_load_time_seconds`  
- `vectorstore_memory_bytes`  
- `vectorstore_indexed_docs_total`

**Accuracy/provenance**
- `rag_citation_hit_rate` (CHR gauge over sliding window)  
- `rag_precision_shipped` (periodic batch scorer push)  
- `rag_under_refusal_count_total`

**Infrastructure**
- `llm_api_rate_limited_total`  
- `llm_api_error_total`  
- `queue_backlog_count` (if using background queues)

---

## Suggested PromQL alerts (examples)

> Tune thresholds to your workload.

**A) Latency breach (interactive)**
```yaml
alert: RAGHighP95Latency
expr: histogram_quantile(0.95, sum(rate(rag_e2e_latency_seconds_bucket[5m])) by (le,instance)) > 2
for: 5m
labels:
  severity: page
annotations:
  summary: "RAG p95 > 2s ({{ $labels.instance }})"
````

**B) Error spike**

```yaml
alert: RAGErrorSpike
expr: increase(rag_error_count_total[5m]) > 50
for: 2m
labels: { severity: page }
```

**C) Retriever empty results**

```yaml
alert: RetrieverEmptyResults
expr: increase(retriever_empty_result_count_total[5m]) > 1
for: 5m
labels: { severity: ticket }
```

**D) CHR drop**

```yaml
alert: CHRDrop
expr: rag_citation_hit_rate < 0.6
for: 10m
labels: { severity: ticket }
```

**E) LLM auth failure**

```yaml
alert: LLMAuthFail
expr: increase(llm_api_error_total{code="401"}[5m]) > 0
for: 1m
```

---

## Dashboard panels (recommended)

1. E2E latency (p50/p95/p99) trend.
2. Requests per second and error rate.
3. Retriever QPS, avg retrieved docs, empty results.
4. CHR & Precision (batch scorer push).
5. Vectorstore memory & disk IO.
6. LLM provider error & rate-limit metrics.

---

## Incident play (fast actions)

1. If CHR drop → run **diagnostic retrieval** for 10 golden queries (retrieved ids + cosine scores).
2. If retriever empty → check vectorstore health and index partitions. Restart index shard if needed.
3. If E2E latency spike with LLM errors → throttle traffic, put a hard rate limit and rollback deploy if needed.
4. If LLM auth failure → rotate key & redeploy secrets.

---

## How to integrate scoring metrics

* Periodic scorer job should push `rag_citation_hit_rate` and `rag_precision_shipped` as a short-timeseries gauge (per 5–15m window).
* Use batching: run `score_eval.py` (see `ProblemMap/eval/README.md`) nightly and push summary metrics via a small exporter.

---

## Troubleshooting queries (prometheus examples)

* Check p95 per instance:

  ```promql
  histogram_quantile(0.95, sum(rate(rag_e2e_latency_seconds_bucket[5m])) by (le,instance))
  ```
* CHR trend:

  ```promql
  avg_over_time(rag_citation_hit_rate[30m])
  ```

---

### Links

* Deployment checklist → [deployment\_checklist.md](./deployment_checklist.md)
* Debug playbook → [debug\_playbook.md](./debug_playbook.md)
* Eval & scoring → [../eval/README.md](../eval/README.md)

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


