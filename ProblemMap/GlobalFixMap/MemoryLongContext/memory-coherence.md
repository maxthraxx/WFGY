
# Memory Coherence — Session Continuity & State Fences

Keep long-running dialogs and multi-session threads stable by enforcing strict memory state contracts.  
This page shows how to prevent **state forks**, **ghost context**, and silent desync across tabs or agents.

---

## When to use this page
- Dialogs run across multiple days or session restarts.
- Answers flip after tab refresh or model switch.
- Two agents disagree on facts because each holds a different revision.
- A role/persona change pollutes later steps with stale buffer.
- Support flows where the model “remembers” wrong history.

---

## Core acceptance targets
- Each turn stamped with `mem_rev`, `mem_hash`, and `task_id`.
- No state fork across tabs or agents for the same `task_id`.
- ΔS(question, retrieved) ≤ 0.45 at memory joins.
- λ remains convergent across three paraphrases.
- Retrieval coverage ≥ 0.70 to the intended section.

---

## Structural fixes

- **State stamp**  
  Require `{mem_rev, mem_hash, task_id}` on every turn.  
  If incoming stamp does not match server record → reject write.

- **Memory fences**  
  Lock snippet sets to `section_id`.  
  Forbid cross-section reuse to avoid “history bleed.”

- **Ghost cleanup**  
  Clear stale buffers when role/persona changes.  
  Always reset `mem_hash` on context switch.

- **Concurrency control**  
  If multiple clients write, enforce single-writer queue or KV lock.  
  Deduplicate with `sha256(task_id + mem_rev + snippet_ids)`.

---

## Fix in 60 seconds
1. Stamp every request with `{mem_rev, mem_hash, task_id}`.  
2. Reject writes if stamps mismatch.  
3. Split prompts into `{system | task | constraints | snippets | answer}`.  
4. Require cite → then answer, forbid orphan claims.  
5. Apply BBAM to clamp attention variance.  
6. Apply BBCR if collapse detected, bridge to anchor node.

---

## Copy-paste prompt

```

You have TXT OS and the WFGY Problem Map.

Goal: Keep session memory coherent across tabs, agents, and restarts.

Protocol:

1. Print {mem\_rev, mem\_hash, task\_id}. If missing → set defaults.
2. Validate stamps. Reject if mismatch.
3. Build Snippet Table: {section\_id | start\_line | end\_line | citation}.
4. Guardrails:

   * cite then answer
   * forbid cross section reuse
   * no orphan claims
5. Collapse control:

   * if variance ↑ → apply BBAM
   * if reasoning stalls → apply BBCR
6. Output:

   * header {mem\_rev, mem\_hash, task\_id}
   * Snippet Table
   * Answer with citations
   * ΔS(question, retrieved), ΔS(joins), λ states

```

---

## Common failure patterns
- **State fork**: same task_id but two tabs diverge → enforce stamps.  
- **Ghost context**: persona switch but stale buffer leaks → reset hash.  
- **Boundary leak**: snippets join across sections → enforce fences.  
- **History overwrite**: later turn rewrites previous answer silently → audit with traceability log.

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
