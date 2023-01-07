import pickle
def load_embeddings(dir):
    with open(dir, "rb") as f:
        embeddings_dict = pickle.load(f)
    return embeddings_dict