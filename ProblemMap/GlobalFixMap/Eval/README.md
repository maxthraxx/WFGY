# Evaluation & Guardrails — Global Fix Map

<details>
  <summary><strong>🏥 Quick Return to Emergency Room</strong></summary>

<br>

  > You are in a specialist desk.  
  > For full triage and doctors on duty, return here:  
  > 
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](https://github.com/onestardao/WFGY/blob/main/ProblemMap/README.md)  
  > 
  > Think of this page as a sub-room.  
  > If you want full consultation and prescriptions, go back to the Emergency Room lobby.
</details>

A hub to **prove fixes actually work and won’t regress**.  
Use this folder when you want to validate that your RAG / LLM pipeline changes are stable, measurable, and reproducible.  
The goal is to prevent “double hallucination,” enforce acceptance gates, and keep evaluation pipelines auditable.

---

## What this page is
- A compact playbook to evaluate RAG quality and reasoning stability  
- Drop-in guardrails that catch failures before users see them  
- CI/CD-ready acceptance targets you can copy directly  

---

## When to use
- You shipped a fix but cannot show measurable improvement  
- Answers look plausible but citations or snippets don’t match  
- Performance flips between seeds, sessions, or agent mixes  
- Latency tuning silently changes accuracy  
- Your team disagrees on whether a fix is “actually better”  

---

## Open these first
- RAG precision/recall spec → [eval_rag_precision_recall.md](./eval_rag_precision_recall.md)  
- Latency versus accuracy method → [eval_latency_vs_accuracy.md](./eval_latency_vs_accuracy.md)  
- Cross-agent agreement tests → [eval_cross_agent_consistency.md](./eval_cross_agent_consistency.md)  
- Semantic stability checks → [eval_semantic_stability.md](./eval_semantic_stability.md)  
- Why-this-snippet schema → [retrieval-traceability.md](../retrieval-traceability.md)  
- Snippet & citation schema → [data-contracts.md](../data-contracts.md)  

---

## Common evaluation pitfalls
- **Double hallucination** → Metrics look good (BLEU, ROUGE) but answers cite the wrong snippet  
- **Recall illusion** → Top-k recall seems fine, yet ΔS(question, context) is still unstable  
- **Seed lottery** → Success on one random seed hides instability across paraphrases  
- **Hybrid flapping** → HyDE + BM25 mixes reorder results differently every run  
- **Over-clamping** → Filters enforce tone but fail to fix logical drift  
- **Benchmark mismatch** → Eval set ignores OCR noise or multilingual inputs  
- **No trace table** → You cannot audit which snippet was cited  

---

## Fix in 60 seconds
1. **Adopt acceptance gates**
   - Retrieval sanity: token overlap ≥ 0.70 to the gold section  
   - ΔS(question, context) ≤ 0.45 on median across suite  
   - λ_observe stays convergent across 3 paraphrases  

2. **Require citations first**
   - Enforce cite-then-answer with [data-contracts.md](../data-contracts.md)  
   - Log: question, retrieved ids, snippet spans, ΔS, λ  

3. **Stability before speed**
   - Always measure latency vs accuracy before tuning  
   - See [eval_latency_vs_accuracy.md](./eval_latency_vs_accuracy.md)  

4. **Cross-agent cross-check**
   - Run 2 strong models on the same retrieval  
   - See [eval_cross_agent_consistency.md](./eval_cross_agent_consistency.md)  

5. **Regression fence in CI**
   - Block merges if ΔS median > 0.45 or coverage < 0.70  
   - See [eval_rag_precision_recall.md](./eval_rag_precision_recall.md)  

---

## Minimal checklist
- Trace table saved (citations + snippet spans)  
- ΔS computed per item; λ recorded at retrieval & reasoning  
- Coverage ≥ 0.70 to gold snippet  
- Cross-agent agreement tested  
- Latency vs accuracy chart archived with run id  

---

## Acceptance targets
- ΔS(question, context) median ≤ **0.45**  
- λ **convergent** across 3 paraphrases  
- Token overlap ≥ **0.70** to gold snippet  
- No unexplained rank flips on hybrid retrievers  
- CI blocks merges when targets fail  

---

## FAQ

**Q: What is ΔS and why does it matter?**  
A: ΔS measures semantic distance between your query and retrieved context. Values above 0.45 indicate unstable retrieval, even if the snippet looks similar.  

**Q: Why not just trust BLEU/ROUGE?**  
A: They score surface similarity, not factual correctness. A fluent but wrong answer can pass BLEU. WFGY gates enforce snippet fidelity.  

**Q: What does λ_observe mean?**  
A: λ_observe tracks whether paraphrased queries converge on the same retrieval. Divergence shows instability that will confuse users.  

**Q: How do I build a trace table?**  
A: For every eval item, log `question`, `retrieved ids`, `snippet spans`, `ΔS`, `λ_state`. This makes your pipeline auditable later.  

**Q: Do I need a big eval set?**  
A: No. Start with 20 smoke-test items, including multilingual or noisy samples. Scale up only after you pass basic gates.  

**Q: What if latency tuning drops accuracy?**  
A: Always plot latency vs accuracy. Use the knee point of the curve, not the fastest or slowest configuration.  

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
