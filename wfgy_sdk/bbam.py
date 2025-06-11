import numpy as np

def modulate_attention(logits, gamma=0.5):
    """
    Apply BBAM modulation to logits: a_i * exp(-gamma * sigma(a))

    Args:
        logits (np.ndarray): Original attention logits
        gamma (float): Scaling factor for variance suppression

    Returns:
        np.ndarray: Modulated logits
    """
    sigma = np.std(logits)
    modulated_logits = logits * np.exp(-gamma * sigma)
    return modulated_logits

def run_demo():
    logits = np.array([1.2, 0.9, 1.1])
    new_logits = modulate_attention(logits)
    print(f"Original: {logits}")
    print(f"Modulated: {new_logits}")

if __name__ == "__main__":
    run_demo()
