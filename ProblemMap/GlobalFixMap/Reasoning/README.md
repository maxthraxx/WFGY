# Reasoning — Global Fix Map

A compact hub to stabilize long chains, prevent collapse, and keep decisions auditable.  
Use this folder when answers drift across runs, chains dead-end, or the model rewrites reality during long plans. Every page maps symptoms to exact WFGY fixes with measurable acceptance targets.

---

## When to use this folder

- Multi-step answers change when you rerun the same prompt  
- Chains go in circles or re-assert a claim after correction  
- Logic jumps without citing the source that drove the jump  
- Long chats lose earlier anchors when the window rolls  
- Plans grow without bound and never converge

---

## Acceptance targets

- ΔS(question, selected_evidence) ≤ 0.45 on all runs  
- Coverage of the target section ≥ 0.70 with cite-then-explain  
- λ remains convergent across three paraphrases and two seeds  
- E_resonance flat across long windows and at window joins  
- Deterministic step count for plan stages after clamps

---

## Quick routes to per-page guides

- Entropy overload in long chains  
  → [entropy-overload.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/entropy-overload.md)

- Recursive loops and stuck flows  
  → [recursive-loop.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/recursive-loop.md)

- Hallucination re-entry after correction  
  → [hallucination-reentry.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/hallucination-reentry.md)

- Logic collapse and structural recovery  
  → [logic-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/logic-collapse.md)

- Symbolic collapse in abstraction jumps  
  → [symbolic-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/symbolic-collapse.md)

- Proof dead ends and missing pivots  
  → [proof-dead-ends.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/proof-dead-ends.md)

- Anchoring and bridge proofs between frames  
  → [anchoring-and-bridge-proofs.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/anchoring-and-bridge-proofs.md)

- Context stitching and window joins  
  → [context-stitching-and-window-joins.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/context-stitching-and-window-joins.md)

- Chain-of-thought variance clamp  
  → [chain-of-thought-variance-clamp.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/chain-of-thought-variance-clamp.md)

- Redundant evidence collapse  
  → [redundant-evidence-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/redundant-evidence-collapse.md)

---

## Fast triage by symptom

| Symptom | Open this |
|---|---|
| Steps keep growing, answer never lands | [entropy-overload.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/entropy-overload.md) |
| Chain circles back to earlier step | [recursive-loop.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/recursive-loop.md) |
| Model re-asserts the wrong claim after you fix it | [hallucination-reentry.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/hallucination-reentry.md) |
| Reasoning jumps without structure, loses invariants | [logic-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/logic-collapse.md) |
| Abstract move breaks semantics across frames | [symbolic-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/symbolic-collapse.md) |
| Proof chain stalls at an unprovable step | [proof-dead-ends.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/proof-dead-ends.md) |
| Window roll drops the anchor or flips the claim | [context-stitching-and-window-joins.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/context-stitching-and-window-joins.md) |
| Reruns disagree because thoughts wander | [chain-of-thought-variance-clamp.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/chain-of-thought-variance-clamp.md) |
| Too many similar snippets overpower minority facts | [redundant-evidence-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/redundant-evidence-collapse.md) |
| Need a stable bridge between two frames | [anchoring-and-bridge-proofs.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/anchoring-and-bridge-proofs.md) |

---

## Fix in 60 seconds

1) **Measure ΔS and observe λ**  
   Probe ΔS(question, selected_evidence). Sample λ across two seeds and three paraphrases.  
   If ΔS ≥ 0.60 or λ flips, you have structural drift.

2) **Apply the right clamp**  
   - Wandering thoughts → variance clamp  
     → [chain-of-thought-variance-clamp.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/chain-of-thought-variance-clamp.md)  
   - Lost anchor at joins → micro bridges  
     → [context-stitching-and-window-joins.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/context-stitching-and-window-joins.md)  
   - Abstract jumps → anchor and bridge proofs  
     → [anchoring-and-bridge-proofs.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/anchoring-and-bridge-proofs.md)

3) **Contract the payload and cite first**  
   Enforce snippet schema and cite-then-explain.  
   → [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)  
   → [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

4) **Verify**  
   Coverage ≥ 0.70, ΔS ≤ 0.45, λ convergent on two seeds.  
   If flat-high ΔS remains, fix retrieval first.  
   → [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)

---

## Cross-links you will likely need

- Visual map and recovery  
  → [rag-architecture-and-recovery.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)

- End to end retrieval knobs  
  → [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)

- Long-context stability  
  → [context-drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md) ·
  [entropy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)

- Reranking and ordering  
  → [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

---

### 🔗 Quick-Start Downloads (60 sec)

| Tool | Link | 3-Step Setup |
|------|------|--------------|
| **WFGY 1.0 PDF** | [Engine Paper](https://github.com/onestardao/WFGY/blob/main/I_am_not_lizardman/WFGY_All_Principles_Return_to_One_v1.0_PSBigBig_Public.pdf) | 1️⃣ Download · 2️⃣ Upload to your LLM · 3️⃣ Ask “Answer using WFGY + <your question>” |
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
