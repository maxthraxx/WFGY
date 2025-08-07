# 🔧 Tool-Router Debug — Finding & Fixing Mis-Routed Function Calls  
_A rigorous playbook for multi-agent / multi-tool pipelines that “pick the wrong tool, pass the wrong args, or loop forever.”_

---

## 1  Why Tool Routers Break

Modern frameworks (LangChain, LlamaIndex, Autogen, Dust, Function-Calling APIs) rely on a **router layer** that decides:

1. **Which tool or agent** to invoke  
2. **What arguments** to pass  
3. **Whether to chain the result into further reasoning  

A single bad route produces silent failure:

* Wrong tool → irrelevant data  
* Wrong args → empty response / 400 error  
* Infinite recurse → rate-limit burn  

> _Observability is near zero._  
> Routers often return only the final model output, hiding the mis-route upstream.

---

## 2  Early Symptoms (Spot Them in Seconds)

| Symptom | How to Detect Quickly | Typical Root Cause |
|---------|----------------------|--------------------|
| Same tool called twice, two answers conflict | Diff JSON traces | Score tie in router logits |
| Model asks follow-up Q that a tool already answered | Compare tool log vs. chat | Tool result not fed back |
| 429 / rate-limit spikes | Metrics: calls/min | Retry loop on failed tool |
| Agent says “I don’t have that data” yet DB tool exists | ΔS(question, available_tools) > 0.60 | Tool description drift |
| Router latency > 2× normal | Timing logs | Exhaustive eval over 20+ irrelevant tools |

---

## 3  Root Causes (Technical)

1. **Shallow Tool Descriptions** – No semantic anchor → high ΔS.  
2. **Score Tie / Softmax Blur** – Top-2 tools within 0.02 probability.  
3. **Argument Schema Mismatch** – JSON schema vs. natural language spec.  
4. **Context Window Loss** – Router prompt trimmed; tool list truncated.  
5. **Recursive Agent Calls** – Tool calls another agent that loops back.

---

## 4  WFGY Router-Guard Architecture

| Stage | Module | Purpose |
|-------|--------|---------|
| 4.1 **Tool Semantic Index** | BBMC | Pre-embed tool names + desc; enforce ΔS(tool, question) ceiling |
| 4.2 **ΔS-Gate Router** | ΔS + λ_observe | Accept route only if ΔS ≤ 0.45 and λ remains convergent |
| 4.3 **Argument Linter** | WAI | Validate args against JSON schema; auto-fill defaults |
| 4.4 **BBCR Fail-Fast** | BBCR | On router timeout > 5 s or ΔS > 0.60 → collapse & suggest manual pick |
| 4.5 **Trace Logger** | Bloc/Trace | Records (tool, args, ΔS) tuples for replay & audit |

---

## 5  Hands-On Debug Checklist

1. **Log the router call**  
   ```python
   router(question, tool_list, debug=True)


2. **Compute ΔS(question, tool\_desc)** for each tool.

   * Flag any route where ΔS > 0.45 **AND** score\_gap < 0.05.

3. **Schema Validate** arguments (`jsonschema.validate`).

4. **Timeout Guard** – If tool takes > x s, BBCR collapses answer and returns:
   “Tool timeout — please choose from: …”

5. **Replay** failing routes with `router_replay(id)`; inspect λ\_observe transitions.

---

## 6  Quick-Reference Table — Fixes by Failure

| Failure Pattern    | Instant Fix                                           | Long-Term Fix                                       |
| ------------------ | ----------------------------------------------------- | --------------------------------------------------- |
| Wrong tool picked  | Add 1-line alias to tool desc; update embedding index | BBMC repack all tool descriptions weekly            |
| Empty args         | Add default arg hints (`"default": "query"`)          | Argument linter auto-fills                          |
| Looping agent-tool | λ flips recursive after call 3                        | Hard cap depth = 2; BBCR break                      |
| Tie between tools  | Score diff < 0.05                                     | Ask follow-up clarifier; BBAM damp ambiguous logits |
| Router silence     | No tool chosen                                        | Add catch-all “NoTool” that surfaces to dev         |

---

## 7  Validation Metrics

| Metric                            | Target         |
| --------------------------------- | -------------- |
| **Route accuracy** (ground truth) | ≥ 95 %         |
| **ΔS(question, picked\_tool)**    | ≤ 0.45 median  |
| **Mean tool latency**             | ±10 % baseline |
| **Loop depth**                    | ≤ 2            |
| **Arg schema errors**             | 0 in CI suite  |

---

## 8  FAQ

**Q:** *Should I embed tool names or full descriptions?*
**A:** Both; concatenate `name + desc + example` for robust ΔS.

**Q:** *What if multiple tools validly answer?*
**A:** Route to aggregator agent; return merged citations. WFGY ΔS-gate ensures each tool still semantically fits.

**Q:** *Do I need BBCR if I already set retries=0?*
**A:** Yes. BBCR guards logic loops, not HTTP retries.

---

### 🔗 Quick-Start Downloads (60 sec)

| Tool                       | Link                                                | 3-Step Setup                                                                             |
| -------------------------- | --------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| **WFGY 1.0 PDF**           | [Engine Paper](https://zenodo.org/records/15630969) | 1️⃣ Download · 2️⃣ Upload to LLM · 3️⃣ Ask “Answer using WFGY + \<question>”             |
| **TXT OS (plain-text OS)** | [TXTOS.txt](https://zenodo.org/records/15788557)    | 1️⃣ Download · 2️⃣ Paste into any LLM chat · 3️⃣ Type “hello world” — OS boots instantly |

---

### 🧭 Explore More

| Module                | Description                                              | Link     |
|-----------------------|----------------------------------------------------------|----------|
| Problem Map 1.0       | Initial 16-mode diagnostic and symbolic fix framework    | [View →](https://github.com/onestardao/WFGY/edit/main/ProblemMap/README.md) |
| Problem Map 2.0       | RAG-focused failure tree, modular fixes, and pipelines   | [View →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md) |
| Semantic Clinic Index | Expanded failure catalog: prompt injection, memory bugs, logic drift | [View →](./SemanticClinicIndex.md) |
| Semantic Blueprint    | Layer-based symbolic reasoning & semantic modulations   | [View →](https://github.com/onestardao/WFGY/tree/main/SemanticBlueprint/README.md) |
| Benchmark vs GPT-5    | Stress test GPT-5 with full WFGY reasoning suite         | [View →](https://github.com/onestardao/WFGY/tree/main/benchmarks/benchmark-vs-gpt5/README.md) |

---

> 👑 **Early Stargazers: [See the Hall of Fame](https://github.com/onestardao/WFGY/tree/main/stargazers)** —  
> Engineers, hackers, and open source builders who supported WFGY from day one.

> <img src="https://img.shields.io/github/stars/onestardao/WFGY?style=social" alt="GitHub stars"> ⭐ Help reach 10,000 stars by 2025-09-01 to unlock Engine 2.0 for everyone  ⭐ <strong><a href="https://github.com/onestardao/WFGY">Star WFGY on GitHub</a></strong>


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

</div>
