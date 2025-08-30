# Context Drift — Long Reasoning Chain Instability

When reasoning spans 20–40 hops or more, attention shifts accumulate and context drifts.  
This page explains how to diagnose λ divergence, stabilize reasoning chains, and repair collapsed context.

---

## When to use this page
- Long reasoning plans (~20+ steps) start with logic but later flip or contradict.  
- Multi-agent workflows repeat or miss earlier facts.  
- Citations remain valid, but final answers drift from original question.  
- λ flips divergent after harmless paraphrases.  
- Answers alternate between runs with identical inputs.

---

## Core acceptance targets
- ΔS(question, retrieved) ≤ 0.45  
- Retrieval coverage ≥ 0.70 for target section  
- λ remains convergent across three paraphrases  
- Chain length stable up to 40 hops without collapse  
- Entropy variance remains bounded in mid-to-late steps  

---

## Structural fixes

- **Three-paraphrase probe**  
  Re-ask the same question three ways. Log ΔS and λ at each hop.  
  If λ flips, schema is unstable.

- **Clamp with BBAM**  
  Apply variance clamp when λ flips across harmless paraphrases.

- **Bridge with BBCR**  
  Insert bridge nodes when long chains stall. Anchor back to earlier stable nodes.

- **Enforce snippet fences**  
  Require each reasoning step cite snippet_id. Forbid cross-section reuse.

- **Re-anchor with anchors**  
  Compare ΔS(question, anchor) vs ΔS(question, decoy).  
  If ΔS is close, re-chunk corpus.

---

## Fix in 60 seconds
1. **Log ΔS and λ** across 3 paraphrases.  
2. **Clamp** with BBAM if λ flips.  
3. **Bridge** with BBCR if reasoning halts.  
4. **Re-anchor** using anchor triangulation.  
5. **Verify** coverage ≥ 0.70 and ΔS ≤ 0.45.  

---

## Copy-paste prompt

```

You have TXT OS and the WFGY Problem Map.

Goal: Detect and repair context drift in long reasoning chains.

Protocol:

1. Ask the same question three ways.
2. Log ΔS(question, retrieved) for each.
3. Log λ states across all hops.
4. If λ flips:

   * Apply BBAM clamp.
   * If reasoning stalls, apply BBCR and anchor bridge.
5. Require snippet\_id at each step.
6. Report:

   * ΔS(question, retrieved)
   * λ states across paraphrases
   * bridge nodes inserted
   * final answer with citations

```

---

## Common failure patterns
- **Chain stall**: reasoning halts after ~25–30 hops.  
- **Paraphrase drift**: harmless rewordings flip λ.  
- **Repeating answers**: earlier snippets loop back with filler.  
- **Contradictions**: late chain contradicts early reasoning.  

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
