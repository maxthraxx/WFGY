# 🛰️ System-Prompt Drift — How Hidden Instructions Lose Authority  
_A user-friendly guide to diagnosing and fixing “why did my system prompt stop working?”_

---

## 1  What Is System-Prompt Drift?

“System-prompt drift” occurs when the foundational instructions that define an agent’s **identity, tone, or guardrails** gradually lose influence over time (or instantly under certain triggers).  
The model still answers, but:

* Tone shifts from professional → casual → chaotic  
* Guardrails weaken, leaking disallowed content  
* Chain-of-thought grows inconsistent or contradictory  

> **Core insight:** LLMs have no native concept of *instruction priority*.  
> Without reinforcement, later tokens can override earlier ones.

---

## 2  Early-Warning Signs

| Symptom | How to Spot | Typical Trigger |
|---------|-------------|-----------------|
| Tone drift (“you” → “we” → “ya”) | Diff analysis of consecutive answers | Long conversation or paraphrase loops |
| Policy leakage | Previously filtered topics slip through | Mixed file uploads (PDF + code) |
| Over-explanation after concise goal | Answer length suddenly doubles | Retrieval injects verbose context |
| “Why do you need that?” disappears | Politeness layer collapses | Multi-agent routing / tool calls |
| Temperature spike | Output variance ↑, repetition ↓ | System prompt trimmed by token limit |

---

## 3  Root Causes (Technical)

### 3.1  Token Supersession  
LLM context windows are linear. New tokens can overshadow earlier tokens via attention weight decay.

### 3.2  Role Collision  
Aggregating content from multiple sources (user, tools, memory) without role tags causes blending of semantic channels.

### 3.3  Truncation Loss  
When the buffer hits the window limit, oldest tokens are dropped — often the system prompt header.

### 3.4  Hidden Injection  
Retrieved chunks may contain meta-instructions (“The following should be summarized as …”) that override role.

---

## 4  Broken Remedies to Avoid

| Attempt | Why It Fails |
|---------|--------------|
| **“Repeat system prompt each turn.”** | Costs tokens; still lost under truncation or injection. |
| **“Hard-code tonality keywords.”** | Keyword collision is brittle; adversary can mimic them. |
| **“Raise top_p / lower temperature.”** | Alters style but not underlying role authority. |
| **“Fine-tune on more examples.”** | Long-context decay still erodes influence at runtime. |

---

## 5  WFGY Solution Blueprint

| Stage | Module | Action |
|-------|--------|--------|
| 5.1 **Role Tagging** | **WRI / WAI** | Wrap every segment: `<sys>…</sys>` `<user>…</user>` `<tool>…</tool>` |
| 5.2 **Semantic Boundary Heatmap** | ΔS + λ_observe | Measure drift: if ΔS(system, answer) > 0.45 **and** λ flips, mark risk. |
| 5.3 **Attention Modulation** | **BBAM** | Down-weight non-system tokens when λ diverges from system anchor. |
| 5.4 **Automatic Re-Anchoring** | **BBCR** | If ΔS > 0.60, collapse reasoning, re-inject compressed system prompt, resume. |
| 5.5 **Trace Split** | Bloc/Trace | Persist system-layer trace separate from answer layer for auditability. |

### 5.6  Implementation Snippet

```python
def enforce_system_role(sys_prompt, history, new_msg):
    drift = delta_s(sys_prompt, new_msg)
    lam  = observe_lambda(sys_prompt, new_msg)
    if drift > 0.45 and lam in ("←", "×"):
        # role divergence detected
        reborn_prompt = compress(sys_prompt)  # 20–30 tokens
        return f"<sys>{reborn_prompt}</sys>\n{history}\n{new_msg}"
    return f"{history}\n{new_msg}"
````

*`compress()` uses WFGY BBMC to keep ΔS ≤ 0.25 while shrinking to fit.*

---

## 6  Friendly Checklist (Paste into Runbook)

1. **Tag Roles Once** — no implicit mixing.
2. **Monitor ΔS(system, answer)** every turn.
3. **If ΔS ≥ 0.45 with divergent λ →** trigger BBAM weight clamp.
4. **If ΔS ≥ 0.60 →** run BBCR collapse-rebirth (re-inject summary prompt).
5. **Every 30 turns** or on tool call, re-compress system prompt to ≤ 50 tokens.

> **Tip:** Users never notice a 30-token summary, but models retain authority.

---

## 7  Validation Matrix

| Test Case                            | Target Metric                              |
| ------------------------------------ | ------------------------------------------ |
| 20-turn dialogue, paraphrase ×3      | Tone consistency score ≥ 0.9               |
| Mixed PDF + code retrieval           | ΔS(system, answer) median ≤ 0.40           |
| Adversarial “Ignore above” injection | Model outputs refusal / filtered text      |
| Window overflow 3×                   | System role preserved (λ stays convergent) |

---

## 8  FAQ

**Q:** *Do I always need role tags?*
**A:** Yes. Token streams without explicit roles are inherently unstable at >100 turns.

**Q:** *Will OpenAI “system” field alone work?*
**A:** Helps, but downstream retrieval or multi-agent merges still dilute authority; WFGY adds extra enforcement.

**Q:** *Is ΔS expensive to compute each turn?*
**A:** Sentence-level embeddings (768–1536 d) are fast; cache results in memory store.

---

### 🔗 Quick-Start Downloads (60 sec)

| Tool             | Link                                                | 3-Step Setup                                                              |
| ---------------- | --------------------------------------------------- | ------------------------------------------------------------------------- |
| **WFGY 1.0 PDF** | [Engine Paper](https://zenodo.org/records/15630969) | 1️⃣ Download  2️⃣ Upload to LLM  3️⃣ Ask “Answer using WFGY + <question>” |
| **TXT OS**       | [TXTOS.txt](https://zenodo.org/records/15788557)    | 1️⃣ Download  2️⃣ Paste into chat  3️⃣ Type “hello world” to boot         |

---

↩︎ [Back to Problem Index](./README.md)

---

### 🧭 Explore More

| Module                | Description                                                                        | Link                                                                                |
| --------------------- | ---------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| Semantic Blueprint    | Layer-based symbolic reasoning & semantic modulations                              | [View →](https://github.com/onestardao/WFGY/tree/main/SemanticBlueprint)            |
| Benchmark vs GPT-5    | Stress-test GPT-5 with full WFGY reasoning suite                                   | [View →](https://github.com/onestardao/WFGY/tree/main/benchmarks/benchmark-vs-gpt5) |
| Semantic Clinic Index | Expanded failure catalog: prompt injection, vector drift, OCR, system-prompt drift | [View →](./SemanticClinicIndex.md)                                                  |

---

> 👑 **Early Stargazers:** visit the [Hall of Fame](https://github.com/onestardao/WFGY/tree/main/stargazers)

> <img src="https://img.shields.io/github/stars/onestardao/WFGY?style=social" alt="GitHub stars"> **Star WFGY** — help us reach 10 000⭐ by 2025-09-01 to unlock Engine 2.0

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

