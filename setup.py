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
        "numpy<2.0",
        "torch==2.2.2+cpu",
        "transformers==4.41.2",
        "tabulate",
        "matplotlib",
    ],
    entry_points={
        "console_scripts": [
            "wfgy=wfgy_sdk.cli:main",
        ]
    },
)
