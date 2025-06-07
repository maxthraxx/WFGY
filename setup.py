# setup.py

from setuptools import setup, find_packages

setup(
    name="wfgy_sdk",
    version="1.0.0",
    description="WFGY 1.0 Self-Healing LLM Framework SDK",
    author="PSBigBig",
    author_email="hello@onestardao.com",
    url="https://github.com/onestardao/WFGY",
    packages=find_packages(include=["wfgy_sdk", "wfgy_sdk.*"]),
    install_requires=[
        "PyYAML>=6.0",
        "transformers>=4.30.0",
        "torch>=2.0.0",
        "datasets>=2.12.0",
        "evaluate>=0.4.0",
        "accelerate>=0.18.0",
        "tensorboard",
        "tqdm",
        "scipy",
        "click",
        "requests"
    ],
    entry_points={
        "console_scripts": [
            "wfgy=wfgy_sdk.cli:main"
        ]
    }
)
