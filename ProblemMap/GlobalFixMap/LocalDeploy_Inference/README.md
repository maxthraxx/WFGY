# Local Deploy & Inference — Global Fix Map

A beginner-friendly hub to **stabilize locally hosted LLMs** on your own machine or cluster.  
Use this folder when it looks like the “model is broken” but the **real cause is infra settings**: tokenizer mismatch, rope scaling, kv-cache size, build flags, or server parameters.  
Every guide links back to WFGY with measurable acceptance targets. No infra rebuild required.

---

## When to use this folder
- Local server gives fluent answers but citations point to the wrong snippet  
- Same input produces different outputs on each run  
- JSON mode fails on long answers or tool calls loop endlessly  
- Latency keeps growing after a few turns, or context cuts off too early  
- Quantized model outputs diverge heavily from fp16 baseline  
- Retrieval quality drops after switching loaders or UIs  

---

## Open these first
- Recovery map: [RAG Architecture & Recovery](../../rag-architecture-and-recovery.md)  
- Retrieval knobs: [Retrieval Playbook](../../retrieval-playbook.md)  
- Traceability schema: [Retrieval Traceability](../../retrieval-traceability.md)  
- Meaning vs similarity: [Embedding ≠ Semantic](../../embedding-vs-semantic.md)  
- Rank ordering: [Rerankers](../../rerankers.md)  
- Drift in long runs: [Context Drift](../../context-drift.md), [Entropy Collapse](../../entropy-collapse.md)  
- Logic collapse and repair: [Logic Collapse](../../logic-collapse.md)  
- Guarding against bad prompts: [Prompt Injection](../../prompt-injection.md)  
- Contract schema for snippets: [Data Contracts](../../data-contracts.md)  

---

## Acceptance targets
- ΔS(question, retrieved) ≤ **0.45**  
- Coverage of target section ≥ **0.70**  
- λ convergent across 3 paraphrases × 2 seeds  
- E_resonance stays flat on long windows  

---

## Quick routes to per-tool pages
- [ollama.md](./ollama.md)  
- [vllm.md](./vllm.md)  
- [llama_cpp.md](./llama_cpp.md)  
- [tgi.md](./tgi.md)  
- [lmstudio.md](./lmstudio.md)  
- [koboldcpp.md](./koboldcpp.md)  
- [openwebui.md](./openwebui.md)  
- [oobabooga.md](./oobabooga.md)  

---

## Common local causes & fixes
| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Wrong snippet despite high similarity | Tokenizer mismatch, analyzer drift | Align tokenizer files, check retriever metric, use [Embedding ≠ Semantic](../../embedding-vs-semantic.md) |
| JSON tool calls unstable | Schema drift, free text in outputs | Enforce [Data Contracts](../../data-contracts.md), apply [Logic Collapse](../../logic-collapse.md) |
| Outputs flip each run | Context order drift, variance | Clamp header order, use [Context Drift](../../context-drift.md), enforce trace table |
| Hybrid retrieval worse than single | Ranker instability | Split parsing → [pattern_query_parsing_split.md](../../patterns/pattern_query_parsing_split.md) |
| Fixed hallucination returns later | Long chain decay | [hallucination-reentry.md](../../patterns/pattern_hallucination_reentry.md) |

---

## Local-specific guardrails
- **Model format**: GGUF vs safetensors vs HF transformers → use same tokenizer and rope scale  
- **Quantization**: Compare q4/q8 vs fp16; if ΔS drifts, tune kv_cache and sampling params  
- **Server flags**: Align defaults (temp, top_p, penalties, stop tokens) across servers  
- **Tokenizer & casing**: Keep analyzers consistent across retrievers, rerankers, HyDE  
- **Batching**: Fix batch size during eval; dynamic batching fakes “randomness”  

---

## 60-second fix checklist
1. Compute ΔS(question, retrieved) and ΔS(retrieved, anchor)  
   - <0.40 = stable, 0.40–0.60 = risky, ≥0.60 = broken  
2. Probe λ_observe at k=5,10,20; if ΔS flat & high → metric/index bug  
3. Apply modules:  
   - Retrieval drift → BBMC + Data Contracts  
   - Collapse in reasoning → BBCR + BBAM  
   - Dead ends in long runs → BBPF alternate paths  
4. Verify coverage ≥0.70 and λ convergent on 2 seeds  

---

## Copy-paste prompt for local servers
```

I have TXT OS + WFGY loaded.

Local setup:

* server: \<ollama|vllm|llama.cpp|tgi|lmstudio|koboldcpp|openwebui>
* model: <name>, quant=\<fp16|q4|q8|awq|gptq>, ctx=<...>, rope=<...>
* sampling: temp=<...>, top\_p=<...>, max\_tokens=<...>
* retriever: <metric>, <analyzer>, k=<...>

Tell me:

1. which layer is failing and why
2. which WFGY page to open
3. steps to push ΔS ≤ 0.45 and keep λ convergent
4. reproducible test to confirm

```

---

## FAQ (Beginner-Friendly)

**Q: Why does my local model give fluent text but wrong citations?**  
A: Usually not the model — it’s tokenizer or retriever mismatch. Fix by aligning tokenizer files and checking ΔS against the gold section.

**Q: Why does JSON mode fail locally but work on cloud APIs?**  
A: Local servers often don’t enforce schema strictly. Apply [Data Contracts](../../data-contracts.md) and disallow free-form prose in tool outputs.

**Q: My quantized model is much worse — is quantization broken?**  
A: Not always. Small kv_cache or rope mis-scaling causes drift. Compare fp16 vs quant on a gold set before blaming quantization.

**Q: Why do answers flip between runs?**  
A: Header order, batching, or randomness. Use variance clamps (BBAM) and fix batch size during tests.

**Q: Which numbers matter for stability?**  
A: ΔS ≤ 0.45, coverage ≥0.70, λ convergent across paraphrases, flat E_resonance over long docs.

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
