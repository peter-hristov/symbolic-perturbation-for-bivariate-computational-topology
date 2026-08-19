import os
import pickle


def load_or_compute(name, compute_fn):

    CACHE_DIR = "cache"
    os.makedirs(CACHE_DIR, exist_ok=True)

    path = os.path.join(CACHE_DIR, f"{name}.pkl")

    if os.path.exists(path):
        print(f"Loading {name} from cache...")
        with open(path, "rb") as f:
            return pickle.load(f)

    print(f"Computing {name}...")
    result = compute_fn()

    with open(path, "wb") as f:
        pickle.dump(result, f)

    return result
