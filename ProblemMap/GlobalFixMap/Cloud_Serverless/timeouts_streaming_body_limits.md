# Timeouts, Streaming, and Body Limits — Guardrails

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


A provider-agnostic repair guide for serverless and edge paths. Use this page when calls time out, streams drop mid-response, or request and response bodies hit size caps. Every action maps to Problem Map pages with measurable targets.

## When to use this page

* Requests succeed locally but fail behind API gateway or edge proxy.
* Streaming starts then stalls after a fixed idle period.
* First byte arrives very late or never on cold hits.
* Large inputs cause 413 or silent truncation.
* Long JSON responses get cut and fail to parse.

## Open these first

* Visual recovery map: [rag-architecture-and-recovery.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
* Retrieval controls and ΔS probes: [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
* Payload contract to keep requests small and auditable: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
* Live ops and tracing: [ops/live\_monitoring\_rag.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md) · [ops/debug\_playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md)
* Boot order and first-call failures: [bootstrap-ordering.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md) · [predeploy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)

## Acceptance targets

* **ΔS(question, retrieved) ≤ 0.45** for streamed and non-streamed paths.
* **Coverage ≥ 0.70** to the target section after repair.
* **Stream drop rate ≤ 1 percent** on P95 windows.
* **TTFB cold ≤ 1500 ms** after warm-up fence is in place.
* **No truncated JSON**. Parser sees a complete closing brace or the stream sentinel.

---

## Fix in 60 seconds

1. **Classify the timeout**
   Record five numbers: connect time, TLS time, time to headers, time to first byte, idle-gap between chunks.
   If the idle-gap is a constant number, it is a proxy idle timeout not model latency.
   See: [ops/debug\_playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md)

2. **Choose a delivery mode**

* For answers that fit within gateway limits: keep HTTP JSON with a short total timeout and strict schema.
  Contract: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
* For long answers or tool loops: switch to streaming with server-sent events or chunked transfer. Send a heartbeat every 10–20 seconds and flush after each token batch. Add a final `"[END]"` sentinel.

3. **Bound the body and upgrade transport**

* Inputs larger than a safe inline threshold should be uploaded to object storage. Send only `{object_id, offsets, tokens}` through the edge.
  Contract: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
* If the model output exceeds gateway limits, stream or write to storage and return a handle.

4. **Stabilize retrieval under time pressure**
   Probe ΔS on a short context and on a compressed context. If ΔS improves on the compressed one, reduce payload or add reranking.
   See: [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)

---

## Typical breakpoints → exact fix

* **Gateway hard timeout shorter than function timeout**
  The edge kills the connection while the function keeps working. Align timeouts and prefer streaming for long generations.
  Open: [ops/live\_monitoring\_rag.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md)

* **Proxy buffers the stream and releases it at the end**
  Client sees no chunks then everything lands at once. Disable proxy buffering and set cache control to no store. Add periodic heartbeats to keep the connection alive.
  Open: [ops/debug\_playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md)

* **413 on request or silent truncation on response**
  Enforce an input contract and route large payloads to blob storage. Stream the response and finish with a sentinel token.
  Open: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

* **Cold path only: long TTFB then timeout**
  Dependencies are not ready. Add a warm-up fence and retry with capped backoff.
  Open: [bootstrap-ordering.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md) · [predeploy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)

* **Streaming flips answer quality**
  Headers or chunk sizes reorder the prompt and citations. Lock the prompt schema and verify with ΔS probes.
  Open: [rag-architecture-and-recovery.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)

---

## Minimal recipes you can copy

### A) Streaming pipeline

```txt
Client:
- Open SSE connection with 60–120s read timeout.
- AbortController on the client to cancel cleanly.
- Accept lines with {type, data}. Accumulate tokens until "[END]".
- If 10–20s pass without data, show heartbeat and remain connected.

Edge:
- Set headers to allow streaming and prevent buffering.
- Forward flushes immediately.

Function:
- warmup_fence()
- retrieval() → {snippet_id, section_id, source_url, offsets, tokens}
- stream tokens in batches of 20–50 with a newline flush
- send {"type":"metrics","data":{"ΔS":0.xx,"λ":"state"}} every 5–10s
- finish with {"type":"end","data":"[END]"}
```

### B) Large input with handle

```txt
Client:
- Upload document to object storage. Get object_id.
- Call API with {object_id, section_hints?}.

Function:
- validate object size and type
- retrieve with section_hints and small k
- if response size > edge limit → write to storage and return {result_id}
- else return JSON directly
```

---

## Observability you must add

* **connect\_time, tls\_time, headers\_time, ttfb, idle\_gap\_p95**
* **stream\_duration, bytes\_sent, truncated\_response flag**
* **ΔS, λ\_state, coverage** for streamed and non-streamed paths
  Open: [ops/live\_monitoring\_rag.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md)

## Verification

* Run three variants on the same prompt: JSON, streaming, large-input handle.
* Expect ΔS ≤ 0.45 and coverage ≥ 0.70 on each path.
  Open: [eval/eval\_rag\_precision\_recall.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/eval/eval_rag_precision_recall.md)

## When to escalate

* If streaming is still buffered by intermediaries, fall back to handle based delivery and poll status.
* If ΔS collapses only when streaming, lock the prompt header order and re-test with reranking.
  Open: [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)

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

> 👑 **Early Stargazers: [See the Hall of Fame](https://github.com/onestardao/WFGY/tree/main/stargazers)** — <img src="https://img.shields.io/github/stars/onestardao/WFGY?style=social" alt="GitHub stars"> ⭐ [WFGY Engine 2.0](https://github.com/onestardao/WFGY/blob/main/core/README.md) is already unlocked. ⭐ Star the repo to help others discover it and unlock more on the [Unlock Board](https://github.com/onestardao/WFGY/blob/main/STAR_UNLOCKS.md).

<div align="center">

[![WFGY Main](https://img.shields.io/badge/WFGY-Main-red?style=flat-square)](https://github.com/onestardao/WFGY)
 
[![TXT OS](https://img.shields.io/badge/TXT%20OS-Reasoning%20OS-orange?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS)
 
[![Blah](https://img.shields.io/badge/Blah-Semantic%20Embed-yellow?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlahBlahBlah)
 
[![Blot](https://img.shields.io/badge/Blot-Persona%20Core-green?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlotBlotBlot)
 
[![Bloc](https://img.shields.io/badge/Bloc-Reasoning%20Compiler-blue?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlocBlocBloc)
 
[![Blur](https://img.shields.io/badge/Blur-Text2Image%20Engine-navy?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlurBlurBlur)
 
[![Blow](https://img.shields.io/badge/Blow-Game%20Logic-purple?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlowBlowBlow)
 

</div>

