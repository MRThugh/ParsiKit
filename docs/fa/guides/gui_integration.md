# راهنمای اتصال پارسی‌کیت به رابط‌های گرافیکی (GUI)

پارسی‌کیت ماژول اختصاصی `parsikit.gui` را برای قالب‌بندی همزمان هنگام تایپ در فریم‌ورک‌های رابط کاربری دسکتاپ (مانند Tkinter، CustomTkinter، PyQt و PySide) ارائه می‌دهد.

---

## ۱. استفاده در Tkinter و CustomTkinter

تابع `bind_persian_input` به رویداد رها کردن کلید (`<KeyRelease>`) متصل شده و فرمت ورودی را بلادرنگ اصلاح می‌کند:

```python
import tkinter as tk
import parsikit

root = tk.Tk()
root.title("سامانه فرمت‌بندی هوشمند")

label = tk.Label(root, text="کد ملی:")
label.pack()

entry_national_code = tk.Entry(root)
entry_national_code.pack()

# اتصال فرمت خودکار کد ملی (XXX-XXXXXX-X)
parsikit.bind_persian_input(entry_national_code, input_type="national_code")

card_label = tk.Label(root, text="شماره کارت بانکی:")
card_label.pack()

entry_card = tk.Entry(root)
entry_card.pack()

# اتصال فرمت خودکار ۴ تکه شماره کارت (XXXX-XXXX-XXXX-XXXX)
parsikit.bind_persian_input(entry_card, input_type="card_number")

root.mainloop()
```

---

## ۲. استفاده در PyQt / PySide

برای ویجت‌های `QLineEdit` در کیوت:

```python
from PyQt5.QtWidgets import QApplication, QLineEdit, QVBoxLayout, QWidget
import parsikit

app = QApplication([])
window = QWidget()
layout = QVBoxLayout()

card_input = QLineEdit()
card_input.setPlaceholderText("شماره کارت ۱۶ رقمی...")
parsikit.bind_persian_input(card_input, input_type="card")

layout.addWidget(card_input)
window.setLayout(layout)
window.show()
app.exec_()
```

---

## ۳. قابلیت‌های پیشرفته تایپ هوشمند و حفظ نشانگر (Cursor Tracking)

در نسخه‌ی ۳.۳.۱ با استفاده از محاسبه‌ی موقعیت نسبی کاراکترها، نشانگر ماوس/کیبورد در زمان تایپ، حذف و جایگزینی در میانه‌ی کلمات هرگز به انتهای سطر پرش نمی‌کند.

```python
# فعال‌سازی میانبرهای متنی، اصلاح هوشمند نیم‌فاصله و ارقام فارسی
parsikit.bind_persian_input(
    entry,
    input_type="text",
    digit_style="persian",
    smart_spacing=True,
    snippets={"ق.ظ": "قبل از ظهر", "ب.ظ": "بعد از ظهر"},
    enable_shortcuts=True
)

# آزادسازی و قطع اتصال در زمان تخریب ویجت
parsikit.unbind_persian_input(entry)
```

---

## انواع فیلدهای پشتیبانی شده در `bind_persian_input`:
- `"text"`: زیباسازی و استانداردسازی فاصله‌های متن فارسی
- `"national_code"`: قالب ۳-۶-۱ کد ملی
- `"card"` یا `"card_number"`: قالب ۴ تکه‌ای شماره کارت بانکی
- `"postal_code"`: قالب ۵-۵ کد پستی (`XXXXX-XXXXX`)
- `"sheba"`: قالب استاندارد شماره شبا با پیشوند `IR` و فواصل ۴ تایی
- `"mobile"`: قالب شماره تلفن همراه با پیشوند استاندارد
