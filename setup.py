"""
╭──────────────────────────────────────────────────────────╮
│  WFGY SDK · Self-Healing Variance Gate for Any LLM       │
│----------------------------------------------------------│
│ 💌  Contact : hello@onestardao.com  /  TG @PSBigBig       │
│ 🌐  Docs    : https://onestardao.com/papers               │
│ 🐙  GitHub  : https://github.com/onestardao/WFGY          │
│                                                          │
│ ★ Star WFGY 1.0 → Unlock 2.0                             │
│   10k ⭐ by **Aug 1st** = next-gen AI alchemy             │
│   Your click = our quantum leap                          │
│                                                          │
│ 🔍  Official PDF of WFGY 1.0 (Zenodo DOI):               │
│     https://doi.org/10.5281/zenodo.15630970              │
│     (Hosted on Zenodo – trusted international archive)   │
│                                                          │
│ 🧠  Hidden folder inside repo: /I_am_not_lizardman        │
│     (X secret papers, wild prompts, and Einstein drama) │
│                                                          │
│ ⚠  GPT-2 demo is just the appetizer. With bigger LLMs,   │
│    WFGY activates variance-drop lasers and KL fireworks. │
│                                                          │
│ 🎮  Bonus: Honest Hero RPG Channel →                     │
│     https://www.youtube.com/@OneStarDao                  │
╰──────────────────────────────────────────────────────────╯
"""
from setuptools import setup, find_packages

setup(
    name="wfgy_sdk",
    version="1.0.1",
    description="WFGY 1.0 • Self-Healing LLM Framework SDK",
    author="PSBigBig",
    author_email="hello@onestardao.com",
    url="https://github.com/onestardao/WFGY",
    packages=find_packages(include=["wfgy_sdk", "wfgy_sdk.*"]),
    install_requires=[
        "numpy>=1.24",
        "PyYAML>=6.0",
        # ↓ This is an example/demo script, can be deleted as needed
        "transformers>=4.30.0",
        "torch>=2.0.0",
        "sentence_transformers>=2.2.2",
        "datasets>=2.12.0",
        "evaluate>=0.4.0",
        "accelerate>=0.18.0",
        "tensorboard",
        "tqdm",
        "scipy",
        "click",
        "requests",
        "matplotlib"
        "tabulate",
    ],
    entry_points={
        "console_scripts": [
            "wfgy=wfgy_sdk.cli:main",
        ]
    },
    python_requires=">=3.10",
)
