# Роҳнамо: Интегратсия бо интерфейсҳои графикӣ (GUI) ва расмкашӣ

Расмкашии матнҳои рости шарқӣ дар барномаҳои мизи корӣ (Tkinter, PyQt, PySide) ё китобхонаҳои коркарди тасвир (Pillow, OpenCV) омодасозии махсуси пайвасти ҳарфҳоро тақозо мекунад.

---

## 1. Расмкашии тасвир ва матн дар Pillow ва OpenCV

Барои муҳаррикҳое, ки пайвасти хатти шаклиро пуштибонӣ намекунанд, аз `reshape_for_graphics` истифода баред:

```python
from PIL import Image, ImageDraw, ImageFont
import parsikit

# Сохтани тасвири холӣ
image = Image.new("RGB", (600, 200), color=(255, 255, 255))
draw = ImageDraw.Draw(image)

# Бозсозии матн барои расмкашӣ
text = "Системаи идоракунии ҳуҷҷатҳо"
reshaped = parsikit.reshape_for_graphics(text)

# draw.text((50, 80), reshaped, fill=(0, 0, 0))
```

---

## 2. Тақсимбандии бандҳои дароз (`reshape_paragraph_for_graphics`)

Барои қуттиҳои матнии бисёрсатра:

```python
import parsikit

paragraph = (
    "Китобхонаи ParsiKit маҷмӯаи асбобҳои стандартсозӣ ва "
    "санҷиши додаҳо барои таҳиягарони Python мебошад."
)

wrapped_lines = parsikit.reshape_paragraph_for_graphics(paragraph, max_chars_per_line=30)
for line in wrapped_lines:
    print(line)
```

---

## 3. Мудирияти навишти мустақим дар Tkinter ва CustomTkinter

Ислоҳи худкори навишт ҳангоми чоп кардани корбар бе ҷаҳиши курсор:

```python
import tkinter as tk
import parsikit

root = tk.Tk()
root.title("Вуруди ҳушманди форсӣ")

entry = tk.Entry(root, font=("Vazirmatn", 14), width=35)
entry.pack(padx=20, pady=20)

# Пайваст кардани ёвари навишт бо ҳифзи курсор ва ихтисорот
parsikit.bind_persian_input(
    entry,
    input_type="text",
    digit_style="persian",
    smart_spacing=True,
    snippets={"қ.з": "қабл аз зӯҳр", "б.з": "баъд аз зӯҳр"},
    enable_shortcuts=True
)

root.mainloop()
```

---

## 4. Пайвастшавӣ бо PyQt ва PySide

Истифода бо виҷетҳои Qt (`QLineEdit`, `QTextEdit`):

```python
from PyQt6.QtWidgets import QApplication, QLineEdit, QVBoxLayout, QWidget
import parsikit

app = QApplication([])
window = QWidget()
layout = QVBoxLayout()

card_input = QLineEdit()
card_input.setPlaceholderText("Рақами корт...")
parsikit.bind_persian_input(card_input, input_type="card")

layout.addWidget(card_input)
window.setLayout(layout)
window.show()
app.exec()
```

---

## 5. Қатъи бехатари пайваст (`unbind_persian_input`)

Барои қатъи амалиёти назорат ҳангоми бастани виҷет:

```python
parsikit.unbind_persian_input(entry)
```
