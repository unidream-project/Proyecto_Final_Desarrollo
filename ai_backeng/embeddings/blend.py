# ai_backeng/embeddings/blend.py
import numpy as np

def blend_embeddings(old_emb, new_emb, alpha=0.85):
    """
    alpha = cuánto peso tiene el historial
    """
    if old_emb is None:
        return new_emb

    old = np.array(old_emb)
    new = np.array(new_emb)

    blended = alpha * old + (1 - alpha) * new
    blended = blended / np.linalg.norm(blended)

    return blended.tolist()
