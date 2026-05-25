from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def embed(texts):
    vecs = model.encode(texts)

    # force clean numpy array
    import numpy as np
    vecs = np.asarray(vecs)

    return vecs