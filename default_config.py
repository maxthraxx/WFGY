# default_config.py

# WFGY default parameters for stable semantic enhancement
DEFAULT_CONFIG = {
    "bbmc_alpha": 0.88,               # Controls strength of semantic residue alignment (higher = more correction)
    "bbpf_noise_level": 0.03,         # Small noise level for creative reasoning without chaos
    "bbcr_reset_value": 0.05,         # Controls system "reset baseline" – low = more persistent state
    "bbam_modulation_scale": 0.92     # Balances modulation effect – 1.0 = strong modulation
}

# Humorous prompt for basic testing
prompt_humorous = "Why don't AIs like to take showers?"
