# Installation Guide

ParsiKit requires Python **3.10** or higher. It has no external dependencies.

---

## 1. Install via PyPI

```bash
pip install parsikit
```

To upgrade to the latest stable release:
```bash
pip install --upgrade parsikit
```

---

## 2. Install in Virtual Environments

### Using `venv`
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install parsikit
```

### Using Poetry
```bash
poetry add parsikit
```

### Using uv
```bash
uv pip install parsikit
```

---

## 3. Install from Source

```bash
git clone https://github.com/MRThugh/ParsiKit.git
cd ParsiKit
pip install -e .
```

---

## 4. Verification

Run the following command to verify installation:

```bash
python3 -c "import parsikit; print('ParsiKit version:', parsikit.__version__)"
```
