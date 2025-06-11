import numpy as np

def compute_residue(I: np.ndarray, G: np.ndarray, m: float = 0.8, c: float = 1.0) -> float:
    """
    Compute semantic residue based on BBMC formula: B = I - G + mc^2

    Args:
        I (np.ndarray): Input semantic vector
        G (np.ndarray): Ground-truth semantic vector
        m (float): Matching coefficient
        c (float): Context factor

    Returns:
        float: L2 norm of semantic residue vector
    """
    B = I - G + m * c ** 2
    return np.linalg.norm(B)

def run_demo():
    I = np.array([1.2, 0.7, 0.5])
    G = np.array([1.0, 0.6, 0.4])
    residue = compute_residue(I, G)
    print(f"BBMC residue: {residue:.4f}")

if __name__ == "__main__":
    run_demo()
