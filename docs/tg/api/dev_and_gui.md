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
Чопи гузориши ранга ва сохторёфта дар консоли фармонҳо.

### `validate_batch(items: list, model_class, silent: bool = False) -> dict`
Санҷиши эътибори ҳамзамони гурӯҳи калони маълумот дар асоси яке аз моделҳои ParsiKit ва таҳияи ҷадвали натиҷаҳо.

---

## Бозсозии хат ва идораи вуруди графикӣ (`parsikit.reshaper`, `parsikit.gui`)

### `reshape_for_graphics(text: str, reverse: bool = True) -> str`
Пайваст кардани ҳарфҳо ва танзими самти навишт барои муҳаррикҳои 2D, ки HarfBuzz надоранд (монанди Pillow, Pygame, OpenCV).

### `reshape_paragraph_for_graphics(text: str, max_chars_per_line: int, reverse: bool = True) -> list[str]`
Тақсим ва бозсозии бандҳои дарози матнӣ ба сатрҳои мувофиқ барои расмкашӣ.

### `bind_persian_input(widget, input_type: str = "text") -> None`
Пайваст кардани ҳолати ислоҳи худкори навишт ба майдонҳои вуруди Tkinter ва CustomTkinter.
