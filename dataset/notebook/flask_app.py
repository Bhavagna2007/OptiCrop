import subprocess
import sys
from pathlib import Path

VENV_PYTHON = Path(r"C:\Users\NITHEESH\Desktop\OptiCrop\.venv\Scripts\python.exe")
THIS_FILE = Path(__file__).resolve()


def main() -> None:
    if VENV_PYTHON.exists() and str(sys.executable).lower() != str(VENV_PYTHON).lower():
        subprocess.run([str(VENV_PYTHON), str(THIS_FILE)], check=False)
        return

    from templates.flask_app import app

    app.run(debug=True)


if __name__ == "__main__":
    main()
