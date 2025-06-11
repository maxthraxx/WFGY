# default_config.py
# Centralised defaults for WFGY SDK 1.0
# Author: PSBigBig & Contributors
# License: MIT

DEFAULT_CONFIG = {
    # --- BBMC (Semantic Residue) ---
    "m": 1.0,                  # Matching coefficient
    "c": 1.0,                  # Context factor

    # --- BBPF (Progression) ---
    "noise_scale": 0.02,       # Gaussian noise σ
    "k_paths": 3,              # Number of perturbation paths

    # --- BBCR (Collapse-Rebirth) ---
    "Bc": 1.0,                 # Residue threshold
    "eps": 0.05,               # f_S threshold
    "max_retries": 3,          # Max collapse cycles

    # --- BBAM (Attention Modulation) ---
    "gamma": 0.5,              # Variance gate strength
    "window_size": None        # Use global σ (set int for local)
}

# Humorous prompt for smoke test
PROMPT_HUMOROUS = "Why don't AIs like to take showers?"
