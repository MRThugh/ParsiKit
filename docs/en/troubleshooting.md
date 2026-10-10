# Troubleshooting Guide (English)

Solutions to common issues encountered when using ParsiKit.

---

## 1. SyntaxError in Python 3.10 / 3.11

### Problem
Prior to Python 3.12, backslashes inside f-string expressions were prohibited by the Python grammar (PEP 701). In ParsiKit v3.3.0, a line in `parsikit.dev.debug_text` triggered this syntax error on Python 3.10 and 3.11.

### Solution
This issue is fixed in ParsiKit v3.3.1. Upgrade to v3.3.1:
```bash
pip install --upgrade parsikit
```

---

## 2. Garbled Characters in Console or Terminal

### Problem
Terminal does not default to UTF-8 output encoding, causing Persian characters to render as question marks or mojibake.

### Solution
Ensure UTF-8 encoding is enabled in your environment:

Linux/macOS:
```bash
export PYTHONIOENCODING=utf-8
```

Windows PowerShell:
```powershell
$env:PYTHONIOENCODING="utf-8"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
```

---

## 3. Disconnected or Reversed Persian in Pillow / OpenCV

### Problem
2D rendering engines render Persian characters disconnected from left-to-right because they lack cursive Arabic text shaping and Unicode Bidirectional (BiDi) algorithm support.

### Solution
Use `parsikit.reshape_for_graphics`:
```python
import parsikit

raw = "پردازش تصویر"
reshaped = parsikit.reshape_for_graphics(raw)
# Pass reshaped to draw.text(...)
```

---

## 4. `InvalidNationalCodeError` on 10-Digit Inputs

### Problem
A 10-digit number may still be rejected if:
1. It consists of 10 identical digits (e.g. `1111111111`).
2. Its 10th digit does not match the modulo-11 checksum calculated from the first 9 digits.

### Solution
Ensure test fixtures use mathematically valid check digits (e.g. for prefix `001012345`, the valid check digit is `8`: `0010123458`).
