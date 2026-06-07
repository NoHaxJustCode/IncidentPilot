from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

from app.eval import run_eval

if __name__ == "__main__":
    print(run_eval().model_dump_json(indent=2))
