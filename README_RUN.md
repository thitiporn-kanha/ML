How to run this workspace (quick)

1) Clone the repo (on another machine):

```bash
git clone https://github.com/thitiporn-kanha/ML.git
cd ML
```

2) Use the helper script to set up a virtual environment and run a project

- Run logistic project:
```bash
./run.sh logistic
```

- Run linear project:
```bash
./run.sh linear
```

- Run both (logistic then linear):
```bash
./run.sh all
```

Notes:
- `run.sh` creates a `.venv` in the repo root and installs dependencies listed in `requirements.txt`.
- `results/` folders are git-ignored so model artifacts and images won't be uploaded.
- If you prefer to manage your own virtualenv, activate it and run the project scripts directly (e.g. `python logistic/main.py`).
