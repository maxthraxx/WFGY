# Feature Flags and Safe Launch — OpsDeploy Guardrails

Ship new prompts, models, retrievers, tools, or index pointers without surprises. This page shows how to scope flags, gate traffic with measurable targets, and roll forward only when the canary stays green.

---

## Open these first
- Readiness gate: [rollout_readiness_gate.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/rollout_readiness_gate.md)
- Canary staging: [staged_rollout_canary.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/staged_rollout_canary.md)
- Blue green cutover: [blue_green_switchovers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/blue_green_switchovers.md)
- Version locking: [version_pinning_and_model_lock.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/version_pinning_and_model_lock.md)
- Cache and invalidation: [cache_warmup_invalidation.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/cache_warmup_invalidation.md)
- Limits under load: [rate_limit_backpressure.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/rate_limit_backpressure.md)
- Ordering and boot fences: [bootstrap-ordering.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md)
- Schema contracts and traceability: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md), [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)

---

## When to use
- New prompt pack or header order.  
- LLM provider or model change.  
- Retriever, chunker, reranker, store, or metric change.  
- Index pointer or alias swap.  
- Tool schema or protocol change.

---

## Acceptance targets for a flag to graduate
- ΔS drift vs baseline: median ≤ 0.03 and p95 ≤ 0.10 on the gold set.  
- Coverage to the target section ≥ 0.70.  
- λ remains convergent across 3 paraphrases and 2 seeds.  
- p95 latency within +15 percent of baseline. Error rate ≤ 0.5 percent. Tool success ≥ 99 percent.  
- Cost per solved query within +10 percent or show a clear quality gain.

---

## 60-second launch plan
1) **Define the flag and scope**  
   Scope by tenant, cohort, product surface, region, or endpoint. Never rely on client only flags.
2) **Pin versions behind the flag**  
   MODEL_VER, PROMPT_VER, INDEX_HASH, RERANK_CONF, TOK_VER, ANALYZER_CONF. See [version_pinning_and_model_lock.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/version_pinning_and_model_lock.md).
3) **Warm the cache for the flagged arm**  
   Use versioned keys and a gold set warmup. See [cache_warmup_invalidation.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/cache_warmup_invalidation.md).
4) **Start at shadow or 5 percent**  
   Compare to a pinned baseline. Hold for one evaluation window.  
5) **Graduate stepwise**  
   5 to 25 to 50 to 100 percent if all targets stay green. Else stop and roll back.

---

## Flag taxonomy and use
- **Kill switch**  
  Immediate global off for a risky module or tool. Server evaluated.
- **Progressive rollout**  
  Traffic weights per tenant or region with hold times and abort gates.
- **Quality gated flag**  
  Opens only when ΔS, coverage, and λ are inside bounds for the current window.
- **Safety guard**  
  Allows cite only output if reason step fails. Protects CX while investigating.
- **Cost guard**  
  Caps heavy chains. Falls back when cost per solved query exceeds budget.

---

## YAML manifest template
```yaml
# opsdeploy/flags/feature_flags.yml
flags:
  prompt_pack_vNplus1:
    scope:
      tenants: ["all"]            # or a list of tenant ids
      regions: ["us-east-1"]      # stage per region
      endpoints: ["/rag/reason"]
    versions:
      MODEL_VER: "gpt-4o-2025-07-15"
      PROMPT_VER: "p-2025.08.31-h1"
      INDEX_HASH: "b7f3..."
      RERANK_CONF: "bge-rerank-v2@top32"
    traffic:
      baseline_weight: 0.95
      canary_weight: 0.05
    gates:
      delta_s:
        median_max: 0.03
        p95_max: 0.10
      coverage_min: 0.70
      lambda_convergent: true
      latency_p95_uplift_max: 0.15
      error_rate_max: 0.005
      tool_success_min: 0.99
      cost_uplift_max: 0.10
    abort_rules:
      hard:
        - kind: "delta_s_p95_over"
          value: 0.15
        - kind: "coverage_under"
          value: 0.60
        - kind: "lambda_flip_rate_over"
          value: 0.20
        - kind: "error_rate_over"
          value: 0.01
      soft:
        - kind: "latency_p95_over_budget"
        - kind: "cost_per_solved_over_budget"
````

---

## Server side evaluation snippet

```python
def pass_gates(metrics, targets):
    if metrics["ds_median"] > targets["delta_s"]["median_max"]: return False
    if metrics["ds_p95"]    > targets["delta_s"]["p95_max"]:    return False
    if metrics["coverage"]  < targets["coverage_min"]:          return False
    if not metrics["lambda_convergent"] and targets["lambda_convergent"]: return False
    if metrics["latency_p95_uplift"] > targets["latency_p95_uplift_max"]:  return False
    if metrics["error_rate"] > targets["error_rate_max"]: return False
    if metrics["tool_success"] < targets["tool_success_min"]: return False
    if metrics["cost_uplift"] > targets["cost_uplift_max"]: return False
    return True
```

---

## Observability you must log

* Exposure events with assignment keys and sticky sampling id.
* Version pins on every request.
* ΔS, coverage, λ states, latency, error, tool success, cost.
* Gate decisions and the reason for pass or fail.
* Abort triggers with the exact rule that fired.

---

## Symptom to fix map

| Symptom                            | Likely cause                               | Open this                                                                                                                                                                                                                                                                                          |
| ---------------------------------- | ------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Users bounce between arms          | no sticky sampling or client only flags    | [staged\_rollout\_canary.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/staged_rollout_canary.md)                                                                                                                                                              |
| Mixed answers across versions      | cache keys not partitioned by version pins | [cache\_warmup\_invalidation.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/cache_warmup_invalidation.md)                                                                                                                                                      |
| Quality regresses after graduation | pins drifted or alias flipped mid window   | [version\_pinning\_and\_model\_lock.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/version_pinning_and_model_lock.md), [blue\_green\_switchovers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/blue_green_switchovers.md) |
| 429 storm during ramp              | retry stampede or no global cap            | [rate\_limit\_backpressure.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/rate_limit_backpressure.md)                                                                                                                                                          |
| Tool loops under the flag          | side effects not fenced                    | [idempotency\_dedupe.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/idempotency_dedupe.md)                                                                                                                                                                     |

---

## Common pitfalls

* Client toggles treated as truth. Always evaluate on the server with signed manifests.
* Two versions live without cache namespace separation.
* Region flags diverge and never converge. Roll by region with audit hashes.
* Graduation without a pinned baseline or a stable eval window.

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

