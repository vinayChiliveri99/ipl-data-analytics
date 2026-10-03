# Python Project Setup Notes

Personal reference notes from setting up my first Python project, with Node.js comparisons.

---

## 1. Creating the project

Run inside the project folder (this does **not** create a new folder; everything goes in the current one):

```bash
python3 -m venv .venv                      # create the virtual environment
source .venv/bin/activate                  # activate it
python -m pip install --upgrade pip        # update pip inside the venv
```

- `python3 -m venv .venv` uses Python's built-in `venv` module. The `-m` flag means "run this module as a script."
- `.venv` is the conventional folder name. VS Code detects it automatically.

> Some tools (e.g. `uv init <name>`) **do** create a new folder when you pass a name. The manual `venv` approach never does.

---

## 2. Why a virtual environment?

| Node.js | Python |
|---|---|
| `npm install` puts packages in the project's `node_modules/` by default | `pip install` puts packages in **one global location** shared by every project |
| Each project is separate automatically | You must create a virtual environment to keep projects separate |

Without a venv, if Project A needs pandas 1.x and Project B needs pandas 2.x, they conflict.

A virtual environment (`.venv/`) is a private folder with:
- its own Python interpreter: `.venv/bin/python`
- its own pip: `.venv/bin/pip`
- its own packages folder: `.venv/lib/python3.12/site-packages/` (the `node_modules` equivalent)

---

## 3. Activating (the new habit)

Node has no equivalent. In Python you activate the venv in **every new terminal session**:

```bash
source .venv/bin/activate     # prompt shows (.venv)
python main.py                # "python" and "pip" now mean the venv's copies
deactivate                    # leave the venv
```

Activating just puts `.venv/bin` at the front of your `PATH`. If you forget, `pip install` puts packages into **global** Python, not your project.

Check which Python you're using:

```bash
which python      # should print .../ipl-project/.venv/bin/python
```

**VS Code:** `Cmd+Shift+P` → "Python: Select Interpreter" → choose `./.venv/bin/python`. New terminals will then activate the venv automatically.

---

## 4. Project files

```
ipl-project/
├── .venv/              ← virtual env (like node_modules + its own Python). NOT committed.
├── .gitignore          ← ignores .venv/, __pycache__/, .env, etc.
├── requirements.txt    ← dependency list (like package.json "dependencies")
└── main.py             ← entry point (like index.js)
```

### The `if __name__ == "__main__":` line in main.py

```python
if __name__ == "__main__":
    main()
```

This means "only run `main()` when this file is executed directly (`python main.py`), not when another file imports it." Node has a similar pattern: `if (require.main === module)`.

---

## 5. Dependencies: pip does NOT update requirements.txt for you

**This is the biggest difference from npm.**

| npm | pip |
|---|---|
| `npm install pandas` installs **and** adds it to `package.json` | `pip install pandas` **only** installs. `requirements.txt` is unchanged. |

### What goes wrong if you forget

1. You run `pip install pandas` and use it in your code.
2. You never update `requirements.txt`.
3. Everything works on **your** machine, because pandas is in your `.venv`.
4. Someone else clones the repo and runs `pip install -r requirements.txt`. pandas isn't listed, so it isn't installed.
5. Their run crashes:
   ```
   ModuleNotFoundError: No module named 'pandas'
   ```

Nothing warns you. Avoiding this is up to you.

### Option A: `pip freeze` (snapshot everything)

```bash
pip install pandas
pip freeze > requirements.txt
```

`pip freeze` lists **every** package in the venv with exact versions:

```
numpy==2.1.2
pandas==2.2.3
python-dateutil==2.9.0.post0
pytz==2024.2
six==1.16.0
tzdata==2024.2
```

- ✅ Fully reproducible (similar to `package-lock.json`)
- ❌ Mixes packages you chose (pandas) with their sub-dependencies (numpy, pytz, …), so you can't tell which ones you actually picked
- ⚠️ `>` **overwrites** the file, so any comments in it are lost
- ⚠️ If the venv is **not activated**, it dumps your global packages instead

### Option B: write top-level dependencies by hand

Edit `requirements.txt` yourself and list only what your code imports directly:

```
pandas==2.2.3
```

- ✅ Clean and readable (like `package.json`)
- ✅ pip installs sub-dependencies (numpy, etc.) automatically
- ❌ Easy to forget, and sub-dependency versions can change between installs

### Check for missing dependencies before shipping

Test the install from scratch in a throwaway venv:

```bash
deactivate
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py          # if something's missing, it fails here, before teammates hit it
```

### The modern fix

Newer tools (`uv`, `poetry`) use a `pyproject.toml` file and have an `add` command, e.g. `uv add pandas`. This installs the package **and** records it, just like `npm install`, and keeps a lock file like `package-lock.json`. Worth using in future projects.

---

## 6. Quick command cheat sheet

| Task | Node.js | Python (venv + pip) |
|---|---|---|
| Create project env | `npm init` | `python3 -m venv .venv` |
| Enter env | (not needed) | `source .venv/bin/activate` |
| Install a package | `npm install pandas` | `pip install pandas` |
| Record dependencies | automatic | `pip freeze > requirements.txt` or edit by hand |
| Install all deps | `npm install` | `pip install -r requirements.txt` |
| List installed | `npm ls` | `pip list` / `pip freeze` |
| Uninstall | `npm uninstall x` | `pip uninstall x` (then update requirements.txt) |
| Run | `node index.js` | `python main.py` |
| Ignore in git | `node_modules/` | `.venv/` |

---

## 7. Coding standards checklist (learned from my first code review)

### Naming (PEP 8): the biggest JS habit to drop

| Thing | Python style | ❌ JS habit |
|---|---|---|
| functions, variables, params | `runs_by_team`, `top_n` | `runsByTeam`, `topN` |
| constants (module level) | `RCB = "Royal Challengers Bangalore"` | string repeated inline |
| classes | `PascalCase` | (same as JS) |

- Don't give two functions names that differ only by capitalization (`findTopBatsman` vs `findTopBatsMan`).
- Names should say what the function returns. `runs_by_batsman` returns all batsmen, so don't call it "find top".

### File structure

```python
"""Module docstring: what this file is for."""   # 1. docstring, not # comments

import csv                                        # 2. imports: standard library
from pathlib import Path

import matplotlib.pyplot as plt                   #    then third-party

from src.plotting import plot_horizontal_bar      #    then your own modules

RCB = "Royal Challengers Bangalore"               # 3. constants


def ...                                           # 4. functions (2 blank lines between)
```

- **No work at import time.** Loading files or running code at module level happens on `import`. Put it inside `main()`.
- **All imports at the top**, never in the middle of the file.

### File paths

```python
# ❌ relative to wherever the terminal is, so it breaks from another folder
open("./data/matches.csv")

# ✅ relative to this source file, so it works from anywhere
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
```

### Counting and sorting with a plain dict

```python
totals = {}
for ball in deliveries:
    name = ball["batsman"]
    if name not in totals:
        totals[name] = 0
    totals[name] += int(ball["batsman_runs"])

sorted_totals = sorted(totals.items(), key=lambda item: item[1], reverse=True)
top_10 = sorted_totals[:10]
```

- `totals.items()` gives `(key, value)` pairs, like `Object.entries()` in JS.
- `key=lambda item: item[1]` sorts by the value. `lambda` is Python's short arrow function: `item => item[1]`.
- `[:10]` slices the first 10, like `.slice(0, 10)`.
- `csv.DictReader` reads a CSV straight into dicts. There's no need to convert to JSON first.
- Later: `collections.Counter` can replace this pattern, once the plain version feels natural.

### DRY (Don't Repeat Yourself)

If two files share 40 identical lines (e.g. chart styling), extract a helper (`src/plotting.py`).
That way one fix covers every chart, and you can't forget a step like `plt.show()` in one copy.

### matplotlib: use the object-oriented API

```python
# ❌ implicit "current figure" state
plt.figure()
plt.barh(...)
plt.gca().spines["top"].set_visible(False)

# ✅ explicit figure and axes
fig, ax = plt.subplots(figsize=(14, 9))
ax.barh(...)
ax.spines["top"].set_visible(False)
```

### Type hints

```python
def top_batsmen(deliveries: list[dict[str, str]], team: str, top_n: int) -> list[tuple[str, int]]:
```

Optional, but standard in professional code. VS Code uses them for autocomplete and error hints.

### Comments

- Explain **why**, not **what**. `reverse=True  # sort in descending order` just repeats the code.
- ✅ Good: `# barh draws the first item at the bottom, so reverse to put it on top`

### Formatting basics

- 4 spaces for indentation (never tabs).
- 2 blank lines between top-level functions, 1 blank line inside functions to separate steps.
- Keep lines under about 88 characters. Wrap long calls inside `( )` across several lines.
- No spaces around `=` in keyword arguments: `top_n=10`, not `top_n = 10`.
- No trailing spaces, and end every file with a newline.

### Refactoring safely

Before restructuring code, save its current output. After refactoring, check the new output matches exactly.
A refactor should change how the code looks, not what it produces.
