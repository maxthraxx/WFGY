# Rollback and Fast Recovery — OpsDeploy Guardrails

Bring production back to a good state fast. This page gives you the exact levers and a 60-second checklist to reverse a bad rollout, recover service, and preserve data integrity.

---

## Open these first
- Canary staging: [staged_rollout_canary.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/staged_rollout_canary.md)
- Blue green cutover: [blue_green_switchovers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/blue_green_switchovers.md)
- Version fences: [version_pinning_and_model_lock.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/version_pinning_and_model_lock.md)
- Index swap: [vector_index_build_and_swap.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/vector_index_build_and_swap.md)
- Feature flags: [feature_flags_safe_launch.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/feature_flags_safe_launch.md)
- Rate and retry: [rate_limit_backpressure.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/rate_limit_backpressure.md), [retry_backoff.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/retry_backoff.md)
- Cache and dedupe: [cache_warmup_invalidation.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/cache_warmup_invalidation.md), [idempotency_dedupe.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/idempotency_dedupe.md)
- First-run traps: [bootstrap-ordering.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md), [deployment-deadlock.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md), [predeploy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)
- Live ops: [live_monitoring_rag.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md), [debug_playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md)

---

## When to pull this page
- ΔS drift p95 over 0.15 or coverage under 0.60 on the canary window.  
- λ flips rise above 0.20 or tool loops detected.  
- 5xx over 1 percent or 429 storms that do not subside with backoff.  
- p99 latency doubles, cache poisoning, mixed answers across versions.  
- Suspicion of duplicate side effects or index mismatch.

---

## Recovery exit targets
- User visible error rate back under 0.5 percent within ten minutes.  
- ΔS and coverage match the pinned baseline window.  
- p95 latency within plus 15 percent of baseline.  
- Duplicate side effects equal zero during and after rollback.

---

## 60-second rollback checklist
1) **Capture state**  
   Dump `BUILD_ID`, `GIT_SHA`, `MODEL_VER`, `PROMPT_VER`, `INDEX_HASH`, `RERANK_CONF`, `TOK_VER`, `ANALYZER_CONF`, sample ΔS and coverage. Keep for the postmortem.
2) **Freeze writes**  
   Pause non-idempotent writers and queue consumers. Confirm fences are active. See [idempotency_dedupe.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/idempotency_dedupe.md).
3) **Pick the fastest lever**  
   - Feature flag kill switch  
   - Blue to Green pointer back to Blue  
   - Index alias from `docs_vB` back to `docs_vA`  
   - Version unpin to the last known good set
4) **Flip one pointer**  
   Single operation. DNS or Ingress or alias or service selector. See the blue green and index swap pages.
5) **Rotate cache namespace**  
   Keys must include `INDEX_HASH` and `PROMPT_VER`. Do not delete in place. See cache page.
6) **Throttling on**  
   Global token budget and circuit breaker while the system cools. See rate and retry pages.
7) **Watch for green**  
   Hold ten to fifteen minutes. Confirm targets are met. Then unfreeze writers.

---

## Rollback decision tree
- **Quality regression**  
  Revert prompt pack or model by flag, then warm cache and verify.  
- **Retriever wrong or mixed answers**  
  Alias index back to previous `docs_vA`. Keys rotate by `INDEX_HASH`.  
- **Hot cost or tail latency**  
  Degrade chain length, return cite only when deadline is tight, enforce global caps.  
- **Duplicate effects**  
  Block writes, enable fences, reconcile receipts, then reopen.

---

## Paste-ready snippets

### Kubernetes service selector flip
```yaml
apiVersion: v1
kind: Service
metadata: { name: wfgy-live }
spec:
  selector: { app: wfgy-blue }   # flip back to blue
  ports: [ { port: 80, targetPort: http } ]
````

### Vector index alias rollback

```bash
vec alias update docs_live --to docs_vA
```

### Feature flag kill switch

```yaml
# opsdeploy/flags/off.yml
flags:
  prompt_pack_vNplus1:
    traffic: { baseline_weight: 1.0, canary_weight: 0.0 }
    abort_rules:
      hard:
        - kind: "global_off"
```

---

## Fast recovery patterns

* **Degrade mode**
  Skip rerank, lower k, or return cite only with links.
* **Sticky routing**
  Keep users pinned to the same arm while the window stabilizes.
* **Single-flight**
  Collapse identical work on misses to avoid stampede.
* **Region by region**
  Roll back one region at a time with audit hashes.

---

## Post-rollback audit

* Verify the pins you expect are actually in logs for every request.
* Confirm cache namespace rotation took effect.
* Validate ΔS, coverage, λ on the warmed gold set.
* Reconcile any side effects created during the incident.
* Open the debug playbook and file the root cause link.

---

## Observability to pin

* Version pins and `INDEX_HASH` on every request.
* ΔS(question,retrieved) and ΔS(retrieved,anchor).
* Coverage and λ states.
* Error rates, 429, queue waits, breaker state.
* Side effect receipts and dedupe decisions.

---

## Common pitfalls

* Rolling back traffic without rotating cache namespace.
* Two writers active during the flip.
* Client only flags that drift from server reality.
* Forgetting to unfreeze jobs after stability returns.
* No captured evidence for the postmortem.

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
