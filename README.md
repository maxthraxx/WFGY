# README.md

# WFGY 1.0 Reproducibility Package

A Universal Unification Framework for Large-Scale Self-Healing LLMs  
Zenodo DOI: 10.5281/zenodo.15593533  
GitHub: https://github.com/PSBigBig/WFGY

## Quickstart

```bash
git clone https://github.com/onestardao/WFGY.git
cd WFGY

# 1. Verify file integrity
python verify_manifest.py

# 2. Create environment
conda env create -f environment.yml
conda activate wfgy

# 3. Install SDK
pip install -e .

# 4. Run reproduction
bash reproduce.sh
