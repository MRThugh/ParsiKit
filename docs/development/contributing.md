# Contributing to ParsiKit

**Project Owner:** Ali Kamrani (MRThugh)  
**License:** MIT License  

We welcome contributions from developers interested in improving Persian computational linguistics, typography, and data infrastructure in Python!

---

## 1. Development Principles

1. **Zero Runtime Dependencies:** ParsiKit must always remain pure Python without mandatory external runtime dependencies.
2. **Conservative & Evidence-Driven:** Every bug fix must include a reproducing regression test.
3. **Persian Typography Excellence:** Respect standard zero-width non-joiners (نیم‌فاصله), standard Persian characters (ی instead of ي, ک instead of ك), and correct numeral handling.
4. **Security & Privacy:** Never commit real national codes, phone numbers, credentials, or bank card numbers. Use fictitious fixtures only.

---

## 2. Setting Up Local Environment

Clone the repository and install development dependencies in editable mode:

```bash
git clone https://github.com/MRThugh/ParsiKit.git
cd ParsiKit
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

---

## 3. Running the Test Suite

Run the full automated test suite:

```bash
python3 -m unittest discover -s tests -v
```

Or run the root test suite:

```bash
python3 test.py
```

---

## 4. Submitting a Pull Request

1. Create a feature branch: `git checkout -b fix/your-bug-fix`
2. Write unit and regression tests in `tests/`.
3. Verify that all existing and new tests pass: `python3 -m unittest discover -s tests`.
4. Update documentation in both `docs/fa/` and `docs/en/` if public behavior is affected.
5. Record changes in `CHANGELOG.md`.
6. Submit a clean Pull Request with a clear rationale.
