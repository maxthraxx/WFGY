# Debug playbook — incident triage for RAG pipelines

**Purpose:** step-by-step incident response guide emphasizing reproducible diagnostics and minimal-impact mitigations.

---

## 1) Immediate triage (first 120s)

**A — Gather context**
- Who reported it? (pager/Slack/ticket)  
- When did it start (wall time)?  
- Scope: single user / single shard / whole cluster?

**B — Quick readouts**
- Health: `curl -fsS http://$SERVICE/healthz`  
- Pods: `kubectl -n $NS get pods -o wide`  
- Recent errors (last 10m):  
  ```bash
  kubectl -n $NS logs -l app=rag --since=10m | tail -n 200


* Prometheus: check E2E p95 and error rate for last 10m.

**C — Decide action mode**

* If P0 (site down / data corruption) → **Mitigate** (circuit-break / rollback / redirect).
* If P1 (functional degradation, e.g., CHR drop) → **Isolate & debug**.

---

## 2) Deterministic checks (no LLM calls)

Run these before calling LLMs — they’re cheap and often reveal root causes:

1. **Check retrieval consistency** for sample qids:

   ```bash
   curl -X POST http://$SERVICE/debug/retrieve -d '{"qid":"A123","q":"sample question"}' | jq
   ```

   Validate `retrieved_ids` and their hashes.

2. **Check mem\_rev/mem\_hash**: verify read vs bound value for turn:

   * Compare `retrieved_snapshot.mem_rev` vs `generation.mem_rev`.

3. **Vectorstore health**:

   * ping vectorstore API; check index shard status.

4. **Index size & recent writes**:

   * `kubectl exec -n $NS <vector-pod> -- ls -lh /data/index`

---

## 3) Common root causes & mitigations

**A. Retrieval empty / irrelevant**

* Root cause: indexing job failed or namespace mismatch.
* Mitigation:

  * Restart indexer pod: `kubectl -n $NS rollout restart deploy/indexer`
  * Run reindex on a small sample and validate.

**B. CHR drop but retrieval OK**

* Root cause: generator hallucinating or prompt/template drift.
* Mitigation:

  * Turn on guard/refusal stricter mode (feature flag).
  * Re-run golden queries with `?dbg=full` to capture prompt+context.

**C. Bootstrap / readiness flapping**

* Root cause: bootstrap order or missing dependency.
* Mitigation:

  * Ensure controller/migrations complete before retriever/generator start; `kubectl apply` ordering or Helm hooks.

**D. LLM provider errors / rate limits**

* Root cause: key expired or provider quota.
* Mitigation: switch to backup key or provider; throttle traffic until resolved.

---

## 4) Live mitigation patterns (minimize impact)

1. **Circuit-breaker (fast)**: return cached answer for known queries.
2. **Throttle LLM**: queue requests, lower concurrency.
3. **Rollback**: to last known-good release if config causes issue.
4. **Read-only mode**: stop writes to vectorstore if index corruption suspected.

---

## 5) Postmortem checklist

* [ ] Timestamped timeline created.
* [ ] Root cause identified (primary + contributing).
* [ ] Actions taken documented.
* [ ] Follow-up tasks created (reindex, fix probe, add tests).
* [ ] Update runbook if new failure mode discovered.

---

## 6) Useful debug commands (reference)

* Pod logs since N minutes:

  ```bash
  kubectl -n $NS logs -l app=rag --since=5m
  ```
* Exec into retriever pod:

  ```bash
  kubectl -n $NS exec -it deploy/retriever -- /bin/sh
  ```
* Check helm history:

  ```bash
  helm -n $NS history rag
  ```

---

### Links

* Deployment checklist → [deployment\_checklist.md](./deployment_checklist.md)
* Live monitoring → [live\_monitoring\_rag.md](./live_monitoring_rag.md)
* Failover & Recovery → [failover\_and\_recovery.md](./failover_and_recovery.md)

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

