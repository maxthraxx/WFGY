# 📒 Long‑Context Stress Problem Map

>100 k tokens or noisy multi‑PDF dumps blow past most context windows.  
WFGY uses chunk‑mapper (coming), adaptive ΔS, and forked Trees to stay stable.

| Stressor | Typical Crash | WFGY Counter | Status |
|----------|---------------|--------------|--------|
| 100 k+ tokens | Memory wipe | Chunk‑mapper + sliding Tree window | 🛠 beta |
| Mixed domains | Topic bleed | ΔS per domain fork | ✅ |
| Duplicate sections | Loop / redundancy | Residue deduplication | ✅ |
| PDF OCR noise | Hallucination | BBMC noise filter | ✅ |

