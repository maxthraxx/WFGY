# Rate Limit and Backpressure — OpsDeploy Guardrails

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **OpsDeploy**.  
  > To reorient, go back here:  
  >
  > - [**OpsDeploy** — operations automation and deployment pipelines](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>


Keep your pipeline stable under load. This page gives concrete limits, retry rules, and queuing patterns that prevent 429 storms, tail spikes, and cascading failure. Store and model agnostic.

---

## Open these first
- Readiness gate: [rollout_readiness_gate.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/rollout_readiness_gate.md)
- Canary staging: [staged_rollout_canary.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/staged_rollout_canary.md)
- Boot and index state: [bootstrap-ordering.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md), [vector_index_build_and_swap.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/vector_index_build_and_swap.md)
- Cache discipline: [cache_warmup_invalidation.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/cache_warmup_invalidation.md)
- Idempotent fences: [idempotency_dedupe.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/idempotency_dedupe.md)
- Live ops: [live_monitoring_rag.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md), [debug_playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md)

---

## Acceptance targets
- 429 rate ≤ 0.5% per minute at steady state. Burst window p95 ≤ 2%.  
- Queue wait p95 ≤ 200 ms for read paths. Write paths use deadlines not exceeding 1× p95 service time.  
- End to end p95 latency within +15% of baseline when limiters are active.  
- Drop rate = 0 for idempotent endpoints and exactly-once jobs.  
- ΔS(question, retrieved) ≤ 0.45 and coverage ≥ 0.70 remain stable while throttled. λ stays convergent across 2 seeds.

---

## 60-second stabilization plan
1) **Admission control**  
   Set hard concurrency caps per endpoint and per tenant. Keep avg utilization near 0.7 under peak.
2) **Token bucket on read paths**  
   Rate r, burst b. Use per-tenant buckets and a global bucket. Enforce at edge and at service.
3) **Leaky queue with deadlines**  
   Put a deadline on each request. If queue wait exceeds deadline, fail fast with a retry hint.
4) **Retries with full jitter**  
   Exponential backoff with randomization. Honor provider Retry-After when present.
5) **Circuit breaker**  
   Open on consecutive errors or saturation. Shed load and degrade features instead of timing out.

---

## Patterns

### Token bucket in Redis (pseudo)
```python
def take(bucket, now, rate, burst):
    # bucket: {tokens, last_ts}
    b = redis.hgetall(bucket) or {"tokens": burst, "last_ts": now}
    delta = max(0, now - float(b["last_ts"]))
    tokens = min(burst, float(b["tokens"]) + rate * delta)
    if tokens < 1:
        return False
    pipe = redis.pipeline()
    pipe.hset(bucket, mapping={"tokens": tokens - 1, "last_ts": now})
    pipe.expire(bucket, 3600)
    pipe.execute()
    return True
````

### Backoff with full jitter (pseudo)

```python
def backoff(retry, base=0.25, cap=10.0):
    import random, math
    return random.random() * min(cap, base * (2 ** retry))
```

### Nginx edge limiter (example)

```nginx
limit_req_zone $binary_remote_addr zone=wfgy_rps:10m rate=20r/s;
server {
  location /api {
    limit_req zone=wfgy_rps burst=40 nodelay;
    proxy_pass http://wfgy_upstream;
  }
}
```

### Priority and fairness

* Two lanes: interactive queries vs batch jobs. Assign separate buckets.
* Per-tenant fairness: bucket per tenant plus a shared global bucket.
* Cost-aware limits: heavier chains consume more tokens.

### Degrade strategies

* Reduce chain length or switch to cached answer if queue wait exceeds threshold.
* Lower k or skip rerank under pressure.
* Return cite-only with links when reason step exceeds deadline.

---

## Symptom to fix map

| Symptom                       | Likely cause                                     | Open this                                                                                                                                                 |
| ----------------------------- | ------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 429 spikes after deploy       | missing jitter, shared retry stampede            | [cache\_warmup\_invalidation.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/cache_warmup_invalidation.md)             |
| Tail latency p99 explodes     | unbounded concurrency or queue with no deadlines | [staged\_rollout\_canary.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/staged_rollout_canary.md)                     |
| Mixed answers across versions | cache keys not partitioned by `INDEX_HASH`       | [version\_pinning\_and\_model\_lock.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/version_pinning_and_model_lock.md) |
| Duplicate side effects        | no idempotency fences under retry                | [idempotency\_dedupe.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/idempotency_dedupe.md)                            |
| Cascading failures to stores  | no circuit breaker or bulkhead                   | [debug\_playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md)                                                       |

---

## Observability you must log

* Per endpoint: tokens remaining, throttle events, 429 count, queue depth, wait time, service time.
* Per tenant: admissions vs evictions, burst usage, fairness ratio.
* Quality under pressure: ΔS, coverage, λ states.
* Retry metrics: attempts, Retry-After adherence, success after retry.

---

## Policy template you can paste

```yaml
# opsdeploy/limits.yml
limits:
  default:
    rps: 20
    burst: 40
    concurrent: 64
    deadline_ms: 2000
    backoff:
      base_s: 0.25
      cap_s: 10
      jitter: full
  endpoints:
    /rag/retrieve:
      rps: 50
      burst: 100
      concurrent: 128
      deadline_ms: 800
    /rag/reason:
      rps: 20
      burst: 40
      concurrent: 64
      deadline_ms: 2000
  tenants:
    premium: { multiplier: 2.0 }
    free:    { multiplier: 0.5 }
decision:
  shed_when:
    queue_wait_p95_ms: 300
    error_rate: 0.01
```

---

## Rollback rule

If 429 rate stays above 2% for one full evaluation window or tail latency p99 exceeds 2× baseline, shed load, open the breaker, and roll back to previous version or index pointer. Then follow the [debug\_playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md).

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

