# Stateless KV and Queue Patterns — Guardrails

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **Cloud_Serverless**.  
  > To reorient, go back here:  
  >
  > - [**Cloud_Serverless** — scalable functions and event-driven pipelines](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>


A compact repair guide for serverless and edge stacks that must survive retries, bursts, out-of-order events, and duplicate webhooks. All patterns map back to Problem Map pages with measurable targets.

## When to use this page

* Functions are stateless and scale horizontally.
* You see duplicate side effects on retries or webhook storms.
* Event order is not guaranteed and you must reconcile late arrivals.
* Writes cross multiple systems and need exactly-once semantics in practice.
* You need queues for backpressure without introducing deadlocks.

## Open these first

* Visual recovery map: [rag-architecture-and-recovery.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
* Contracts for small, auditable payloads: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
* Live ops and tracing: [ops/live\_monitoring\_rag.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md) · [ops/debug\_playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md)
* Boot order and deploy hazards: [bootstrap-ordering.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md) · [deployment-deadlock.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md) · [predeploy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)
* Storm control pattern: [patterns/pattern\_bootstrap\_deadlock.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_bootstrap_deadlock.md)

## Acceptance targets

* Duplicate side-effects ≤ 0.1 percent across 1 million events.
* P99 queue latency ≤ 5 seconds after backpressure is active.
* Lock contention ≤ 3 percent with P95 wait ≤ 100 ms.
* Exactly-once at the boundary: user-visible action never applied twice even with three retries.
* Audit fields present on every message: `event_id`, `source_id`, `revision`, `index_hash`, `dedupe_key`, `attempt`.

---

## Fix in 60 seconds

1. **Define the dedupe key**
   `dedupe_key = sha256(source_id + revision + index_hash)`
   Store in `kv/done/<dedupe_key> = {ts, status, result_id}` with TTL ≥ max replay window.
   Contract: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

2. **Use a leased lock for single-writer sections**
   `kv/lock/<resource>` with value `token` and `ttl = function_timeout - safety_margin`.
   Only the holder token can release. On expiry, another worker may acquire.

3. **Put work behind a queue with visibility timeout**
   Visibility timeout must be greater than `max_processing_time + jitter`. Failed items go to DLQ after `N` attempts. Record `attempt` in the message.

4. **Outbox before publish**
   Write business record and `outbox/<txid>` in the same atomic store.
   A relay process reads the outbox and publishes to the queue.
   Consumers use `inbox/<txid>` as the dedupe ledger.

5. **Idempotent side-effects**
   Before any external call, check `kv/done/<dedupe_key>`.
   If present, return the prior result. If absent, perform the effect then write the ledger.

---

## Typical breakpoints → exact fix

* **Webhook storms and double billing**
  Missing dedupe ledger or TTL too short. Add `kv/done/<dedupe_key>` with long TTL and verify before charge.
  Open: [ops/live\_monitoring\_rag.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md)

* **Queue grows without bound**
  No backpressure or priority lanes. Add consumption quotas per tenant and a high-watermark shed rule.
  Open: [ops/debug\_playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md)

* **Deadlocks when multiple writers compete**
  Locks without leases or cross-locks across resources. Replace with single resource lock per critical section and time-boxed lease.
  Open: [deployment-deadlock.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md)

* **Out-of-order events overwrite newer state**
  Apply a monotonic guard: reject if `revision_in_msg < current_revision`. Keep a compaction job to expire stale inbox entries.
  Open: [bootstrap-ordering.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md)

---

## Minimal recipes you can copy

### A) Leased lock with safe release

```txt
acquire(key, ttl):
  token = random()
  ok = kv.setnx("lock/"+key, token, ttl)
  return ok ? token : null

release(key, token):
  if kv.get("lock/"+key) == token:
    kv.del("lock/"+key)
```

### B) Idempotency ledger

```txt
dedupe_key = sha256(source_id + revision + index_hash)

if kv.get("done/"+dedupe_key):
  return replay(kv.get("done/"+dedupe_key))

result = do_side_effect()
kv.set("done/"+dedupe_key, {ts: now(), result_id: result.id}, ttl=30d)
return result
```

### C) Outbox and inbox

```txt
// producer tx
db.begin()
db.insert("orders", row)
db.insert("outbox", {txid, payload})
db.commit()

// relay
for msg in db.scan("outbox"):
  queue.send({txid, payload})
  db.delete("outbox", msg.txid)

// consumer
if kv.get("inbox/"+txid): return
handle(payload)
kv.set("inbox/"+txid, now(), ttl=30d)
```

### D) Token bucket for backpressure

```txt
bucket = "q_tokens/"+tenant
tokens = kv.incrby(bucket, 1, ttl=1s)
if tokens > limit: requeue_with_delay()
```

---

## Observability you must add

* `queue_depth`, `age_of_oldest`, `consume_rate`, `requeue_rate`, `dlq_rate`.
* `lock_acquired`, `lock_conflicts`, `lock_wait_ms_p95`.
* `dedupe_hits`, `double_effects_detected`.
* Trace fields on every event: `event_id`, `dedupe_key`, `attempt`, `tenant`, `route`.

## Verification

* Fire a test that sends the same event 5 times with random delays. Only one side-effect is applied.
* Kill a worker mid-flight. Message becomes visible again and finishes once.
* Reorder by sending `revision=1,3,2`. State ends at 3.
  Open: [eval/eval\_rag\_precision\_recall.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/eval/eval_rag_precision_recall.md)

## When to escalate

* If locks create long waits or cascades, redesign the critical section into outbox plus eventual reconciliation.
* If queue depth oscillates, split lanes by priority or tenant and apply quotas.
  Open: [ops/live\_monitoring\_rag.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md)

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
