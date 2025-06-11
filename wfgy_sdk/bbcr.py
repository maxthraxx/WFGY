import numpy as np

def check_collapse(B: float, f_S: float, Bc: float = 1.2, epsilon: float = 0.01) -> bool:
    """
    Determine if collapse should be triggered based on residue and progression metric.

    Args:
        B (float): Current semantic residue
        f_S (float): Current progression metric
        Bc (float): Collapse threshold for semantic residue
        epsilon (float): Minimum acceptable progression value

    Returns:
        bool: True if collapse condition is met
    """
    return B >= Bc or f_S < epsilon

def reset_state(state: np.ndarray, delta_B: float = 0.1, alpha: float = 0.8) -> np.ndarray:
    """
    Perform semantic reset with memory-based adjustment.

    Args:
        state (np.ndarray): Current semantic state
        delta_B (float): Residue memory from previous step
        alpha (float): Shrink factor to reduce instability

    Returns:
        np.ndarray: Reinitialized state
    """
    print(">> BBCR Triggered: Performing semantic reset...")
    return alpha * (state * 0.0 + delta_B)

def compute_lyapunov(B: float, f_S: float, lambd: float = 1.0) -> float:
    """
    Compute Lyapunov stability function.

    Args:
        B (float): Semantic residue
        f_S (float): Progression metric
        lambd (float): Scaling factor for progression term

    Returns:
        float: Lyapunov value
    """
    return B ** 2 + lambd * f_S

def run_demo():
    state = np.array([1.0, 2.0, 3.0])
    B = 1.6
    f_S = 0.005
    V_t = compute_lyapunov(B, f_S)

    if check_collapse(B, f_S):
        state = reset_state(state, delta_B=0.2)
        B_new = 0.8
        f_S_new = 0.02
        V_t1 = compute_lyapunov(B_new, f_S_new)
        print(f"Lyapunov before: {V_t:.4f} → after reset: {V_t1:.4f}")
    else:
        print(">> No collapse. Continuing...")

    print(f"Current state: {state}")

if __name__ == "__main__":
    run_demo()
