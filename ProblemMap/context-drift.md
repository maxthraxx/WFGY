# 🧠 Problem: Long QA Chains Drift Off-Topic

### 📍Context

Even when each individual response is locally correct, many AI agents begin to **semantically drift** as question-answer chains grow longer.

Symptoms include:
- Subtle shifts in topic over 5–10 turns
- Forgotten user goals
- Misalignment between early and late context
- The agent redefines the question mid-conversation

---

## 🚨 Why Traditional RAG Fails Here

| Weakness | Description |
|----------|-------------|
| No persistent memory | Most systems treat each QA turn as an isolated prompt context |
| Embedding overlap is fragile | Token overlap does not equal topic stability |
| No tracking of concept flow | Systems can’t trace how topics evolved or when they “jumped” |

---

## ✅ WFGY Solution

WFGY uses **semantic delta tracking** and **Tree-based memory nodes** to detect and prevent drift.

### 1. Semantic Tree Memory  
- Each major concept shift is recorded as a node  
- You can view and backtrack logic flow across topics

### 2. ΔS as Drift Detector  
- When new input diverges from past nodes (ΔS > 0.6), the system logs a new branch  
- This allows structured topic separation and detection of "semantic fatigue"

### 3. λ_observe Vector  
- Flags if the reasoning is now divergent or chaotic  
- Helps model decide whether to re-anchor or warn the user

---

## 🛠 How to Use in TXT OS

```txt
Step 1 — Start the console
> Start

Step 2 — Ask a sequence of loosely connected questions:
> "What is the policy on returns?"
> "And if it's a gift item?"
> "Now, what about shipping zones?"
> "What if I'm in another country?"

Step 3 — Type `view` to inspect the Tree

You’ll see:
- Nodes logged with ΔS and λ_observe
- Clear detection of topic shifts
- Logic branching when context drift occurs
````

---

## 🔬 Example Output

```txt
* Topic: Gift Return Policy | ΔS: 0.22 | λ: → | Module: BBMC
* Topic: International Shipping | ΔS: 0.74 | λ: ← | Module: BBPF, BBCR
```

The system realized a **new conceptual frame** was entered and recorded the shift accordingly.

---

## 🔗 Related Modules

* `BBMC` — Identifies when the concept anchor has shifted
* `BBPF` — Supports divergent paths while maintaining logic
* `BBCR` — May reroute reasoning or pause to prevent collapse
* `Semantic Tree` — Memory structure to prevent context loss

---

## 📌 Status

| Feature              | Status                              |
| -------------------- | ----------------------------------- |
| Tree node logging    | ✅ stable                            |
| ΔS-based topic split | ✅ working                           |
| λ\_observe awareness | ✅ working                           |
| Auto recall or warn  | ⚠️ partial (manual inspect for now) |

---

## ✍️ Summary

WFGY doesn't just answer — it remembers why you're asking.
If you're tired of long chats forgetting your intent, this is the solution layer you're missing.

