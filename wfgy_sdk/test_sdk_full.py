# test_sdk_full.py

import numpy as np
from wfgy_sdk import enable

model = {
    "I": np.array([1.2, 0.7, 0.5]),
    "G": np.array([1.0, 0.6, 0.4]),
    "state": np.array([0.1, 0.2, 0.3]),
    "attention_logits": np.array([1.2, 0.9, 1.1])
}

model = enable(model)
