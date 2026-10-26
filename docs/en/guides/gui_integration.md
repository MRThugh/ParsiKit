# Guide: Desktop GUI & Graphics Integration

Rendering Persian text in desktop applications (Tkinter, PyQt, PySide, CustomTkinter) or graphics pipelines (Pillow / PIL, OpenCV, ReportLab) requires specific adaptations for cursive shaping and right-to-left bidirectional (BiDi) display.

---

## 1. Graphics Engines & Image Generation (Pillow / OpenCV)

Without shaping, Persian letters render disconnected from left-to-right. Use `reshape_for_graphics`:

```python
from PIL import Image, ImageDraw, ImageFont
import parsikit

# Create a blank image
image = Image.new("RGB", (600, 200), color=(255, 255, 255))
draw = ImageDraw.Draw(image)

# Reshape Persian text (BiDi and cursive glyph joining)
text = "سامانه هوشمند مدیریت اسناد پارسی"
reshaped = parsikit.reshape_for_graphics(text)

# Render to canvas
# font = ImageFont.truetype("Vazirmatn-Bold.ttf", 32)
# draw.text((50, 80), reshaped, font=font, fill=(0, 0, 0))
```

---

## 2. Multi-Line Paragraphs (`reshape_paragraph_for_graphics`)

For multi-line text boxes in graphics rendering, wrap each line with consistent width:

```python
import parsikit

paragraph = (
    "کتابخانه پارسی‌کیت مجموعه‌ای از ابزارهای استانداردسازی و "
    "اعتبارسنجی داده‌های فارسی برای توسعه‌دهندگان پایتون است."
)

wrapped = parsikit.reshape_paragraph_for_graphics(paragraph, max_chars_per_line=30)
# Returns formatted lines ready for drawing
```

---

## 3. Real-Time Typing Helper in Tkinter & CustomTkinter

Automatically normalize Persian text as the user types without cursor jumps:

```python
import tkinter as tk
import parsikit

root = tk.Tk()
root.title("Smart Persian Input")

entry = tk.Entry(root, font=("Vazirmatn", 14), width=35)
entry.pack(padx=20, pady=20)

# Bind smart Persian typing with cursor preservation, snippets, and shortcuts
parsikit.bind_persian_input(
    entry,
    input_type="text",
    digit_style="persian",
    smart_spacing=True,
    snippets={"ق.ظ": "قبل از ظهر", "ب.ظ": "بعد از ظهر"},
    enable_shortcuts=True
)

root.mainloop()
```

---

## 4. PyQt & PySide Integration

`bind_persian_input` seamlessly integrates with Qt's `QLineEdit`, `QTextEdit`, and `QPlainTextEdit`:

```python
from PyQt6.QtWidgets import QApplication, QLineEdit, QVBoxLayout, QWidget
import parsikit

app = QApplication([])
window = QWidget()
layout = QVBoxLayout()

card_input = QLineEdit()
card_input.setPlaceholderText("Bank card number...")
parsikit.bind_persian_input(card_input, input_type="card")

layout.addWidget(card_input)
window.setLayout(layout)
window.show()
app.exec()
```

---

## 5. Clean Detachment (`unbind_persian_input`)

To disconnect live typing handlers when destroying or reusing widgets:

```python
parsikit.unbind_persian_input(entry)
```
