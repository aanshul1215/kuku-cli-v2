import sys
from pathlib import Path

# Allow running via `python app/main.py` by ensuring project root is on sys.path.
if __package__ is None or __package__ == '':
    sys.path.append(str(Path(__file__).resolve().parent.parent))

from app import create_app
from app.db import db

app = create_app('development')

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run()
