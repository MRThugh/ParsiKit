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

## 3. Мудирияти навишти мустақим дар Tkinter / CustomTkinter

Ислоҳи худкори навишт ҳангоми чоп кардани корбар:

```python
import tkinter as tk
import parsikit

root = tk.Tk()
entry = tk.Entry(root, font=("Vazirmatn", 14))
entry.pack(padx=20, pady=20)

# Пайваст кардани рӯйдодҳо ва ислоҳи худкори ҳарфҳо
parsikit.bind_persian_input(entry)

root.mainloop()
```
