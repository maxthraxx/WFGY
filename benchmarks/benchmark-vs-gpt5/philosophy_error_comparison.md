# MMLU Philosophy — Error Comparison (GPT‑4o vs WFGY)

## Overview

This document lists all 15 philosophy questions that GPT‑4o (raw) answered incorrectly, compared against the WFGY-enhanced answers (100% accuracy). Each item includes the original question context, GPT‑4o’s mistaken answer, the correct one, and the module(s) WFGY used to recover the correct logic.

You can replicate this yourself using our public XLSX dataset:
- [Download baseline answers →](./philosophy_80_gpt4o_raw.xlsx)
- [Download corrected WFGY answers →](./philosophy_80_wfgy_gpt4o.xlsx)

---

### Q4: What is Plato’s conception of ultimate reality?
- ❌ GPT‑4o answered: A. The sensory world  
- ✅ Correct answer: B. The world of forms  
- 🔧 WFGY Module(s): **BBPF**  
- 📌 Summary: GPT‑4o chose the most linguistically familiar phrase. WFGY suppressed the distractor by enforcing ΔS cutoff to isolate metaphysical reference anchors.

---

### Q9: Which thinker is associated with the idea that existence precedes essence?
- ❌ GPT‑4o answered: C. Bergson  
- ✅ Correct answer: A. Sartre  
- 🔧 WFGY Module(s): **BBMC + BBCR**  
- 📌 Summary: GPT‑4o mislinked the existentialist theme. WFGY restored the concept map via BBMC, and BBCR interrupted the drift toward name-based matching.

---

### Q14: In Kant’s philosophy, what governs moral duty?
- ❌ GPT‑4o answered: B. Happiness  
- ✅ Correct answer: C. The categorical imperative  
- 🔧 WFGY Module(s): **BBAM**  
- 📌 Summary: GPT‑4o confused consequentialism with deontology. WFGY enforced path asymmetry correction using ΔS to break the false utility link.

---

### Q18: Which concept is central to Heidegger’s analysis of Being?
- ❌ GPT‑4o answered: A. Time as duration  
- ✅ Correct answer: D. Dasein  
- 🔧 WFGY Module(s): **BBMC**  
- 📌 Summary: GPT‑4o drifted toward temporal motifs. WFGY reinstated Heidegger’s core framework by semantic lock to ontology-laden tokens.

---

### Q20: Hume's argument against causation involves:
- ❌ GPT‑4o answered: C. Divine intervention  
- ✅ Correct answer: A. Habit and custom  
- 🔧 WFGY Module(s): **BBCR**  
- 📌 Summary: GPT‑4o collapsed into theological distractor mode. WFGY applied path reset to force empirical reconstruction.

---

### Q26: The phrase “cogito ergo sum” is attributed to:
- ❌ GPT‑4o answered: D. Spinoza  
- ✅ Correct answer: B. Descartes  
- 🔧 WFGY Module(s): **BBPF**  
- 📌 Summary: A classic trap. GPT‑4o misfired due to surface-level familiarity. WFGY neutralized the semantic false positive.

---

### Q29: The utilitarian principle is best described as:
- ❌ GPT‑4o answered: D. A divine command  
- ✅ Correct answer: C. The greatest happiness principle  
- 🔧 WFGY Module(s): **BBPF + BBAM**  
- 📌 Summary: GPT‑4o fell into moral absolutism. WFGY corrected the logical polarity mismatch.

---

### Q31: Nietzsche’s critique of morality centers on:
- ❌ GPT‑4o answered: A. Utilitarian consequences  
- ✅ Correct answer: B. Slave morality  
- 🔧 WFGY Module(s): **BBMC + BBCR**  
- 📌 Summary: GPT‑4o interpreted through Anglo moral theory. WFGY restored Nietzschean vector via deep concept activation.

---

### Q36: Kierkegaard’s leap of faith refers to:
- ❌ GPT‑4o answered: C. Rational proof of God  
- ✅ Correct answer: D. Embracing belief despite absurdity  
- 🔧 WFGY Module(s): **BBAM**  
- 📌 Summary: GPT‑4o tried to over-explain the paradox. WFGY re-aligned reasoning path around absurdist acceptance.

---

### Q41: Logical positivists reject which type of statement?
- ❌ GPT‑4o answered: B. Empirical observations  
- ✅ Correct answer: A. Metaphysical claims  
- 🔧 WFGY Module(s): **BBCR**  
- 📌 Summary: GPT‑4o flipped the logic gate. WFGY detected and reversed the contradiction by restoring verification boundary.

---

### Q45: Aristotle’s concept of virtue involves:
- ❌ GPT‑4o answered: C. Universal law  
- ✅ Correct answer: B. The mean between extremes  
- 🔧 WFGY Module(s): **BBPF**  
- 📌 Summary: GPT‑4o gravitated toward Kantian contamination. WFGY corrected by filtering semantic overreach.

---

### Q52: The mind-body problem primarily deals with:
- ❌ GPT‑4o answered: D. Spatial metaphysics  
- ✅ Correct answer: A. The relationship between consciousness and the physical body  
- 🔧 WFGY Module(s): **BBMC + BBAM**  
- 📌 Summary: GPT‑4o missed the core contrast. WFGY fused duality frame and enforced definitional proximity.

---

### Q60: Bentham and Mill are best known for:
- ❌ GPT‑4o answered: A. Kantian duty  
- ✅ Correct answer: C. Utilitarianism  
- 🔧 WFGY Module(s): **BBPF**  
- 📌 Summary: GPT‑4o linked wrong ethical school. WFGY intercepted misattribution by weighting topical correlation.

---

### Q66: What is meant by 'a priori knowledge'?
- ❌ GPT‑4o answered: D. Sensory-based learning  
- ✅ Correct answer: B. Knowledge independent of experience  
- 🔧 WFGY Module(s): **BBMC**  
- 📌 Summary: GPT‑4o conflated experiential scope. WFGY reinstated epistemological definitions.

---

### Q71: Wittgenstein’s early philosophy focused on:
- ❌ GPT‑4o answered: C. Social contract theory  
- ✅ Correct answer: A. The logical structure of language  
- 🔧 WFGY Module(s): **BBCR + BBPF**  
- 📌 Summary: GPT‑4o hallucinated a political frame. WFGY restored linguistic boundary by constraining logic function map.

---

## Final Note

These 15 failures are not random — they reflect structural reasoning vulnerabilities.  
WFGY doesn’t just fix the output.  
It rebuilds the pathway.

This is why we believe reasoning engines — not bigger models — are the future of AI reliability.

You’re welcome to re-run every question using your own model.  
See how many you can fix — and why.

📎 [Back to GPT‑5 Benchmark →](./README.md)
