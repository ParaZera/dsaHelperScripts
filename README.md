# update-dsa-sheet

A small CLI helper for **Das Schwarze Auge (DSA)** character sheets exported as HTML from **Helden Software**.

It annotates the talent table with the hero’s current characteristic values, so entries like:

```
Athletik | (GE/KO/KK) | BEx2 | 7
```

become:

```
Athletik | ( GE[14] / KO[16] / KK[15] ) | BEx2 | 7
```

The tool **modifies the input file in-place** and creates a timestamped backup next to it.

## Requirements

- Python 3.11+ (recommended)
- Works best with `uv`, but can also be installed with `pip`

## Install and run with `uv` (recommended)

### Run without installing (from the repo)

```bash
uv run update-dsa-sheet path/to/character_sheet.html
```

### Install into a virtual environment

```bash
uv sync
uv run update-dsa-sheet path/to/character_sheet.html
```

### Alternative module invocation

```bash
uv run python -m update_dsa_sheet path/to/character_sheet.html
```

## Install and run without `uv`

### Using `pip` in a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate

pip install -e .
```

Run:

```bash
update-dsa-sheet path/to/character_sheet.html
```

Or as a module:

```bash
python -m update_dsa_sheet path/to/character_sheet.html
```

## What it does

- Parses the HTML character sheet
- Extracts the hero’s characteristic values (MU/KL/IN/CH/FF/GE/KO/KK)
- Updates talent rows by expanding the characteristic shorthand with the current values
- Writes the updated HTML back to the original file and creates a `*.bak_<timestamp>` backup

## Development

Run tests:

```bash
uv run pytest
```

(Without `uv`):

```bash
pytest
```

## Notes

- Input file is changed in-place; the backup file is created automatically.
- This project is not affiliated with Helden Software.

