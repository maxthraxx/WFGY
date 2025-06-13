from setuptools import setup, find_packages

setup(
    name="wfgy_sdk",
    version="0.1.0",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "numpy<2.0",
        "torch==2.2.2+cpu",
        "transformers==4.41.2",
        "tabulate",
        "matplotlib",       # <── NEW: fixes ModuleNotFoundError
    ],
    extras_require={
        "dev": ["pytest", "wheel"],
    },
)
