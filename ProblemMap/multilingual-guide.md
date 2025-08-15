# 🌍 Multilingual RAG Guide — CJK, RTL, and Code-Mix Done Right

Build one pipeline that works across languages without wrecking recall or citations.

> **Quick Nav**  
> [Retrieval Playbook](./retrieval-playbook.md) ·
> [Embedding vs Semantic](./embedding-vs-semantic.md) ·
> [Patterns](./patterns/README.md) ·
> [Rerankers](./rerankers.md)

---

## 0) Principles

1. **Detect → Segment → Normalize → Dual-index → Fence citations.**  
2. Keep **original text** for display and **normalized text** for search.  
3. Pick **truly multilingual embeddings** or **per-lang encoders**—don’t mix silently.

---

## 1) Language detection

- Use CLD3/fastText or a simple rule-first fallback (CJK regex, RTL markers).  
- Store `lang` on **chunks** and **queries**.  
- If uncertain, mark `lang="und"` and route to **char-level** retrieval.

```json
{"chunk_id":"c1","lang":"zh","text":"ΔS 衡量語義張力 ..."}
````

---

## 2) Segmentation & normalization

| Language              | Segmenter         | Notes                                                 |
| --------------------- | ----------------- | ----------------------------------------------------- |
| Chinese (zh)          | jieba / pkuseg    | Also store **OpenCC** simplified/Traditional variants |
| Japanese (ja)         | MeCab             | Preserve readings for search if useful                |
| Korean (ko)           | MeCab-ko / khaiii | Keep compound nouns intact when possible              |
| Thai (th)             | PyThaiNLP         | Sentence boundaries matter for chunking               |
| Arabic/Hebrew (ar/he) | ICU               | Handle diacritics/RTL shaping                         |
| Code-mix              | ICU + heuristic   | Fall back to character n-grams if needed              |

Normalization checklist:

* Unify punctuation (full-width/half-width).
* Unicode NFC.
* Lowercase where appropriate (not for proper nouns in citations).
* Keep both **`text_orig`** and **`text_norm`**.

---

## 3) Embeddings & indexing

**Recommended multilingual encoders**

* `bge-m3` (multilingual, strong cross-lingual)
* `LaBSE` (older but solid cross-lingual)

**Patterns**

* If queries in lang A frequently need answers in lang B → *cross-lingual retrieval*.
* For noisy OCR in CJK, consider **char-level dense + BM25** hybrid.

**Indexing**

* Add `lang` and `script` fields; route BM25 analyzers per language.
* For FAISS dense index: **single multilingual vector space** is easiest; if per-lang spaces, keep a **router**.

---

## 4) Retrieval & reranking

* First stage: **hybrid** (dense + BM25) with **RRF**.
* If candidates include multiple languages, re-rank with **cross-encoder multilingual** models (e.g., `bge-reranker-base` works well).
* Never drop minority language candidates too early—keep `k_in ≥ 100` when cross-lingual.

---

## 5) Prompting & citations (SCU-safe)

* Show citations with **language labels** and **line spans**.
* Forbid the LLM from translating citations; allow translations only in the **explanation**.
* If answer language ≠ citation language, state: “Cited in {lang}, answer in {lang}.”

---

## 6) Evaluation

* Build a multilingual **gold set**:

  * Include cross-lingual Q→A pairs (e.g., query in English, answer/citation in zh).
  * Track **recall\@50**, **nDCG\@10**, and **ΔS** per language.
* Acceptance: ΔS ≤ 0.45 for top-ctx in each language; stable λ across 3 paraphrases per language.

---

## 7) Common multilingual pitfalls → fixes

| Pitfall               | Why it happens                | Fix                                                |
| --------------------- | ----------------------------- | -------------------------------------------------- |
| Hybrid fails on CJK   | Analyzer/tokenizer mismatch   | Use ICU analyzers; char-level BM25                 |
| S/T Chinese mismatch  | Source vs query script differ | Store both via **OpenCC**; index two variants      |
| Citations translated  | Prompt schema unlocked        | Fence citations; explain can translate             |
| Cross-lang recall low | Monolingual embeddings        | Use `bge-m3`/LaBSE; or translate query then search |
| Arabic/Hebrew garbled | RTL shaping                   | ICU normalization; verify rendering layer          |

---

## 8) Minimal example (Python, FAISS + BM25 + bge-m3)

```python
# pip install sentence-transformers rank_bm25 faiss-cpu opencc-python-reimplemented
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi
import numpy as np, faiss, opencc

enc = SentenceTransformer("BAAI/bge-m3")
def norm(s, lang):
    if lang in ("zh-hant","zh-hans","zh"):
        return opencc.OpenCC('t2s.json').convert(s)
    return s

chunks = [{"text":"ΔS 衡量語義張力", "lang":"zh"}, {"text":"Delta-S measures semantic stress", "lang":"en"}]
X = enc.encode([norm(c["text"], c["lang"]) for c in chunks], normalize_embeddings=True)
index = faiss.IndexFlatIP(X.shape[1]); index.add(X.astype(np.float32))
bm25 = BM25Okapi([c["text"].split() for c in chunks])

def search(q, lang="en"):
    qv = enc.encode([norm(q, lang)], normalize_embeddings=True).astype(np.float32)
    _, I = index.search(qv, 50); dense_rank=[(int(i), r+1) for r,i in enumerate(I[0])]
    sparse_rank=[(i, r+1) for r,i in enumerate(bm25.get_top_n(q.split(), list(range(len(chunks))), 50))]
    # RRF fuse
```

(Use a proper RRF from the Retrieval Playbook.)

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
