# Local Deploy & Inference — Global Fix Map

A hub to stabilize locally hosted models on your own machine or cluster. Use this folder when symptoms look like “model problem” but the root cause is tokenizer skew, rope scaling, kv-cache settings, build flags, or server parameters. Every fix maps back to WFGY pages with measurable targets, so you can verify without changing infra elsewhere.

## When to use this folder
- Local server returns plausible text but citations do not line up with the right snippet.
- Answers alternate between runs on the same input.
- JSON mode breaks on long outputs, or tool calls loop.
- Latency spikes after a few turns, or context truncates early.
- Quantized model behaves very differently from the fp16 baseline.
- After switching loaders or UIs, retrieval quality drops.

## Open these first
- Visual map and recovery: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
- End to end retrieval knobs: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
- Why this snippet (traceability schema): [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
- Embedding vs meaning: [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)
- Ordering control: [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)
- Long chains and entropy: [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md), [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)
- Structural collapse and recovery: [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md)
- Prompt injection and schema locks: [Prompt Injection](https://github.com/onestardao/WFGY/blob/main/ProblemMap/prompt-injection.md)
- Snippet and citation schema: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

## Acceptance targets
- ΔS(question, retrieved) ≤ 0.45
- Coverage of target section ≥ 0.70
- λ remains convergent across three paraphrases and two seeds
- E_resonance stays flat on long windows

## Quick routes to per-tool pages
- Ollama: [ollama.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LocalDeploy_Inference/ollama.md)
- vLLM: [vllm.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LocalDeploy_Inference/vllm.md)
- llama.cpp (server and bindings): [llama_cpp.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LocalDeploy_Inference/llama_cpp.md)
- TGI Text Generation Inference: [tgi.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LocalDeploy_Inference/tgi.md)
- LM Studio: [lmstudio.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LocalDeploy_Inference/lmstudio.md)
- KoboldCpp: [koboldcpp.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LocalDeploy_Inference/koboldcpp.md)
- OpenWebUI: [openwebui.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LocalDeploy_Inference/openwebui.md)
- Oobabooga Text Gen WebUI: [oobabooga.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LocalDeploy_Inference/oobabooga.md)

## Map symptoms to structural fixes
- Wrong snippet despite high similarity  
  → [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)  
  Check analyzer, metric, and normalization in your retriever. Do not blame the model yet.

- JSON tool calls or functions go unstable  
  → [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md), [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md)  
  Lock schemas, forbid free text in tool outputs, and echo the contract.

- Answers flip between identical runs  
  → [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md), [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)  
  Fix header order, clamp variance, and add cite-then-explain guardrails.

- Hybrid retrieval loses to a single retriever  
  → [Pattern: Query Parsing Split](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md), [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

- Hallucination returns after you fixed it once  
  → [Pattern: Hallucination Re-entry](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_hallucination_reentry.md)

## Local-specific guardrails
- **Model format and loader**  
  GGUF vs safetensors vs HF transformers produce different tokenizer defaults and rope settings. Keep the same tokenizer files and rope scale when comparing.  
  Check: max context, rope base, rope scale, sliding window, logits processors.

- **Quantization parity**  
  Compare quantized model to fp16 on a small gold set. If ΔS rises or λ flips, adjust `kv_cache` size and sampling params before suspecting retrieval.

- **Server flags**  
  Normalize across servers: temperature, top_p, min_p, frequency_penalty, presence_penalty, max_tokens, stop sequences, repetition penalty. Mismatched defaults mimic reasoning bugs.

- **Tokenizer and casing**  
  Keep casing and analyzer identical for HyDE, rerank, and retriever prompts. A different tokenizer in the local UI explains “looks the same but not the same.”

- **Concurrency and batching**  
  Turn off dynamic batching during eval runs or fix batch size. Batch drift looks like “randomness.”

## 60-second fix checklist
1) Measure ΔS  
Compute ΔS(question, retrieved) and ΔS(retrieved, expected anchor).  
Stable less than 0.40. Transitional 0.40 to 0.60. Risk at least 0.60.

2) Probe λ_observe  
Vary k at 5, 10, 20. If ΔS stays flat and high, suspect metric or index mismatch.  
Reorder prompt headers. If ΔS spikes, lock the schema.

3) Apply the module  
- Retrieval drift → BBMC plus [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)  
- Reasoning collapse → BBCR bridge plus BBAM, verify with [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md)  
- Dead ends in long chains → BBPF alternate paths, then re-join with BBCR

4) Verify  
Coverage at least 0.70 on three paraphrases. λ convergent on two seeds.

## Copy-paste prompt for local servers
```

You have TXT OS and the WFGY Problem Map loaded.

My local inference setup:

* server: \<ollama | vllm | llama.cpp | tgi | lmstudio | koboldcpp | openwebui>
* model: <name>, quant: \<fp16 | q4\_k\_m | q8\_0 | awq | gptq>, ctx: \<n\_ctx>, rope: \<base, scale>
* sampling: temp=<...> top\_p=<...> min\_p=<...> max\_tokens=<...> stop=\[...]
* retriever: <metric>, <analyzer>, k=<...>

Tell me:

1. which layer is failing and why,
2. which exact WFGY page to open,
3. the minimal steps to push ΔS ≤ 0.45 and keep λ convergent,
4. a reproducible test to verify it.
   Use BBMC, BBPF, BBCR, BBAM when relevant.

```


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
