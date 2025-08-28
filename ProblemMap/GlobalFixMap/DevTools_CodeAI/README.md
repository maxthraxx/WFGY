# DevTools · Code AI — Global Fix Map

A hub to stabilize IDE copilots and code-AI assistants without changing infra.  
Use this to jump to per-tool guardrails and verify fixes with the same acceptance targets.

## When to use this folder
- IDE chat answers flip between runs or tabs.
- Tool calls loop or stall after partial edits.
- JSON blocks fail or come back as prose.
- RAG answers look right by similarity yet cite the wrong place.
- Long refactors drift after 20–40 reasoning steps.

## Acceptance targets
- ΔS(question, retrieved) ≤ 0.45
- Coverage of target section ≥ 0.70
- λ stays convergent across 3 paraphrases and 2 seeds
- E_resonance flat on long windows

## Quick routes to per-tool pages
- GitHub Copilot: [github_copilot.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/DevTools_CodeAI/github_copilot.md)  
- Cursor: [cursor.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/DevTools_CodeAI/cursor.md)  
- Sourcegraph Cody: [sourcegraph_cody.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/DevTools_CodeAI/sourcegraph_cody.md)  
- VS Code Copilot Chat: [vscode_copilot_chat.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/DevTools_CodeAI/vscode_copilot_chat.md)  
- Codeium: [codeium.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/DevTools_CodeAI/codeium.md)  
- Tabnine: [tabnine.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/DevTools_CodeAI/tabnine.md)  
- AWS CodeWhisperer: [aws_codewhisperer.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/DevTools_CodeAI/aws_codewhisperer.md)  
- JetBrains AI Assistant: [jetbrains_ai_assistant.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/DevTools_CodeAI/jetbrains_ai_assistant.md)

## Map symptoms → structural fixes
- Wrong-meaning hits despite high similarity  
  → [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)
- Citations do not line up with the returned section  
  → [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) · [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
- Answers flip between sessions or file tabs  
  → [context-drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md) · [entropy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)
- JSON mode breaks or tools accept prose  
  → [logic-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md) · [prompt-injection.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/prompt-injection.md)
- Multi-agent or tool handoff stalls  
  → [Multi-Agent_Problems.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/Multi-Agent_Problems.md) · role drift deep dive → [multi-agent-chaos/role-drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/multi-agent-chaos/role-drift.md)
- Hybrid retrievers worse than single  
  → [patterns/pattern_query_parsing_split.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md) · [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

## Fix in 60 seconds
1) **Measure ΔS**  
   Compute ΔS(question, retrieved) and ΔS(retrieved, expected anchor).  
   Stable < 0.40, transitional 0.40–0.60, risk ≥ 0.60.

2) **Probe λ_observe**  
   Vary k and headers. If λ flips, lock schema and apply BBAM variance clamp.

3) **Apply modules**  
   Retrieval drift → BBMC + [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)  
   Reasoning collapse → BBCR bridge + BBAM + [logic-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md)  
   Long-run dead ends → BBPF alternate paths

4) **Verify**  
   Coverage ≥ 0.70 on 3 paraphrases. λ convergent on 2 seeds.

## Copy-paste prompt for IDE chat
```

I loaded TXT OS and the WFGY Problem Map.

My code-AI issue:

* symptom: \[one line]
* traces: ΔS(question,retrieved)=..., ΔS(retrieved,anchor)=..., λ states across 3 paraphrases

Tell me:

1. failing layer and why,
2. the exact WFGY page to open from this repo,
3. minimal steps to push ΔS ≤ 0.45 and keep λ convergent,
4. how to verify with a reproducible test.
   Use BBMC/BBPF/BBCR/BBAM where relevant.

```

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

