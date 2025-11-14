import sys
from pathlib import Path

# Ensure src directory is on sys.path for imports during tests
SRC = Path(__file__).resolve().parents[1] / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
