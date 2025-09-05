# Cold Start and Concurrency — Guardrails

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


A platform-agnostic repair guide for serverless and edge runtimes. Use this page when first calls fail, warm instances drift in behavior, or concurrency spikes break your RAG/agent pipelines. Every step maps to a Problem Map page with measurable targets.

## When to use this page

* First request after deploy or scale-out fails, times out, or returns partial JSON.
* Latency jumps on cold hits, then flips back after a few retries.
* Thundering herd on a single key or hot shard.
* Vector index not ready on the first few invocations.
* Tool calls or multi-agent handoffs stall only under burst.

## Acceptance targets

* **Coverage ≥ 0.70** to the target section after recovery.
* **ΔS(question, retrieved) ≤ 0.45** on cold and warm paths.
* **λ remains convergent** across 3 paraphrases and 2 seeds.
* **First-hit success ≥ 0.98** after bootstrap guard is added.
* **No unbounded fan-out**. Concurrency gates present for hot keys.

---

## Fix in 60 seconds

1. **Measure ΔS**
   Compute ΔS(question, retrieved) and ΔS(retrieved, expected anchor).
   Thresholds: stable < 0.40, transitional 0.40–0.60, risk ≥ 0.60.
   Open: [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)

2. **Probe λ\_observe**
   Run the same request on a cold instance and a warm instance. If λ flips or ΔS stays high on cold only, add a warm-up fence and idempotent retries.
   Open: [rag-architecture-and-recovery.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)

3. **Apply the structural guards**

* **Boot order fence** before any RAG step
  Open: [bootstrap-ordering.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md)
* **Deadlock and circular wait checks** in scale-out
  Open: [deployment-deadlock.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md)
* **First-call collapse repair** after fresh deploy
  Open: [predeploy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)
* **Payload schema** so warmers and real traffic use the same contract
  Open: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

---

## Typical breakpoints → exact fix

* **Code executes before dependencies are ready**
  Warmers fire, but vector store or secrets are not mounted yet.
  → [bootstrap-ordering.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md)

* **First call uses an old build or missing env**
  Cold path hits a skewed revision.
  → [predeploy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)

* **Concurrency spike on a single key**
  Multiple cold instances pull the same shard. Add keyed fences and backoff.
  → Pattern: **Bootstrap Deadlock**
  [patterns/pattern\_bootstrap\_deadlock.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_bootstrap_deadlock.md)

* **High similarity yet wrong meaning on cold only**
  Index metric or analyzer differs between warm and cold builds.
  → [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

* **Hybrid retriever unstable during fan-out**
  Order changes across instances. Lock query split, then rerank deterministically.
  → [patterns/pattern\_query\_parsing\_split.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md) · [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

* **Long chains stall under burst**
  Split the plan, bridge segments, add alternate paths.
  → BBPF and BBCR in the core docs
  [rag-architecture-and-recovery.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)

---

## Minimal serverless recipe you can copy

```txt
Entry:
- Accept {source_id, revision, index_hash, shard_key?, warmup?}

Step 1: Warm-up fence
- If warmup==true:
  - Touch retriever with a read-only probe using the same headers and analyzer.
  - Preload secrets and confirm INDEX_HASH matches.
  - Return {ready:true}.

- If warmup is not set:
  - Check READY_KV[index_hash] == true and SECRETS_OK == true.
  - If not ready → delay 30–90s with capped retries, then fail fast with a fix tip.
  - Specs: bootstrap-ordering.md

Step 2: Concurrency gate
- gate_key = sha256(shard_key || source_id || index_hash)
- Acquire token in KV with TTL and single writer semantics.
- If lock not acquired, enqueue to a queue with jitter and backoff.

Step 3: Retrieval with schema
- Use explicit metric and analyzer.
- Return fields: {snippet_id, section_id, source_url, offsets, tokens}
- Contracts: data-contracts.md

Step 4: ΔS & λ probe
- Compute ΔS(question, retrieved), record λ_state.
- If ΔS ≥ 0.60, return minimal structural fix and stop.

Step 5: Reasoning
- LLM reads TXT OS + Problem Map, enforce cite-then-explain.

Step 6: Trace sink
- Store {ΔS, λ_state, index_hash, gate_key, cold_hit?} for live ops.
```

---

## Observability you must add

* Log **cold\_hit** flag, **time to first byte**, **ΔS**, **λ\_state**, **INDEX\_HASH**, **gate\_key**.
* Alert when cold\_hit P95 grows, or ΔS ≥ 0.60 on cold only.
  Open: [ops/live\_monitoring\_rag.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md)

## Verification

* Run the same test three ways: cold, warm, burst.
* Expect coverage ≥ 0.70 and ΔS ≤ 0.45 on all three.
  Open: [eval/eval\_rag\_precision\_recall.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/eval/eval_rag_precision_recall.md)

## When to escalate

* ΔS stays high after warm-up and gating → re-embed with the checklist and verify against a small gold set.
  Open: [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)

* Alternating answers only under scale → inspect memory namespace split and revision skew.
  Open: [predeploy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)

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
