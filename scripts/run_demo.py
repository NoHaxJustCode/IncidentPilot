from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

from app.agent import investigate

TICKET = "Checkout latency increased for premium users after deploy 4921. p95 went from 240ms to 1800ms around 14:05 UTC."

if __name__ == "__main__":
    report = investigate(TICKET)
    print(report.summary)
