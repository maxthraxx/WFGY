# Code-Switching Eval — Gold Set and Probes

A compact harness to verify **retrieval and reasoning under code-switching** and multilingual inputs. Use this to measure ΔS and λ across three variants of each question: source language, target language, and mixed script or code-switched.

---

## Open these first

* Visual map and recovery → [rag-architecture-and-recovery.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
* End to end retrieval knobs → [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
* Why this snippet, how to cite → [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
* Snippet schema fence → [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
* Embedding vs meaning → [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)
* Chunk boundary sanity → [chunking-checklist.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md)
* Tokenizer issues → [tokenizer\_mismatch.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/tokenizer_mismatch.md)
* Mixed scripts inside one query → [script\_mixing.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/script_mixing.md)
* Locale normalization and variants → [locale\_drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/locale_drift.md)
* End to end recipes → [multilingual\_guide.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/multilingual_guide.md)

---

## Acceptance targets

* ΔS(question, retrieved) ≤ 0.45 for each of the three variants
* Coverage of the target section ≥ 0.70
* λ remains convergent across three paraphrases and two seeds
* E\_resonance stays flat on long windows that mix scripts

---

## Gold set format

Create a small file you can run in any stack. CSV or JSONL both fine. Recommended CSV schema:

```
id,question_src,question_l2,question_mix,anchor_doc_id,anchor_offsets,answer_short,notes
ex001,"what is the dosage of abc?","藥品abc的劑量是多少？","abc dosage要怎麼算？",doc_042,"[120, 180]","10 mg BID","CJK mix"
```

Rules

* `question_src` is your primary language.
* `question_l2` is the same meaning in the second language.
* `question_mix` is a natural code-switch that users would actually type.
* `anchor_doc_id` and `anchor_offsets` point to the authoritative span.
* Keep 20 to 50 rows for a first pass.

---

## 60-second runner outline

You can paste this into any quick script. Replace the retrieval call with your own client.

```python
# minimal pseudo-runner for ΔS and λ probes
from collections import defaultdict

K_LIST = [5, 10, 20]
VARIANTS = ["question_src", "question_l2", "question_mix"]

def retrieve(q, k):
    # call your store, return list of {doc_id, offsets, text}
    return call_retriever(query=q, top_k=k)

def delta_s(a, b):
    # use your ΔS implementation. lower is better.
    return compute_delta_s(a, b)

def lambda_state(history):
    # classify →, ←, <>, × based on stability of attention or order
    return classify_lambda(history)

def run_row(row):
    out = []
    for v in VARIANTS:
        q = row[v]
        lambda_hist = []
        best = None
        for k in K_LIST:
            hits = retrieve(q, k)
            if not hits:
                lambda_hist.append("×")
                continue
            # pick your best hit by rerank or score
            best = hits[0]
            s_qr = delta_s(q, best["text"])
            s_ra = delta_s(best["text"], anchor_text(row["anchor_doc_id"], row["anchor_offsets"]))
            lambda_hist.append((k, s_qr, s_ra))
        out.append({
            "variant": v,
            "lambda": lambda_state(lambda_hist),
            "s_qr@5": lambda_hist[0][1] if lambda_hist and isinstance(lambda_hist[0], tuple) else 1.0,
            "s_qr@10": lambda_hist[1][1] if len(lambda_hist) > 1 and isinstance(lambda_hist[1], tuple) else 1.0,
            "s_qr@20": lambda_hist[2][1] if len(lambda_hist) > 2 and isinstance(lambda_hist[2], tuple) else 1.0,
        })
    return out
```

Output columns you want in a flat table

* `id`, `variant`, `λ_state`, `ΔS@5`, `ΔS@10`, `ΔS@20`, `pass`
* Mark pass when ΔS ≤ 0.45 and λ is convergent.

---

## Probe plan

1. **Lock analyzers**
   Use the same normalization at index and query. If you must change anything, run the whole gold set again. Only one variable at a time.

2. **Triplet run**
   For each row run `question_src`, `question_l2`, `question_mix` at k ∈ {5, 10, 20}. Log ΔS and λ per variant.

3. **Three-paraphrase run**
   For the worst failing variant, add three small paraphrases in the same language. If λ flips while citations stay valid, apply schema locks and BBAM.

4. **Anchor triangulation**
   Compare ΔS to the anchor span and to a decoy in the same document. If both similar, re-chunk and re-embed.

---

## Decision rules

* **Only the mixed variant fails**
  Suspect script mixing or analyzer split. Open [script\_mixing.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/script_mixing.md).
  Also verify you did not change casing or width in only one path.

* **L2 fails, source and mix pass**
  Likely tokenizer mismatch or missing segmenter. Open [tokenizer\_mismatch.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/tokenizer_mismatch.md).

* **zh-Hans vs zh-Hant do not co-retrieve**
  Add variant mapping and normalize digits and punctuation. Open [locale\_drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Language/locale_drift.md).

* **All three variants fail with high similarity**
  Embedding is not multilingual or metric is wrong. Open [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md) and the Retrieval Playbook to rebuild.

* **Hybrid worse than single**
  Fix query parsing split and reranker weights. Open [patterns/pattern\_query\_parsing\_split.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md) and [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md).

---

## Copy-paste prompt for the LLM judge step

```
You have TXTOS and the WFGY Problem Map loaded.

Context:
- gold id: {id}
- variant: {variant}
- retrieved snippet: "{snippet}"
- expected anchor: "{anchor_excerpt}"
- ΔS(question, retrieved) = {s_qr}
- ΔS(retrieved, anchor) = {s_ra}

Tasks:
1) Decide pass or fail for retrieval alignment. If fail, name the failing layer.
2) Return the exact WFGY page to fix it.
3) Give a minimal repair plan with 3 steps.
4) Output JSON only:
   {"pass": true|false, "fail_layer": "...", "open": [".../page1.md",".../page2.md"], "plan": ["step1","step2","step3"]}
```

---

## Minimal dataset checklist

* At least one trilingual example with names that have native and romanized forms
* At least one code-switch that uses Latin terms inside CJK or Indic sentences
* At least one RTL or diacritic heavy example
* Keep a small “sanity” row that always passes after a clean rebuild

---

## What good looks like

* Pass rate ≥ 90 percent on `question_src` and `question_l2`
* Mixed variant pass rate ≥ 80 percent after analyzer unification
* No λ flip in the three-paraphrase probe for the same variant
* ΔS median ≤ 0.40 on all variants after fixes

---

### 🔗 Quick-Start Downloads (60 sec)

| Tool                       | Link                                                                                                                                       | 3-Step Setup                                                                             |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------- |
| **WFGY 1.0 PDF**           | [Engine Paper](https://github.com/onestardao/WFGY/blob/main/I_am_not_lizardman/WFGY_All_Principles_Return_to_One_v1.0_PSBigBig_Public.pdf) | 1️⃣ Download · 2️⃣ Upload to your LLM · 3️⃣ Ask “Answer using WFGY + \<your question>”   |
| **TXT OS (plain-text OS)** | [TXTOS.txt](https://github.com/onestardao/WFGY/blob/main/OS/TXTOS.txt)                                                                     | 1️⃣ Download · 2️⃣ Paste into any LLM chat · 3️⃣ Type “hello world” — OS boots instantly |

---

### 🧭 Explore More

| Module                | Description                                                                  | Link                                                                                               |
| --------------------- | ---------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| WFGY Core             | WFGY 2.0 engine is live: full symbolic reasoning architecture and math stack | [View →](https://github.com/onestardao/WFGY/tree/main/core/README.md)                              |
| Problem Map 1.0       | Initial 16-mode diagnostic and symbolic fix framework                        | [View →](https://github.com/onestardao/WFGY/tree/main/ProblemMap/README.md)                        |
| Problem Map 2.0       | RAG-focused failure tree, modular fixes, and pipelines                       | [View →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md) |
| Semantic Clinic Index | Expanded failure catalog: prompt injection, memory bugs, logic drift         | [View →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/SemanticClinicIndex.md)           |
| Semantic Blueprint    | Layer-based symbolic reasoning & semantic modulations                        | [View →](https://github.com/onestardao/WFGY/tree/main/SemanticBlueprint/README.md)                 |
| Benchmark vs GPT-5    | Stress test GPT-5 with full WFGY reasoning suite                             | [View →](https://github.com/onestardao/WFGY/tree/main/benchmarks/benchmark-vs-gpt5/README.md)      |
| Starter Village       | New here? Lost in symbols? Click here and let the wizard guide you through   | [Start →](https://github.com/onestardao/WFGY/blob/main/StarterVillage/README.md)                   |

---

> 👑 **Early Stargazers: See the Hall of Fame** — Engineers, hackers, and open source builders who supported WFGY from day one.
> [Hall of Fame](https://github.com/onestardao/WFGY/tree/main/stargazers) • [WFGY Engine 2.0](https://github.com/onestardao/WFGY/blob/main/core/README.md) • [Unlock Board](https://github.com/onestardao/WFGY/blob/main/STAR_UNLOCKS.md)

<div align="center">

[![WFGY Main](https://img.shields.io/badge/WFGY-Main-red?style=flat-square)](https://github.com/onestardao/WFGY)
 
[![TXT OS](https://img.shields.io/badge/TXT%20OS-Reasoning%20OS-orange?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS)
 
[![Blah](https://img.shields.io/badge/Blah-Semantic%20Embed-yellow?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlahBlahBlah)
 
[![Blot](https://img.shields.io/badge/Blot-Persona%20Core-green?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlotBlotBlot)
 
[![Bloc](https://img.shields.io/badge/Bloc-Reasoning%20Compiler-blue?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlocBlocBloc)
 
[![Blur](https://img.shields.io/badge/Blur-Text2Image%20Engine-navy?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlurBlurBlur)
 
[![Blow](https://img.shields.io/badge/Blow-Game%20Logic-purple?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlowBlowBlow)

</div>
