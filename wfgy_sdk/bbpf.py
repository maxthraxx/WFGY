import numpy as np

def perturb_state(x, epsilon=0.1, num_paths=3):
    """Return list of perturbed states"""
    return [x + np.random.normal(0, epsilon, size=x.shape) for _ in range(num_paths)]

def run_demo():
    x = np.array([1.0, 2.0, 3.0])
    paths = perturb_state(x)
    for i, p in enumerate(paths):
        print(f"Path {i+1}: {p}")
