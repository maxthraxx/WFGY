import numpy as np

def bbpf_progression(x: np.ndarray, epsilon: float = 0.1, num_paths: int = 3,
                     P: list = None) -> list:
    """
    Perform BBPF multi-path semantic progression via perturbation and path weighting.

    Args:
        x (np.ndarray): Current semantic state
        epsilon (float): Standard deviation for random perturbation
        num_paths (int): Number of progression paths to generate
        P (list of float, optional): Weight for each path. If None, uniform weights are used.

    Returns:
        list of np.ndarray: List of progressed semantic states
    """
    if P is None:
        P = [1.0 / num_paths] * num_paths

    paths = []
    for i in range(num_paths):
        perturbation = np.random.normal(0, epsilon, size=x.shape)
        new_state = x + P[i] * perturbation
        paths.append(new_state)

    return paths

def run_demo():
    x = np.array([1.0, 2.0, 3.0])
    paths = bbpf_progression(x, epsilon=0.1, num_paths=3)
    for i, p in enumerate(paths):
        print(f"Path {i+1}: {p}")

if __name__ == "__main__":
    run_demo()
