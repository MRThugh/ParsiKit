# Contributing to ParsiKit

**Project Owner:** Ali Kamrani (MRThugh)  
**License:** MIT License  
**Target Version:** 3.3.1  

We welcome contributions from developers interested in improving Persian and regional computational linguistics, typography, and data infrastructure in Python!

---

## 1. Development Principles

1. **Zero Runtime Dependencies:** ParsiKit must always remain pure Python without mandatory external runtime dependencies.
2. **Conservative & Evidence-Driven:** Every bug fix must include a reproducing regression test in `tests/`.
3. **Persian & Regional Typography Excellence:** Respect standard zero-width non-joiners (نیم‌فاصله), standard Persian characters (ی instead of ي, ک instead of ك), and correct numeral handling across Iranian Persian, Afghan Dari, and Tajikistan Tajik.
4. **Security & Privacy:** Never commit real national codes, phone numbers, credentials, or bank card numbers. Use fictitious fixtures only.
5. **Four-Language Documentation Integrity:** Maintain cross-language consistency across all four supported documentation editions (`docs/en/`, `docs/fa/`, `docs/fa-AF/`, `docs/tg/`) and their respective root README files (`README.md`, `README.fa.md`, `README.fa-AF.md`, `README.tg.md`).

---

## 2. Setting Up Local Environment

Clone the repository and install development dependencies in editable mode:

```bash
git clone https://github.com/MRThugh/ParsiKit.git
cd ParsiKit
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e .
```

---

## 3. Running the Test Suite

Run the full automated test suite:

```bash
python3 -m unittest discover -s tests -v
# or using pytest
pytest -v tests
```

Or run the root regression test suite:

```bash
python3 test.py
```

Run the documentation validation check:

```bash
python3 scripts/validate_docs.py
```

---

## 4. Submitting a Pull Request

1. Create a feature branch: `git checkout -b fix/your-bug-fix`
2. Write unit and regression tests in `tests/`.
3. Verify that all existing and new tests pass: `python3 -m unittest discover -s tests`.
4. Update documentation in all four language editions (`docs/fa/`, `docs/fa-AF/`, `docs/tg/`, `docs/en/`) and root README files if public behavior or APIs are affected.
5. Verify internal Markdown links and documentation coverage: `python3 scripts/validate_docs.py`.
6. Record changes in `CHANGELOG.md`.
7. Submit a clean Pull Request with a clear rationale.
