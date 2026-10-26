# Маълумотномаи модулҳои ташхис ва интерфейси графикӣ (`parsikit.dev`, `parsikit.gui`)

---

## Ҳамоҳангсозии визуалӣ ва ташхиси матн (`parsikit.dev`)

### `pformat(template: str, *args, **kwargs) -> str`
Қолаббандии ҳушманди матн, ки таъсири аломатҳои бепаҳноро (нимафосила, эъроб) ба назар гирифта, баробарсозии сутунҳоро аз рӯи паҳнои воқеии экран ҳисоб мекунад. Аз нишонаҳои `:fa` ва `:p` барои табдили худкори рақамҳо пуштибонӣ менамояд.

### `persian_fstring(template: str, **kwargs) -> str`
Арзёбии сатрҳои қолаббандӣ бо хондани худкори тағйирёбандаҳо аз муҳити барнома ва татбиқи баробарсозии визуалӣ.

### `inspect_text(text: str) -> dict`
Таҳлили муфассали матн ва пешниҳоди ҳисоботи оморӣ аз теъдоди ҳарфҳо, нимафосилаҳо ва пешниҳодҳои ислоҳӣ.

### `debug_text(text: str) -> None`
Чопи гузориши ранга ва сохторёфта дар консоли фармонҳо бо риояи стандартҳои `NO_COLOR`, `FORCE_COLOR`, терминали Windows (`WT_SESSION`) ва ConEmu.

### `validate_batch(items: list, model_class, silent: bool = False) -> dict`
Санҷиши эътибори ҳамзамони гурӯҳи калони маълумот дар асоси яке аз моделҳои ParsiKit ва таҳияи ҷадвали натиҷаҳо.

---

## Бозсозии хат ва идораи вуруди графикӣ (`parsikit.reshaper`, `parsikit.gui`)

### `reshape_for_graphics(text: str, reverse: bool = True) -> str`
Пайваст кардани ҳарфҳо ва танзими самти навишт барои муҳаррикҳои 2D, ки HarfBuzz надоранд (монанди Pillow, Pygame, OpenCV).

### `reshape_paragraph_for_graphics(text: str, max_chars_per_line: int, reverse: bool = True) -> list[str]`
Тақсим ва бозсозии бандҳои дарози матнӣ ба сатрҳои мувофиқ барои расмкашӣ.

### `bind_persian_input(widget, input_type: str = "text", *, digit_style: str = "auto", smart_spacing: bool = False, snippets: dict[str, str] | None = None, enable_shortcuts: bool = True) -> None`
Пайваст кардани ёвари худкори навишти форсӣ ба майдонҳои вуруди графикӣ:
- **Китобхонаҳои дастгиришаванда**:
  - Майдонҳои Tkinter (`tk.Entry`, `tk.Text`)
  - Элементҳои CustomTkinter (`ctk.CTkEntry`)
  - Фреймворки Qt (`QLineEdit`, `QTextEdit`, `QPlainTextEdit` дар PyQt5, PyQt6, PySide2, PySide6)
- **Нигоҳдории ҳушманди мавқеи курсор (Cursor Tracking)**:
  - Пешгирӣ аз ҷаҳиши ногаҳонии курсор ба охири сатр ҳангоми воридкунӣ, поксозӣ ё таҳрир дар миёнаи матн.
- **Параметрҳо**:
  - `input_type`: навъи вурудӣ (`"text"`, `"national_code"`, `"mobile"`, `"card"`, ё `"sheba"`).
  - `digit_style`: тарзи табдили рақамҳо (`"auto"`, `"persian"`, `"english"`, ё `"none"`).
  - `smart_spacing`: ислоҳи худкори нимафосилаҳо (`ме-`, `-ҳо`).
  - `snippets`: луғати ихтисорот барои ҷойгузинии зуд.
  - `enable_shortcuts`: фаъолсозии тугмаҳои ёрирасон ба мисли Shift+Space.

### `unbind_persian_input(widget) -> None`
Қатъи бехатари пайвасти ҳолати навишт аз виҷети графикӣ.
