def check_collapse(B, Bc=1.2):
    """If residue exceeds threshold, trigger reset"""
    return B > Bc

def reset_state(state, delta_B):
    print("Reset triggered. Reinitializing state.")
    return state * 0.0 + delta_B

def run_demo():
    state = 3.0
    B = 1.5
    if check_collapse(B):
        state = reset_state(state, delta_B=0.1)
    print(f"Post-reset state: {state}")
