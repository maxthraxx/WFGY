# wfgy_sdk/initializer.py

import os, zipfile, requests
from .utils import DATA_DIR

URLS = {
    "data":     "https://zenodo.org/.../wfgy_data.zip",
    "weights":  "https://zenodo.org/.../wfgy_weights.zip",
    "configs":  "https://zenodo.org/.../wfgy_configs.zip"
}

def initialize():
    os.makedirs(DATA_DIR, exist_ok=True)
    for name, url in URLS.items():
        target = os.path.join(DATA_DIR, f"{name}.zip")
        print(f"Downloading {name}...")
        resp = requests.get(url, stream=True)
        with open(target, "wb") as f:
            for c in resp.iter_content(1024):
                f.write(c)
        with zipfile.ZipFile(target, "r") as z:
            z.extractall(DATA_DIR)
        os.remove(target)
    print("Initialization complete.")
