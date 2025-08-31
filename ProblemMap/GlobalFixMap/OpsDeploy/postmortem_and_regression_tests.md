# Postmortem and Regression Tests — OpsDeploy Guardrails

Turn incidents into permanent fixes. This page gives a short postmortem template, evidence you must capture, and a drop-in regression suite so the same class of failure does not ship again.

---

## Open these first
- Rollout and canary: [rollout_readiness_gate.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/rollout_readiness_gate.md), [staged_rollout_canary.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/staged_rollout_canary.md)
- Cutovers: [blue_green_switchovers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/blue_green_switchovers.md), [vector_index_build_and_swap.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/vector_index_build_and_swap.md)
- Version and cache discipline: [version_pinning_and_model_lock.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/version_pinning_and_model_lock.md), [cache_warmup_invalidation.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/cache_warmup_invalidation.md)
- Stability under load: [rate_limit_backpressure.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/rate_limit_backpressure.md), [retry_backoff.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/retry_backoff.md)
- Side effects: [idempotency_dedupe.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/idempotency_dedupe.md)
- Rollback: [rollback_and_fast_recovery.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/rollback_and_fast_recovery.md)
- Live ops: [live_monitoring_rag.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md), [debug_playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md)

---

## When to run a postmortem
- ΔS drift p95 above 0.15 or coverage below 0.60 in any canary window.  
- λ flips above 0.20 or tool loops detected.  
- 5xx above 1 percent or sustained 429 storms.  
- Mixed answers across versions or index mismatch.  
- Duplicate side effects or data corruption risk.

---

## Exit targets after recovery
- Error rate below 0.5 percent within ten minutes.  
- ΔS and coverage match the last pinned baseline window.  
- p95 latency within plus 15 percent of baseline.  
- Duplicate side effects equal zero after reconciliation.

---

## Evidence you must capture
- Version pins: `BUILD_ID`, `GIT_SHA`, `MODEL_VER`, `PROMPT_VER`, `EMBED_MODEL_VER`, `EMBED_DIM`, `NORM`, `metric`, `RERANK_CONF`, `TOK_VER`, `ANALYZER_CONF`, `CHUNK_SCHEMA_VER`, `INDEX_HASH`.  
- Gold set window: ΔS(question,retrieved), ΔS(retrieved,anchor), coverage, λ states before and after.  
- Traffic weights or flags during the event.  
- Cache namespace keys that were active.  
- Side effect receipts and idempotency decisions.  
- Timeline of flips and breaker state.

---

## Root cause classifier
| Class | Typical sign | Primary fix page |
|---|---|---|
| Pin drift | answers change after silent provider update | [version_pinning_and_model_lock.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/version_pinning_and_model_lock.md) |
| Index swap error | mixed citations or stale blends | [vector_index_build_and_swap.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/vector_index_build_and_swap.md) |
| Cache namespace bug | cross-arm answers after cutover | [cache_warmup_invalidation.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/cache_warmup_invalidation.md) |
| Idempotency missing | duplicate writes or refunds | [idempotency_dedupe.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/idempotency_dedupe.md) |
| Load controls weak | 429 storms, tail spikes | [rate_limit_backpressure.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/rate_limit_backpressure.md), [retry_backoff.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/retry_backoff.md) |
| Boot ordering | first call fails after deploy | [bootstrap-ordering.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md) |
| Prompt regression | fluent but wrong citations | [rollout_readiness_gate.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/rollout_readiness_gate.md) |

---

## 60-second postmortem checklist
1) Lock recovery window and freeze writes for reconciliation.  
2) Capture all pins and the gold set metrics before and after the flip.  
3) Identify the first bad change and the last known good set.  
4) Classify the root cause using the table above.  
5) Attach the exact fix page link that prevents this class.  
6) Add a regression test that fails on the pre-fix build and passes on the fixed build.  
7) File owners and due dates. Publish within 48 hours.

---

## Postmortem template (paste-ready)
```markdown
# Incident <slug> · severity <S1..S4>
## Summary
One paragraph in plain language.

## Timeline
- <time> first alerts
- <time> rollback lever pulled
- <time> green window confirmed

## Blast radius and impact
Users affected, error rate, CX notes, cost impact.

## Evidence
Pins: MODEL_VER, PROMPT_VER, INDEX_HASH, RERANK_CONF, TOK_VER, ANALYZER_CONF  
Metrics: ΔS, coverage, λ, latency, 429, 5xx  
Flags and weights: what was on and where

## Root cause
Classifier: <from table>  
Primary mechanism: one paragraph

## What went well
Short bullets.

## What went wrong
Short bullets.

## Permanent fixes
- Link to exact WFGY fix page
- Config or code diff
- Owner and due date

## Regression tests added
List each new test and where it runs.

## Appendix
Raw logs, dashboards, receipts, diffs.
````

---

## Regression suite you should own

### Retrieval quality

* Gold set of 20 to 40 questions. Targets: ΔS(question,retrieved) ≤ 0.45 and coverage ≥ 0.70. λ convergent across two seeds.

### Prompt pack invariants

* Header checksum test. Fails when header order or critical clauses change without bumping `PROMPT_VER`.

### Embedding and metric guard

* Dimension, norm, and metric checks. Reject mismatches before index build.

### Reranker stability

* Deterministic top-k order for a frozen candidate set. Log p95 swap rate.

### Tokenizer and analyzer checks

* CJK and diacritics forms. Fullwidth and halfwidth. RTL punctuation. Compare token counts across builds.

### Index alias swap rehearsal

* Build docs\_vB offline and run head-to-head against docs\_vA. One operation flips alias and is reversible.

### Feature flags and rollout gates

* Simulated 5 to 25 to 50 to 100 percent ramp. Abort rules fire on ΔS p95, coverage, λ, error rate, latency.

### Rate limit and retry harness

* Token bucket and full jitter backoff. Ensure 429 p95 is below 2 percent in burst windows.

### Idempotency fences

* Webhook replay, API write retry, and consumer crash replay. Duplicate side effects equal zero.

### Cache versioning and warmup

* Keys must include `INDEX_HASH` and `PROMPT_VER`. Warm both L1 and L2. Negative cache TTL short with jitter.

### Cold start and boot order

* First call after deploy. Secrets ready, index mounted, health probe includes a gold QA.

### Rollback rehearsal

* Blue to Green and index alias back to A. Cache namespace rotates. System returns to baseline targets.

---

## CI manifest example

```yaml
# opsdeploy/regression_suite.yml
gates:
  retrieval:
    ds_max: 0.45
    coverage_min: 0.70
    lambda_convergent: true
  latency:
    p95_uplift_max: 0.15
  errors:
    rate_max: 0.005
invariants:
  pin_fields:
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
  forbid_mutation_during_rollout: true
scenarios:
  - name: index_alias_swap
    required: true
  - name: retry_replay_idempotency
    required: true
  - name: feature_flag_ramp
    required: true
decision:
  on_fail: block_rollout
  on_pass: ship
artifacts:
  - logs/regression_report.json
```

---

## Observability fields to pin for every run

* Version pins, flags, weights, and region.
* ΔS metrics, coverage, λ states.
* p50 and p95 latency per stage.
* 429 and 5xx counts, queue wait, breaker state.
* Dedupe decisions and effect receipts.

---

## Common pitfalls

* Postmortem without a regression test that fails first.
* No owner or due date on action items.
* Fix shipped without updating pins or cache namespace.
* Region divergences that never reconverge.
* Canary windows too short to detect drift.

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

