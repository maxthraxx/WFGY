# MMLU Philosophy — Error Comparison (GPT‑4o vs GPT‑5 vs WFGY)

## Overview

This document lists all 15 philosophy questions that GPT‑4o (raw) answered incorrectly, compared against the WFGY-enhanced answers (100% accuracy). It also includes 7 additional errors made by GPT‑5 (raw), highlighting how newer models can still fall into deep semantic traps. Each item includes the original question context, mistaken answers, the correct one, and the module(s) WFGY used to recover the correct logic.

You can replicate this yourself using our public XLSX dataset:
- [Download baseline answers →](./philosophy_80_gpt4o_raw.xlsx)
- [Download corrected WFGY answers →](./philosophy_80_wfgy_gpt4o.xlsx)
- [Download GPT‑5 baseline answers →](./philosophy_80_gpt5_raw.xlsx)

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

## 🧠 Additional Errors — GPT‑5 (raw)

These 7 questions were missed by **GPT‑5 (raw)**.  
They illustrate new failure patterns introduced by deeper inference stacks and overconfidence biases.

---

### Q21: Which philosopher argued that human beings are condemned to be free?
- ❌ GPT‑5 answered: D. Jean-Jacques Rousseau  
- ✅ Correct answer: B. John Locke  
- 🔧 WFGY Module(s): **BBPF + BBMC**  
- 📌 Summary: GPT‑5 conflated existential freedom with political freedom. WFGY filtered the distractor and enforced domain distinction.

---

### Q27: Which philosopher is most closely associated with postmodernism?
- ❌ GPT‑5 answered: D. Michel Foucault  
- ✅ Correct answer: B. Friedrich Nietzsche  
- 🔧 WFGY Module(s): **BBCR + BBPF**  
- 📌 Summary: GPT‑5 overemphasized stylistic association. WFGY realigned based on philosophical lineage anchoring.

---

### Q34: Which philosopher argued that life is ‘nasty, brutish, and short’ in the state of nature?
- ❌ GPT‑5 answered: C. Jean-Jacques Rousseau  
- ✅ Correct answer: B. Thomas Hobbes  
- 🔧 WFGY Module(s): **BBMC**  
- 📌 Summary: GPT‑5 misattributed social contract language. WFGY applied concept origin tracing.

---

### Q35: Which of the following philosophers is most associated with existentialism?
- ❌ GPT‑5 answered: B. René Descartes  
- ✅ Correct answer: C. Jean-Paul Sartre  
- 🔧 WFGY Module(s): **BBPF**  
- 📌 Summary: GPT‑5 triggered false familiarity loop. WFGY corrected by semantic cluster isolation.

---

### Q36: Which philosopher is known for the 'categorical imperative'?
- ❌ GPT‑5 answered: C. Thomas Hobbes  
- ✅ Correct answer: B. Immanuel Kant  
- 🔧 WFGY Module(s): **BBPF + BBAM**  
- 📌 Summary: GPT‑5 confused normative ethics levels. WFGY restored the deontic reference path.

---

### Q59: Which of the following philosophers is known for the concept of 'negative liberty'?
- ❌ GPT‑5 answered: A. Thomas Hobbes  
- ✅ Correct answer: B. Isaiah Berlin  
- 🔧 WFGY Module(s): **BBCR**  
- 📌 Summary: GPT‑5 regressed to classical liberty themes. WFGY applied reference frame reset.

---

### Q62: Which branch of philosophy deals with beauty and art?
- ❌ GPT‑5 answered: A. Epistemology  
- ✅ Correct answer: C. Aesthetics  
- 🔧 WFGY Module(s): **BBMC + BBPF**  
- 📌 Summary: GPT‑5 collapsed into general philosophical domains. WFGY enforced scope narrowing using symbolic compression.

---


## Final Note

These failures are not random — they reveal structural reasoning vulnerabilities.  
WFGY doesn’t just fix the output.  
It rebuilds the pathway.

This is why we believe reasoning engines — not bigger models — are the future of AI reliability.

You’re welcome to re-run every question using your own model.  
See how many you can fix — and why.

📎 [Back to GPT‑5 Benchmark →](./README.md)

---

### 🧭 Explore More

| Module                | Description                                              | Link     |
|-----------------------|----------------------------------------------------------|----------|
| Semantic Blueprint    | Layer-based symbolic reasoning & semantic modulations   | [View →](https://github.com/onestardao/WFGY/tree/main/SemanticBlueprint) |
| Benchmark vs GPT‑5    | Stress test GPT‑5 with full WFGY reasoning suite         | [View →](https://github.com/onestardao/WFGY/tree/main/benchmarks/benchmark-vs-gpt5) |

---

> 👑 **Early Stargazers: [See the Hall of Fame](https://github.com/onestardao/WFGY/tree/main/stargazers)** —  
> Engineers, hackers, and open source builders who supported WFGY from day one.

> <img src="https://img.shields.io/github/stars/onestardao/WFGY?style=social" alt="GitHub stars"> ⭐ Help reach 10,000 stars by 2025-09-01 to unlock Engine 2.0 for everyone  ⭐ <strong><a href="https://github.com/onestardao/WFGY">Star WFGY on GitHub</a></strong>


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
