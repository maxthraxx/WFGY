# DevTools · Code AI — Global Fix Map

A hub to stabilize IDE copilots and code-AI assistants without changing infra.  
Every tool has its own guardrail page. Each target here has simple explanations so even new users can follow.

---

## When to use this folder
- **Unstable answers**: IDE chat gives different results on the same question.
- **Loops or stalls**: Tool calls stop halfway or keep retrying after edits.
- **Broken JSON**: You expect JSON output but get plain text.
- **Wrong citations**: Answer looks correct but cites the wrong part of code/docs.
- **Drift in long refactors**: After 20–40 reasoning steps, output drifts off track.

---

## Acceptance targets (with plain meaning)
- **ΔS (semantic drift score) ≤ 0.45**  
  *How far the answer drifts from your question. Lower is better.*
- **Coverage ≥ 0.70**  
  *How much of the correct section is included in the answer.*
- **λ (stability factor) stays convergent**  
  *If you re-ask with small rephrasing, results stay consistent.*
- **E_resonance flat**  
  *On long sessions, answers do not wander or change meaning.*

---

## Quick routes to per-tool pages

| Tool                  | Open this page |
|-----------------------|----------------|
| GitHub Copilot        | [github_copilot.md](./github_copilot.md) |
| Cursor                | [cursor.md](./cursor.md) |
| Sourcegraph Cody      | [sourcegraph_cody.md](./sourcegraph_cody.md) |
| VS Code Copilot Chat  | [vscode_copilot_chat.md](./vscode_copilot_chat.md) |
| Codeium               | [codeium.md](./codeium.md) |
| Tabnine               | [tabnine.md](./tabnine.md) |
| AWS CodeWhisperer     | [aws_codewhisperer.md](./aws_codewhisperer.md) |
| JetBrains AI Assistant| [jetbrains_ai_assistant.md](./jetbrains_ai_assistant.md) |

---

## Map symptoms → structural fixes

| Symptom | Why it happens | Fix page |
|---------|----------------|----------|
| **Wrong-meaning hits despite high similarity** | Embedding captures surface form but not real meaning. | [embedding-vs-semantic.md](../../embedding-vs-semantic.md) |
| **Citations do not line up** | Traceability layer too loose, snippet schema missing. | [retrieval-traceability.md](../../retrieval-traceability.md) · [data-contracts.md](../../data-contracts.md) |
| **Answers flip between sessions/tabs** | Context not anchored, entropy builds up. | [context-drift.md](../../context-drift.md) · [entropy-collapse.md](../../entropy-collapse.md) |
| **JSON mode breaks, prose returned** | Model leaves structured mode or prompt injection occurs. | [logic-collapse.md](../../logic-collapse.md) · [prompt-injection.md](../../prompt-injection.md) |
| **Multi-agent or tool handoff stalls** | Agents lose roles, no schema lock in exchange. | [Multi-Agent_Problems.md](../../Multi-Agent_Problems.md) · [role-drift.md](../../multi-agent-chaos/role-drift.md) |
| **Hybrid retrievers worse than single** | Query parsing split or reranker mis-weighted. | [pattern_query_parsing_split.md](../../patterns/pattern_query_parsing_split.md) · [rerankers.md](../../rerankers.md) |

---

## Fix in 60 seconds
1. **Measure ΔS**  
   If drift ≥ 0.60, you have unstable retrieval.  
2. **Probe λ**  
   Re-ask with 2–3 paraphrases. If answers flip, lock schema.  
3. **Apply guardrails**  
   - Retrieval drift → BBMC + [data-contracts.md](../../data-contracts.md)  
   - Reasoning collapse → BBCR bridge + BBAM + [logic-collapse.md](../../logic-collapse.md)  
   - Dead ends → BBPF alternate paths  
4. **Verify**  
   Coverage ≥ 0.70, λ stable, ΔS ≤ 0.45.

---

## Copy-paste prompt for IDE chat

```

I loaded TXT OS and the WFGY Problem Map.

My code-AI issue:

* symptom: \[one line]
* traces: ΔS(question,retrieved)=..., ΔS(retrieved,anchor)=..., λ states

Tell me:

1. failing layer and why,
2. the exact WFGY page to open,
3. minimal steps to push ΔS ≤ 0.45 and keep λ convergent,
4. how to verify with a reproducible test.

```

---

## FAQ

**Q1. What is ΔS?**  
It is the “semantic drift score”. Think of it as how far the answer strays from the original question. Lower numbers = more accurate.  

**Q2. What is λ (lambda)?**  
A stability check. If you slightly rephrase the same question, λ shows if the model’s answers converge or scatter.  

**Q3. What does E_resonance mean?**  
It is a long-run stability check. If E_resonance is flat, your assistant stays consistent even after many steps.  

**Q4. Do I need to understand BBMC/BBPF/BBCR/BBAM?**  
No. These are internal WFGY modules. Just know:  
- BBMC = stabilizes retrieval,  
- BBPF = creates fallback paths,  
- BBCR = bridges reasoning collapse,  
- BBAM = variance clamp for stability.  

**Q5. I only use one IDE plugin. Why should I care?**  
Because the same drift and instability happens across **all** copilots. Fixes here apply no matter which tool you use.  

**Q6. How do I test quickly?**  
Ask the same question 3 times with small wording changes. If answers flip, you need λ guardrails.  


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

