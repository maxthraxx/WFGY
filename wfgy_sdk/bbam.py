import numpy as np

def modulate_attention(logits, gamma=0.5):
    sigma = np.std(logits)
    return logits * np.exp(-gamma * sigma)

def run_demo():
    logits = np.array([1.2, 0.9, 1.1])
    new_logits = modulate_attention(logits)
    print(f"Original: {logits}\nModulated: {new_logits}")
