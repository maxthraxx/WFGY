from . import bbmc, bbpf, bbcr, bbam

def enable(model):
    print("WFGY 1.0 ENABLED ✅")

    I = model["I"]
    G = model["G"]

    B = bbmc.compute_residue(I, G)
    print("BBMC → Residue =", B)

    if bbcr.check_collapse(B):
        model["state"] = bbcr.reset_state(model["state"], delta_B=0.1)
    else:
        paths = bbpf.perturb_state(model["state"])
        model["state"] = paths[0]  

    model["attention"] = bbam.modulate_attention(model["attention_logits"])
    print("WFGY 1.0 complete.\n")
    return model

def disable(model):
    print("WFGY disabled ❌")
    return model
