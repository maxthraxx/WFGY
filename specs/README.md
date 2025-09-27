
# WFGY – Public API Specs & ONNX Graphs
*Version 1.0 · last updated 2025-06-12*

WFGY is open by design.  
To guarantee that each module can be inspected, audited, or re-implemented,
we publish (1) a concise API spec and (2) a lightweight ONNX graph for every
core component.  
Download the `.onnx` files and open them in **[Netron](https://netron.app)**
or any ONNX viewer to see the exact computation graph—no black box, no
hidden layers.

| Module | API spec | ONNX graph |
|--------|----------|-----------|
| **BBMC**<br>_Semantic Residue_ | [`bbmc_api.md`](bbmc_api.md) | [`onnx/bbmc.onnx`](onnx/bbmc.onnx) |
| **BBPF**<br>_Progression Flow_ | [`bbpf_api.md`](bbpf_api.md) | [`onnx/bbpf.onnx`](onnx/bbpf.onnx) |
| **BBCR**<br>_Collapse–Rebirth_ | [`bbcr_api.md`](bbcr_api.md) | [`onnx/bbcr.onnx`](onnx/bbcr.onnx) |
| **BBAM**<br>_Attention Modulator_ | [`bbam_api.md`](bbam_api.md) | [`onnx/bbam.onnx`](onnx/bbam.onnx) |

---

## Re-exporting the graphs

All four graphs are intentionally **tiny** (~20 KB each) so they build in
seconds and reveal the tensor flow without shipping proprietary weights.

```bash
# in repo root
python export_onnx.py
````

This script recreates the folder structure:

```
specs/
├── onnx/
│   ├── bbam.onnx
│   ├── bbcr.onnx
│   ├── bbmc.onnx
│   └── bbpf.onnx
└── *.md               # human-readable API specs
```

Feel free to replace these dummy graphs with full-precision weights
if you need exact numerical reproduction.

---

## License & Citation

The API descriptions and ONNX graphs are released under the MIT license.
If you use WFGY in research, please cite the Zenodo release:

```
PSBigBig, “WFGY 1.0: A Self-Healing Variance Gate for LLMs,”
```

> Any issue / PR is welcome—open science thrives on transparency.

```

---

### Will Colab runs change after adding this folder?

No. `specs/` is pure documentation.  
All examples (`example_01`–`08`), tests, and the SDK itself remain identical,
so you can keep running the original Colab notebook without any modification.
```

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


