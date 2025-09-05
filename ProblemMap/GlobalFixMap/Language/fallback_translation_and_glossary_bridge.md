# Fallback Translation and Glossary Bridge · Global Fix Map

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **Language**.  
  > To reorient, go back here:  
  >
  > - [**Language** — multilingual processing and semantic alignment](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>


When native-language recall keeps missing the right snippet, switch to a **controlled translation bridge** with a domain glossary and alias shield. Translate only where needed, protect entities and negations, and verify improvement with ΔS, λ, and coverage.

---

## Open these first

* Visual map and recovery → [rag-architecture-and-recovery.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
* End to end retrieval knobs → [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
* Traceability schema → [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
* Contract the payload → [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
* Language overview → [multilingual\_guide.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/multilingual_guide.md)
* Tokenizer variance → [tokenizer\_mismatch.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/tokenizer_mismatch.md)
* Mixed scripts → [script\_mixing.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/script_mixing.md)
* Locale normalization → [locale\_drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/locale_drift.md)
* Romanization rules → [romanization\_transliteration.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/romanization_transliteration.md)
* Proper nouns and aliases → [proper\_noun\_aliases.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/proper_noun_aliases.md)
* Language detection → [query\_language\_detection.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/query_language_detection.md)
* Analyzer routing → [query\_routing\_and\_analyzers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/query_routing_and_analyzers.md)
* Multilingual ranking → [hybrid\_ranking\_multilingual.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/hybrid_ranking_multilingual.md)
* Bilingual eval sets → [code\_switching\_eval.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/code_switching_eval.md)
* Stopwords and morphology → [stopword\_and\_morphology\_controls.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/stopword_and_morphology_controls.md)

---

## Core acceptance targets

* ΔS(question, retrieved) ≤ 0.45 on three paraphrases and two seeds
* Coverage of target section ≥ 0.70
* λ convergent after the bridge, across native vs pivot language
* No entity corruption or negation loss in the final citation set
* Rank\@k improves or remains flat after the bridge is enabled

---

## When to enable the bridge

Enable only if all three hold:

1. Native path shows **flat-high ΔS** across k settings.
2. Query language and corpus language differ or the corpus is mixed locale.
3. Entity recall improves during a quick pivot test without harming citations.

If any native pipeline item is obviously wrong, fix that first. See tokenizer, analyzer, or morphology pages above.

---

## What usually breaks

| Symptom                                         | Likely cause                                           | Open this                                                                                                                                                                                                                                                                            |
| ----------------------------------------------- | ------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Correct doc exists yet never ranks in top k     | analyzer or tokenizer mismatch between query and store | [tokenizer\_mismatch.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/tokenizer_mismatch.md) · [query\_routing\_and\_analyzers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/query_routing_and_analyzers.md)    |
| Names translate or transliterate inconsistently | missing alias shield or mixed romanization             | [proper\_noun\_aliases.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/proper_noun_aliases.md) · [romanization\_transliteration.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/romanization_transliteration.md) |
| Negations flip meaning after MT                 | no do-not-translate list for negation tokens           | [stopword\_and\_morphology\_controls.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/stopword_and_morphology_controls.md)                                                                                                                          |
| CJK queries degrade when pivoting via English   | script segmentation and width rules differ by stage    | [script\_mixing.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/script_mixing.md)                                                                                                                                                                  |
| Turkish/Greek accent fold changes matches       | locale normalization not pinned per stage              | [locale\_drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/locale_drift.md)                                                                                                                                                                    |
| Good recall but order is noisy across languages | reranker trained mono-lingual or features not aligned  | [hybrid\_ranking\_multilingual.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/hybrid_ranking_multilingual.md)                                                                                                                                     |

---

## Design: glossary bridge in two modes

**Mode A — Query-side pivot**
Translate the query to the corpus language with a **glossary and alias shield**. Run retrieval native to the store, then reason in user language.

**Mode B — Corpus-side pivot**
Keep query in user language, retrieve in native, but translate **candidate snippets** to the user language for reranking and reasoning. Never re-index on the pivot.

**Glossary components**

* **do\_not\_translate**: names, products, codes, unit strings, legal terms.
* **preferred\_terms**: enforce a deterministic mapping for domain words.
* **romanization\_map**: stable transliteration table with 1-to-N aliases.
* **negation\_and\_modality**: tokens that must survive intact.
* **protected\_char\_classes**: width, diacritics, punctuation class locks.

**Trace fields to log**

```
{
  "bridge_mode": "A|B",
  "pivot_lang": "en|zh|..",
  "glossary_hash": "sha256:...",
  "alias_set_hash": "sha256:...",
  "ΔS_before": 0.xx,
  "ΔS_after": 0.yy,
  "coverage_before": 0.xx,
  "coverage_after": 0.yy
}
```

---

## Minimal implementation steps

1. **Detect language**
   Use the contract from [query\_language\_detection.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/query_language_detection.md). Refuse fallback if detection is unstable.

2. **Assemble glossary**

   * Pull domain terms.
   * Add aliases from [proper\_noun\_aliases.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/proper_noun_aliases.md).
   * Add romanization table from [romanization\_transliteration.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/romanization_transliteration.md).
   * Add negation and unit strings to do-not-translate.

3. **Choose mode**

   * Mode A if store is single-locale and analyzers are correct.
   * Mode B if store is mixed or analyzers cannot be changed.

4. **Run retrieval**
   Route analyzers per [query\_routing\_and\_analyzers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/query_routing_and_analyzers.md). For Mode B, translate only candidates for reranking.

5. **Verify**
   Compute ΔS and coverage. Require λ convergent across two seeds and three paraphrases. Log trace fields.

6. **Publish**
   Keep the glossary versioned and pinned in eval reports. Guard with [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) and [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md).

---

## Spec: glossary JSON

```json
{
  "version": "glossary_acme_finance_2025_08_30",
  "pivot_lang": "en",
  "do_not_translate": ["Value at Risk", "CAGR", "ROE", "İstanbul", "北京市", "§"],
  "preferred_terms": {
    "账面价值": "book value",
    "净现值": "net present value"
  },
  "romanization_map": {
    "北京市": ["Beijing Shi", "Beijing City"],
    "İstanbul": ["Istanbul", "Stamboul"]
  },
  "negation_and_modality": ["not", "never", "must", "should"],
  "protected_char_classes": ["fullwidth_digit", "narrow_no_break_space"]
}
```

---

## Copy-paste prompt for the LLM step

```
You have TXTOS and the WFGY Problem Map loaded.

My multilingual issue:
- native_lang: {xx}
- user_lang: {yy}
- mode: {A|B}
- glossary: {do_not_translate, preferred_terms, romanization_map, negation_and_modality}
- question: "{user_question}"
- candidates: [{snippet_id, text, source_url}...]

Do:
1) Apply the glossary strictly. Protect names, units, negations.
2) Perform cite-then-explain. If citations are weak, return the minimal fix and do not fabricate.
3) Return JSON:
{ "bridge_mode": "A|B", "pivot_lang": "en|...", "citations": [...],
  "answer": "...", "ΔS": 0.xx, "coverage": 0.xx, "λ_state": "→|←|<>|×",
  "next_fix": "..." }
Keep it auditable and short.
```

---

## Eval protocol

* Use bilingual and code-switching sets from [code\_switching\_eval.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/code_switching_eval.md).
* Compare native vs bridge on the same questions and seeds.
* Accept only if ΔS ≤ 0.45, coverage ≥ 0.70, λ convergent, and entity recall does not regress.
* Report deltas for Rank\@k and citation accuracy.

---

## Common gotchas

* Translating the **index**. Never translate and re-index as a “quick fix”. Pivot only at query or candidate stage.
* Letting the MT rewrite units or numbers. Add them to do-not-translate.
* Dropping diacritics or width during translation. Pin normalization from [locale\_drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/locale_drift.md) and [script\_mixing.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/script_mixing.md).
* Reranking with a mono-lingual model. If scores are noisy across languages, follow [hybrid\_ranking\_multilingual.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/hybrid_ranking_multilingual.md).

---

### 🔗 Quick-Start Downloads (60 sec)

| Tool                       | Link                                                                                                                                       | 3-Step Setup                                                                             |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------- |
| **WFGY 1.0 PDF**           | [Engine Paper](https://github.com/onestardao/WFGY/blob/main/I_am_not_lizardman/WFGY_All_Principles_Return_to_One_v1.0_PSBigBig_Public.pdf) | 1️⃣ Download · 2️⃣ Upload to your LLM · 3️⃣ Ask “Answer using WFGY + \<your question>”   |
| **TXT OS (plain-text OS)** | [TXTOS.txt](https://github.com/onestardao/WFGY/blob/main/OS/TXTOS.txt)                                                                     | 1️⃣ Download · 2️⃣ Paste into any LLM chat · 3️⃣ Type “hello world” — OS boots instantly |

---

### 🧭 Explore More

| Module                   | Description                                                                  | Link                                                                                               |
| ------------------------ | ---------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| WFGY Core                | WFGY 2.0 engine is live: full symbolic reasoning architecture and math stack | [View →](https://github.com/onestardao/WFGY/tree/main/core/README.md)                              |
| Problem Map 1.0          | Initial 16-mode diagnostic and symbolic fix framework                        | [View →](https://github.com/onestardao/WFGY/tree/main/ProblemMap/README.md)                        |
| Problem Map 2.0          | RAG-focused failure tree, modular fixes, and pipelines                       | [View →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md) |
| Semantic Clinic Index    | Expanded failure catalog: prompt injection, memory bugs, logic drift         | [View →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/SemanticClinicIndex.md)           |
| Semantic Blueprint       | Layer-based symbolic reasoning & semantic modulations                        | [View →](https://github.com/onestardao/WFGY/tree/main/SemanticBlueprint/README.md)                 |
| Benchmark vs GPT-5       | Stress test GPT-5 with full WFGY reasoning suite                             | [View →](https://github.com/onestardao/WFGY/tree/main/benchmarks/benchmark-vs-gpt5/README.md)      |
| 🧙‍♂️ Starter Village 🏡 | New here? Lost in symbols? Click here and let the wizard guide you through   | [Start →](https://github.com/onestardao/WFGY/blob/main/StarterVillage/README.md)                   |

---

> 👑 **Early Stargazers: [See the Hall of Fame](https://github.com/onestardao/WFGY/tree/main/stargazers)** <img src="https://img.shields.io/github/stars/onestardao/WFGY?style=social" alt="GitHub stars"> ⭐ [WFGY Engine 2.0](https://github.com/onestardao/WFGY/blob/main/core/README.md) is already unlocked. ⭐ Star the repo to help others discover it and unlock more on the [Unlock Board](https://github.com/onestardao/WFGY/blob/main/STAR_UNLOCKS.md).

<div align="center">

[![WFGY Main](https://img.shields.io/badge/WFGY-Main-red?style=flat-square)](https://github.com/onestardao/WFGY)

[![TXT OS](https://img.shields.io/badge/TXT%20OS-Reasoning%20OS-orange?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS)

[![Blah](https://img.shields.io/badge/Blah-Semantic%20Embed-yellow?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlahBlahBlah)

[![Blot](https://img.shields.io/badge/Blot-Persona%20Core-green?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlotBlotBlot)

[![Bloc](https://img.shields.io/badge/Bloc-Reasoning%20Compiler-blue?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlocBlocBloc)

[![Blur](https://img.shields.io/badge/Blur-Text2Image%20Engine-navy?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlurBlurBlur)

[![Blow](https://img.shields.io/badge/Blow-Game%20Logic-purple?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlowBlowBlow)

</div>

