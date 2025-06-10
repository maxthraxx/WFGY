import numpy as np

def compute_residue(I, G, m=0.8, c=1.0):
    """Compute semantic residue B = I - G + mc^2"""
    B = I - G + m * c ** 2
    return np.linalg.norm(B)

def run_demo():
    I = np.array([1.2, 0.7, 0.5])
    G = np.array([1.0, 0.6, 0.4])
    residue = compute_residue(I, G)
    print(f"BBMC residue: {residue}")
