from pathlib import Path
import requests

BASE = "https://huggingface.co/datasets/mabilton/fremtpl2/resolve/main"
FILES = ["freMTPL2freq.csv", "freMTPL2sev.csv"]
RAW = Path("data/raw")

def main():
    RAW.mkdir(parents=True, exist_ok=True)
    for name in FILES:
        dest = RAW / name
        if dest.exists():
            print(f"{name} already exists, skipping")
            continue
        print(f"Downloading {name}...")
        r = requests.get(f"{BASE}/{name}", timeout=120)
        r.raise_for_status()
        dest.write_bytes(r.content)
        print(f"Saved {dest} ({dest.stat().st_size / 1e6:.1f} MB)")

if __name__ == "__main__":
    main()