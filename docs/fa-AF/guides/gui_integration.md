# رهنمود: یکپارچه‌سازی با واسط‌های گرافیکی (GUI) و رسم متن

رسم متن‌های راست‌به‌چپ در برنامه‌های دسکتاپ (Tkinter, PyQt, PySide) یا کتابخانه‌های پروسس تصویر (Pillow, OpenCV) نیازمند آماده‌سازی خاص اتصال حروف است.

---

## ۱. رسم تصویر و متن در Pillow و OpenCV

برای موتورهایی که اتصال خط عربی/فارسی را پشتیبانی نمی‌نمایند، از `reshape_for_graphics` استفاده کنید:

```python
from PIL import Image, ImageDraw, ImageFont
import parsikit

# ایجاد تصویر خالی
image = Image.new("RGB", (600, 200), color=(255, 255, 255))
draw = ImageDraw.Draw(image)

# بازآرایی متن جهت رسم
text = "سامانه‌ی مدیریت اسناد و مدارک"
reshaped = parsikit.reshape_for_graphics(text)

# font = ImageFont.truetype("Vazirmatn-Bold.ttf", 32)
# draw.text((50, 80), reshaped, font=font, fill=(0, 0, 0))
```

---

## ۲. شکستن پاراگراف‌های طولانی (`reshape_paragraph_for_graphics`)

برای جعبه‌های متنی چندسطری:

```python
import parsikit

paragraph = (
    "کتابخانه‌ی پارسی‌کیت مجموعه‌ای از ابزارهای معیارسازی و "
    "اعتبارسنجی داده‌ها برای توسعه‌دهنده‌گان پایتون می‌باشد."
)

wrapped_lines = parsikit.reshape_paragraph_for_graphics(paragraph, max_chars_per_line=30)
for line in wrapped_lines:
    print(line)
```

---

## ۳. مدیریت تایپ زنده در Tkinter و CustomTkinter

اصلاح خودکار ورودی‌های متنی حین تایپ کاربر بدون پرش کرسر:

```python
import tkinter as tk
import parsikit

root = tk.Tk()
root.title("سامانه‌ی تایپ هوشمند")

entry = tk.Entry(root, font=("Vazirmatn", 14), width=35)
entry.pack(padx=20, pady=20)

# اتصال دستیار هوشمند با حفظ موقعیت کرسر و میانبرها
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

## ۴. یکپارچه‌سازی با PyQt و PySide

اتصال به ویجت‌های Qt (`QLineEdit`, `QTextEdit`):

```python
from PyQt6.QtWidgets import QApplication, QLineEdit, QVBoxLayout, QWidget
import parsikit

app = QApplication([])
window = QWidget()
layout = QVBoxLayout()

card_input = QLineEdit()
card_input.setPlaceholderText("شماره کارت بانکی...")
parsikit.bind_persian_input(card_input, input_type="card")

layout.addWidget(card_input)
window.setLayout(layout)
window.show()
app.exec()
```

---

## ۵. آزادسازی و قطع اتصال (`unbind_persian_input`)

جهت قطع ارتباط رویدادها هنگام پاکسازی ویجت:

```python
parsikit.unbind_persian_input(entry)
```
