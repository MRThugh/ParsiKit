# ParsiKit Release Process

**Author & Maintainer:** Ali Kamrani (MRThugh)  
**Target Version:** 3.3.1  

---

## 1. Release Checklist

Before tagging or distributing a new patch release:

1. **Verify Baseline Tests:**
   Run `python3 -m unittest discover -s tests -v` and `python3 test.py`. All tests must pass with 0 failures and 0 errors.
2. **Version Synchronization:**
   Ensure the target version (e.g. `3.3.1`) matches across:
   - `parsikit/__init__.py` (`__version__`)
   - `pyproject.toml` (`version`)
   - `setup.py` (`version`)
   - `CHANGELOG.md`
3. **Distribution Construction:**
   Build both source distribution (`sdist`) and binary wheel (`bdist_wheel`):
   ```bash
   python3 setup.py sdist bdist_wheel
   ```
4. **Inspect Artifact Contents:**
   Inspect the wheel contents using `unzip -l dist/*.whl` to confirm:
   - Only `parsikit/` is packaged.
   - `tests/` and scratch files are strictly excluded.
   - `LICENSE` and metadata are included.
5. **Clean Installation Test:**
   Install the built wheel in a clean virtual environment and verify import:
   ```bash
   pip install dist/parsikit-*.whl
   python3 -c "import parsikit; print(parsikit.__version__)"
   ```
6. **Documentation Synchronization:**
   Verify that Persian (`docs/fa/`) and English (`docs/en/`) documentation and examples are synchronized with current behavior.
7. **Authorization & Publishing:**
   Never publish or tag without explicit maintainer authorization.
