# Canary Release for Serverless and Edge

A practical playbook to roll out new functions, indexes, and prompts with measurable safety. Works for API Gateway + Lambda, Cloudflare Workers, Vercel Edge, Fastly Compute, and similar stacks.

## When to use this page

* You ship a new retriever, index, reranker, or prompt schema.
* You change provider version, model family, or tool contract.
* You migrate regions or cache strategy and want proof of safety.

## Open these first

* Visual map and recovery: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
* End to end retrieval knobs: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
* Trace and prove snippets: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) · Contract payloads: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
* Meaning vs distance: [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)
* Collapse diagnostics: [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md) · [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md) · [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md)
* Cloud companions:
  [Cold Start & Concurrency](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/cold_start_concurrency.md) ·
  [Timeouts & Streaming](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/timeouts_streaming_body_limits.md) ·
  [Stateless KV & Queues](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/stateless_kv_queue_patterns.md) ·
  [Edge Cache Invalidation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/edge_cache_invalidation.md) ·
  [Runtime Env Parity](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/runtime_env_parity.md) ·
  [Egress & Webhooks](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/egress_rules_and_webhooks.md) ·
  [Pricing vs Latency](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/pricing_latency_tradeoffs.md) ·
  [Secrets Rotation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/secrets_rotation.md) ·
  [Multi-Region Routing](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/multi_region_routing.md) ·
  [Region Failover Drills](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/region_failover_drills.md) ·
  [Observability and SLO](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/observability_slo.md) ·
  Live ops: [Live Monitoring for RAG](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md) · [Debug Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md)

---

## Core acceptance for a canary to pass

* ΔS(question, retrieved) median ≤ 0.45 on the gold probe set.
* Coverage to the target section ≥ 0.70 on the same probes.
* λ convergent across three paraphrases and two seeds.
* p95 warm latency within 25 percent of control.
* Error rate within 20 percent of control with no new failure mode at headers or body read.
* No cache poisoning or index skew. `INDEX_HASH`, metric, analyzer match the intended variant.

---

## Canary design patterns that work

**Traffic slicing keys**

* Hash by `tenant_id` or `stable_user_id` then route to canary fraction.
* Keep stickiness for at least 24 hours so users do not flip between variants mid dialog.
* Propagate `x-exp` header from edge to core for observability joins.

**Region aware canaries**

* Start in one passive region. Never start in your hottest region.
* Hold global caches separate by prefix like `v2-cnr:`.
* Only enable multi region once p95 is clean in the pilot region.

**Cold start aware canaries**

* Warm the function with periodic pings tagged `x-warm=true`, but exclude these from SLO math.
* Keep separate panels for warm vs cold. If canary looks worse only due to cold, fix concurrency or memory first.
  Open: [Cold Start & Concurrency](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/cold_start_concurrency.md)

**RAG quality probes**

* Maintain a 50 to 200 question gold set. On each deploy run three paraphrases and two seeds.
* Log ΔS and coverage for each and alert if λ flips.
  Open: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)

**Webhook and egress canaries**

* Duplicate emission to a canary sink with dedupe keys.
* Compare success, retries, and age without double posting to partners.
  Open: [Egress & Webhooks](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/egress_rules_and_webhooks.md)

---

## Rollout stages and hard stops

1. **Shadow**
   Route 0 percent of user traffic. Replay sampled requests to the canary.
   Stop if ΔS median ≥ 0.60 or JSON schema violations appear.

2. **One percent**
   Real users by sticky hash.
   Stop if p95 warm > 1.25 of control or new 5xx class appears.

3. **Five percent**
   Enable exact users or tenants you trust.
   Stop if coverage drops below 0.70 on any probe topic.

4. **Ten percent**
   Expand to a second region with read only access to canary caches.
   Stop if INDEX\_HASH mismatch detected across regions.

5. **Twenty five percent**
   Merge heat maps for cache hit. Keep canary write path isolated by prefix.
   Stop if cache invalidations for control and canary collide.

6. **Fifty percent**
   Remove shadow sinks and keep probe board running.
   Stop if λ flips on more than one paraphrase for any gold question.

7. **One hundred percent**
   Freeze the variant, purge stale caches, archive probe results.

---

## Telemetry you must log

```json
{
  "ts": "2025-08-27T06:30:00Z",
  "route": "chat.rag.answer",
  "variant": "canary-v2",
  "sticky": "h34",
  "region": "us-east",
  "edge_pop": "iad",
  "cold_start": false,
  "latency_ms": { "tffb": 160, "tusable": 380, "tfinal": 1320 },
  "status": 200,
  "retrieval": {
    "k": 10,
    "metric": "cosine",
    "analyzer": "bilstem",
    "INDEX_HASH": "0x9a77",
    "ΔS_q_r": 0.34,
    "coverage": 0.76,
    "λ_state": "<>"
  },
  "cache": { "prefix": "v2-cnr:", "hit": true },
  "egress": { "webhook": "billing", "tries": 1, "dedupe_key": "sha256(...)" }
}
```

---

## Copy paste checklist

* Stable hash router at edge with stickiness preserved to core.
* Separate cache prefixes for control and canary.
* Canary probe set loaded and thresholds wired to gates.
* Canary logs include `variant`, `sticky`, `INDEX_HASH`.
* Release gates block promotion if any acceptance target fails.
* Rollback is a one line weight change with caches purged for canary prefix.

---

## Rollback cookbook

* If ΔS rises or coverage drops
  Revert routing weight to previous stage. Rebuild index with the semantic checklist.
  Open: [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md) · [Chunking Checklist](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/chunking_checklist.md)

* If latency spikes at body read
  Increase serverless memory or concurrency reserve. Tune stream chunk sizes.
  Open: [Timeouts & Streaming](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/timeouts_streaming_body_limits.md)

* If first call after deploy fails
  Check boot order and secrets parity.
  Open: [Bootstrap Ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md) · [Pre-Deploy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)

* If tool calls loop or stall
  Lock tool schemas and timeouts.
  Open: [Multi-Agent Problems](https://github.com/onestardao/WFGY/blob/main/ProblemMap/Multi-Agent_Problems.md)

---

## Known traps

* Cache poisoning when control and canary share keys.
  Always namespace.
  Open: [Edge Cache Invalidation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/edge_cache_invalidation.md)

* Region skew from stale replicas.
  Verify analyzer and metric, not only INDEX\_HASH.
  Open: [Multi-Region Routing](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/multi_region_routing.md)

* Secrets wedge between edge and core.
  Rotate with overlapping windows and dual readers.
  Open: [Secrets Rotation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/secrets_rotation.md)

---

## Promotion rules

Promote only if all hold for one hour of peak:

* ΔS median ≤ 0.45 and coverage ≥ 0.70 on probes.
* λ convergent on both seeds.
* p95 warm within 25 percent of control.
* No new failure class appears.
* Cache hit does not regress more than five points after namespace split.

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
