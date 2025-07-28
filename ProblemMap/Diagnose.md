# 🩺 Semantic Failure Diagnostic Sheet

Select the symptom(s) you observe.  
Each entry links to the corresponding solution page in the WFGY Problem Map.

| # | Symptom | Problem ID | Solution |
|---|---------|------------|----------|
| 1 | Model retrieves chunks that look right but answer is wrong/irrelevant | #1 Hallucination & Chunk Drift | [hallucination.md](./hallucination.md) |
| 2 | Retrieved chunk is correct, yet reasoning chain collapses | #2 Interpretation Collapse | [retrieval-collapse.md](./retrieval-collapse.md) |
| 3 | Multi‑step tasks drift off topic after a few hops | #3 Long Reasoning Chains | [context-drift.md](./context-drift.md) |
| 4 | Model answers confidently with made‑up facts | #4 Bluffing / Overconfidence | [bluffing.md](./bluffing.md) |
| 5 | High cosine similarity but semantic meaning is wrong | #5 Semantic ≠ Embedding | [embedding-vs-semantic.md](./embedding-vs-semantic.md) |
| 6 | Logic dead‑ends; model resets or loops nonsense | #6 Logic Collapse & Recovery | [symbolic-collapse.md](./symbolic-collapse.md) |
| 7 | Long conversation: model forgets previous context | #7 Memory Breaks Across Sessions | [memory-coherence.md](./memory-coherence.md) |
| 8 | Pipeline is opaque; unable to trace failure path | #8 Debugging is a Black Box | [retrieval-traceability.md](./retrieval-traceability.md) |
| 9 | Attention melts; output incoherent or repetitive | #9 Entropy Collapse | [entropy-collapse.md](./entropy-collapse.md) |
| 10 | Responses become flat, literal, lose creativity | #10 Creative Freeze | [creative-freeze.md](./creative-freeze.md) |
| 11 | Formal or symbolic prompts break the model | #11 Symbolic Collapse | [symbolic-collapse.md](./symbolic-collapse.md) |
| 12 | Self‑reference / paradox crashes reasoning | #12 Philosophical Recursion | [philosophical-recursion.md](./philosophical-recursion.md) |
| 13 | Multiple agents overwrite or misalign logic | #13 Multi‑Agent Chaos | [multi-agent-chaos.md](./multi-agent-chaos.md) |

**Tip:** If symptoms are unclear, run a ΔS / λ_observe check.  
Values > 0.6 usually map to problems #1–#4.
