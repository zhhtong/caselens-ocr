from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]

def load_yaml(name: str):
    path = ROOT / "config" / name
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

