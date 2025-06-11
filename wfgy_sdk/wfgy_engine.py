import numpy as np
from bbmc import compute_residue
from bbpf import perturb_state
from bbcr import check_collapse, reset_state
from bbam import modulate_attention

class WFGYEngine:
    def __init__(self, m=0.8, c=1.0, epsilon=0.1, num_paths=3, Bc=1.2, delta_B=0.1, gamma=0.5):
        self.m = m
        self.c = c
        self.epsilon = epsilon
        self.num_paths = num_paths
        self.Bc = Bc
        self.delta_B = delta_B
        self.gamma = gamma

    def run(self, I, G, enable_bbcr=True, enable_bbam=True, return_all=False):
        residue = compute_residue(I, G, self.m, self.c)
        paths = perturb_state(I, epsilon=self.epsilon, num_paths=self.num_paths)

        results = []
        for path in paths:
            state = path.copy()
            collapse_triggered = False

            if enable_bbcr and check_collapse(residue, self.Bc):
                state = reset_state(state, delta_B=self.delta_B)
                collapse_triggered = True

            if enable_bbam:
                state = modulate_attention(state, gamma=self.gamma)

            results.append({
                'state': state,
                'collapsed': collapse_triggered,
                'residue': residue
            })

        if return_all:
            return results
        else:
            return [r['state'] for r in results]

if __name__ == "__main__":
    engine = WFGYEngine()
    I = np.array([1.2, 0.7, 0.5])
    G = np.array([1.0, 0.6, 0.4])
    output = engine.run(I, G, return_all=True)
    for i, r in enumerate(output):
        print(f"Path {i+1}: State={r['state']}, Collapsed={r['collapsed']}, Residue={r['residue']}")
