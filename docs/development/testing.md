# ParsiKit Testing Guide

**Target Version:** 3.3.1  
**Test Runner:** `unittest` (Standard Library) / `pytest` Compatible  

---

## 1. Test Suite Architecture

The test suite is organized into distinct categories under the `tests/` directory:

```text
tests/
├── unit/            # Isolated tests for individual functions and classes
├── integration/     # End-to-end workflows connecting multiple modules
├── regression/      # Verified tests for previously reported bug fixes
├── security/        # Privacy, masking, sensitive data, and boundary tests
├── fixtures/        # Shared synthetic, non-sensitive fixtures
├── conftest.py      # Shared pytest configuration and state reset
└── __init__.py
```

---

## 2. Test Execution Commands

### Run all tests with standard library unittest:
```bash
python3 -m unittest discover -s tests -v
```

### Run specific test suites:
```bash
python3 -m unittest discover -s tests/unit -v
python3 -m unittest discover -s tests/integration -v
python3 -m unittest discover -s tests/regression -v
python3 -m unittest discover -s tests/security -v
```

### Run baseline test entrypoint:
```bash
python3 test.py
```

---

## 3. Test Standards & Guidelines

1. **Deterministic:** Tests must not depend on network access, current system clock (use explicit `reference` arguments in date humanization), or specific OS environments.
2. **Synthetic Data Only:** Real personal identifiers (کد ملی), bank cards, or phone numbers must NEVER appear in test fixtures or assertions.
3. **Descriptive Names:** Test methods should clearly describe what property is being evaluated.
4. **Regression Guarantee:** When fixing a defect, add a corresponding test method in `tests/regression/test_v331_regressions.py`.
