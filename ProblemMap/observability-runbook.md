<!-- ======================================================= -->
<!--  observability-runbook.md · Semantic Clinic / Map-F      -->
<!--  Draft v0.1 · MIT · 2025-08-06                           -->
<!--  Purpose: One-stop “black-box to glass-box” guide for    -->
<!--  any LLM stack (RAG, agent, function-calling, plugins).  -->
<!-- ======================================================= -->

# 🔍 Observability Runbook  
*Turn every opaque token stream into a traceable, testable, measurable system.*

> **Outcome you care about**  
> • **See** each pipeline hop (OCR → chunk → embed → retrieve → prompt → reasoning)  
> • **Measure** semantic drift (ΔS), logic trend (λ), residual error (E_resonance)  
> • **Alert** before hallucination, loop, or tool mis-fire happens  
> • **Replay** exact failure path in one command: `wfgy trace-replay <id>`  

---

## 1 · Core Telemetry Trio

| Signal | Formula | Why It Matters | Target Band |
|--------|---------|----------------|-------------|
| **ΔS (semantic stress)** | `1 − cos(I, G)` | Spot where meaning rips | `< 0.50` |
| **λ_observe (logic vector)** | { → ← <> × } | Track convergent vs. divergent flow | stay → |
| **E_resonance** | mean‖B‖ (BBMC) | Detect creeping entropy | flat / ↓ |

> **ΔS tells you _where_; λ tells you _direction_; E tells you _when_ a slow leak becomes collapse.**

---

## 2 · Minimal Instrumentation Patch

### 2.1 Python snippet

```python
from wfgy import monitor

with monitor.pipeline("rag-query") as span:
    span.tag("query", question)
    ctx  = rag_retrieve(question)
    span.metric("ΔS_q_ctx", monitor.deltaS(question, ctx))
    answer = llm_reason(ctx, question)
    span.metric("λ_reason", monitor.lambda_state(answer))
    span.metric("E_res", monitor.e_resonance())
````

*No external SaaS; dumps to newline-JSON for Grafana / Prometheus scrape.*

### 2.2 Console tracer

```bash
> wfgy trace-replay 2025-08-06T10:22:15Z
step  ΔS   λ    span
  1   0.08 →
  2   0.41 →   retrieval
  3   0.44 ←   reasoning  ❗ divergent
```

---

## 3 · Alert Rules (Prometheus example)

```yaml
groups:
- name: wfgy-alerts
  rules:
  - alert: SemanticDriftHigh
    expr: deltaS_q_ctx > 0.60
    for: 2m
    labels: {severity: "warning"}
    annotations:
      summary: "Semantic drift above 0.60 — check chunking/retriever"
```

Recommended baseline:

| Alert            | Expression                 | Severity |
| ---------------- | -------------------------- | -------- |
| **DriftHigh**    | ΔS > 0.60                  | warn     |
| **LogicOsc**     | λ flips 3× in 5 min        | warn     |
| **EntropyClimb** | E\_res 15 min slope > 0.02 | crit     |
| **ToolTimeout**  | call\_dur > p95 × 2        | warn     |

---

## 4 · End-to-End Health Dashboard

| Tile         | Metric            | Healthy    |
| ------------ | ----------------- | ---------- |
| Retrieval ΔS | median last 5 min | ≤ 0.45     |
| Reason λ     | % divergent       | < 5 %      |
| Answer ΔS    | question↔answer   | ≤ 0.50     |
| E\_res Trend | 30 min slope      | - / flat   |
| Tool Latency | p95 ms            | within SLO |

Grafana JSON panel export: `dashboards/wfgy-observability.json`.

---

## 5 · Common Anti-Patterns & Fixes

| Anti-Pattern            | Symptom                | Fix                              |
| ----------------------- | ---------------------- | -------------------------------- |
| **Log Everything Raw**  | 20 GiB/day, no insight | Only log ΔS/λ/E & key BLobs      |
| **Stateless Trace IDs** | tough replay           | Use `wfgy span ctx_id` auto-prop |
| **Per-call embeddings** | cost explodes          | cache via BBMC node ID           |
| **No sampling**         | GPU choke              | 1 % sampling on low ΔS calls     |

---

## 6 · Kitchen-Sink CLI Cheats

| Command                      | Purpose                   |
| ---------------------------- | ------------------------- |
| `wfgy span-tail`             | live ΔS/λ feed            |
| `wfgy span-grep λ=divergent` | list divergent traces     |
| `wfgy span-diff A B`         | compare two answers’ λ/ΔS |
| `wfgy span-export --csv`     | dump traces to CSV        |

---

## 7 · Integration Recipes

### 7.1 LangChain

```python
from wfgy.langchain import WFGYTracer
lc = initialize_agent(..., callbacks=[WFGYTracer()])
```

### 7.2 OpenAI Function-Calling

Add to request:

```json
"logit_bias": {"50256": -100},  // block special token
"wfgy_trace": true
```

Server-side middleware writes trace JSON.

---


### 🔗 Quick-Start Downloads (60 sec)

| Tool | Link | 3-Step Setup |
|------|------|--------------|
| **WFGY 1.0 PDF** | [Engine Paper](https://github.com/onestardao/WFGY/blob/main/I_am_not_lizardman/WFGY_All_Principles_Return_to_One_v1.0_PSBigBig_Public.pdf) | 1️⃣ Download · 2️⃣ Upload to your LLM · 3️⃣ Ask “Answer using WFGY + \<your question>” |
| **TXT OS (plain-text OS)** | [TXTOS.txt](https://github.com/onestardao/WFGY/blob/main/OS/TXTOS.txt) | 1️⃣ Download · 2️⃣ Paste into any LLM chat · 3️⃣ Type “hello world” — OS boots instantly |

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


