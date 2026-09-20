import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STUDY_DIR = ROOT / "data" / "studies"

def list_studies() -> list[str]:
    STUDY_DIR.mkdir(parents=True, exist_ok=True)
    return sorted(p.stem for p in STUDY_DIR.glob("*.json"))

def save_study(name: str, inclusion: str, exclusion: str, version: str = "1.0") -> Path:
    STUDY_DIR.mkdir(parents=True, exist_ok=True)
    safe = "".join(c for c in name.strip() if c.isalnum() or c in "-_ ").strip().replace(" ", "_") or "study"
    path = STUDY_DIR / f"{safe}.json"
    path.write_text(json.dumps({"name": name.strip(), "version": version, "inclusion": inclusion, "exclusion": exclusion}, ensure_ascii=False, indent=2), encoding="utf-8")
    return path

def load_study(name: str) -> dict:
    return json.loads((STUDY_DIR / f"{name}.json").read_text(encoding="utf-8"))

