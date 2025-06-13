"""
WFGY SDK · setup.py  (only the install_requires list is touched)
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
    python_requires=">=3.10",
    install_requires=[
        "numpy>=1.24",
        "PyYAML>=6.0",
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
        "matplotlib",          # ← NEW (comma kept)
        "tabulate",            # ← NEW (comma kept)
    ],
    entry_points={
        "console_scripts": [
            "wfgy=wfgy_sdk.cli:main",
        ]
    },
)
