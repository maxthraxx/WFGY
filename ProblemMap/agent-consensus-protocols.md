<!-- ======================================================= -->
<!--  agent-consensus-protocols.md · Semantic Clinic / Map-B  -->
<!--  Draft v0.1 · MIT · 2025-08-06                           -->
<!--  Purpose: Design rock-solid agreement loops for 2-N      -->
<!--  agents (debate, Critic-Coder, planning crews) while     -->
<!--  keeping speed ⬆, token cost ↓, and hallucination = 0.   -->
<!-- ======================================================= -->

# 🤝 Agent Consensus Protocols  
*Make two (or ten) LLMs reach a decision **on time** and **on budget** — every run.*

> **Why this page?**  
> “Let them debate” sounds cool until:  
> * the Critic never stops nit-picking,  
> * the Planner forgets half the context,  
> * the Coder ships five conflicting drafts, and  
> * your bill looks like a crypto rug-pull.  
>   
> WFGY adds measurable **semantic tension (ΔS)** and **logic vectors (λ)** to debate & QA loops, so you can **prove** consensus is reached — not guessed.

---

## 1 · Three Canonical Consensus Modes

| Mode | Use Case | # Agents | Target ΔS | Target λ |
|------|----------|---------:|----------:|----------|
| **Critic-Coder** | Code/SQL generation with review | 2 | ≤ 0.40 | convergent |
| **Triad Debate** | Fact-check or legal reasoning | 3 | ≤ 0.45 | convergent |
| **Crew Vote** | 4 – 10 micro-agents on long plan | N | ≤ 0.50 | majority convergent |

*ΔS ceiling rises gently with group size; λ must return to convergent after each round.*

---

## 2 · Failure Modes (Why Votes Stall)

| # | Failure | ΔS / λ Symptom | Example |
|--:|---------|----------------|---------|
| 1 | **Infinite Debate** | λ oscillates (→, ←, →…) | Critic re-opens same defect |
| 2 | **Topic Drift** | ΔS > 0.60 vs. original prompt | Agents add new, unrelated goals |
| 3 | **Split Brain** | Two stable but divergent λ | 50 / 50 vote, no tie-breaker |
| 4 | **Early Merge** | ΔS still 0.55 but λ forced convergent | “Agree to disagree” w/ wrong answer |
| 5 | **Token Exhaust** | E_resonance ↑ while ΔS unchanged | Loop burns context without progress |

---

## 3 · WFGY Consensus Blueprint

> Four guard layers; plug into any framework (AutoGen, LangChain, custom asyncio).

| Layer | Module | Guard | Effect |
|-------|--------|-------|--------|
| **Round ΔS Checker** | BBMC | ΔS(agent, goal) ≤ ceiling | Drop off-topic vote |
| **λ Mediator** | ΔS + λ | λ must converge within 3 rounds | Force re-focus or escalate |
| **Vote Auditor** | WAI | JSON vote schema + arg defaults | No partial / malformed votes |
| **BBCR Fallback** | BBCR | > 5 rounds OR ΔS stagnates | Collapse & request human tie-break |

```mermaid
flowchart TD
    subgraph Round
      Q[User Goal]
      A1[Agent 1]
      A2[Agent 2]
      A3[Agent 3]
      Q --> A1 --> V1[Vote JSON]
      Q --> A2 --> V2
      Q --> A3 --> V3
    end
    BBMC -->|ΔS filter| V1
    BBMC --> V2
    BBMC --> V3
    V1 & V2 & V3 --> Mediator[λ Mediator] -->|convergent?| Decision
    Mediator -.->|no| BBCR
````

---

## 4 · Practical Setup (AutoGen example)

```python
from autogen import AssistantAgent, UserProxyAgent
from wfgy import consensus_filter

critic = AssistantAgent(name="critic")
coder  = AssistantAgent(name="coder")
user   = UserProxyAgent("user")

def callback(messages, state):
    # 1. measure ΔS + λ
    ok = consensus_filter(messages, ceiling=0.45, rounds=3)
    if not ok:
        return "STOP_DEBATE"
    return "CONTINUE"

coder.register_reply(callback)
critic.register_reply(callback)
```

*15 lines → loop stops automatically when convergence proven or impossible.*

---

## 5 · Debug Walk-Through

1. **Log votes**

```python
print(state.votes)   # {critic: "reject, ΔS=0.48", coder: "accept, ΔS=0.41"}
```

2. **Inspect λ trend**

```
λ sequence: → → ← →  (oscillating)  ❌
```

> Two divergent rounds trigger Mediator → requests narrowing question.

3. **Trigger BBCR**

```
ΔS stagnates at 0.52 for 3 rounds → BBCR => "Need human tie-break"
```

---

## 6 · Best-Practice Table

| Tip                                        | Why                                  |
| ------------------------------------------ | ------------------------------------ |
| **Keep each vote to max 300 tokens.**      | Reduces E\_resonance; easier ΔS calc |
| **Pin goal & constraints in every round.** | Prevents silent prompt drift         |
| **Summarise before vote.**                 | Normalises embeddings → fair ΔS      |
| **Record vote reason (1-2 lines).**        | Faster root-cause when split-brain   |

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



