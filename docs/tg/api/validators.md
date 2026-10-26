# Маълумотномаи модули эътиборсанҷӣ (`parsikit.validators`)

Маҷмӯаи функсияҳои санҷиши дурустии додаҳои расмӣ ва молиявӣ:

---

## Функсияҳои асосӣ

### `is_valid_national_code(code: str, strict: bool = True) -> bool`
Санҷиши эътибори рамзи 10-рақама бо истифода аз алгоритми бақияи тақсим ба 11 (чек-сам).

### `format_national_code(code: str) -> str`
Қолаббандии рамз ба 3 бахши хатчадор (`XXX-XXXXXX-X`).

### `detect_national_code_location(code: str) -> dict | None`
Муайян кардани минтақа ва шаҳри судур аз рӯи 3 рақами аввал.

### `is_valid_mobile(phone: str) -> bool`
Санҷиши сохтори рақами мобилӣ аз рӯи пешрақами ширкатҳо.

### `normalize_mobile(phone: str, prefix: str = "0") -> str`
Ҳамоҳангсозии рақам ба қолаби дохилӣ (`09...`) ё байналмилалӣ (`+989...`).

### `detect_mobile_operator(phone: str) -> str | None`
Шинохти номи ширкати алоқаи мобилӣ.

### `is_valid_landline(phone: str) -> bool`
Санҷиши рақамҳои телефони доимӣ бо рамзи шаҳрӣ.

### `detect_landline_province(phone: str) -> str | None`
Муайян кардани минтақаи телефони доимӣ.

### `is_valid_card_number(card: str) -> bool`
Санҷиши кортҳои бонкии 16-рақама бо алгоритми Лун (Luhn Mod-10).

### `format_card_number(card: str, separator: str = "-") -> str`
Гурӯҳбандии корт ба 4 қисми чоррақама.

### `detect_bank_from_card(card: str) -> str | None`
Муайян кардани номи бонки содиркунанда аз рӯи 6 рақами аввал.

### `is_valid_sheba(sheba: str) -> bool`
Санҷиши рақами IBAN аз рӯи стандарти байналмилалии ISO 7064 Mod 97-10.

### `format_sheba(sheba: str, chunk_size: int = 4) -> str`
Фосилагузории хоно дар рақами суратҳисоб.

### `detect_bank_from_sheba(sheba: str) -> str | None`
Муайян кардани номи бонк аз рӯи рамзи дохили суратҳисоб.

### `is_valid_postal_code(code: str) -> bool`
Санҷиши сохтори 10-рақамаи рамзи почта.

### `format_postal_code(code: str) -> str`
Қолаббандии рамзи почта ба шакли ду бахши панҷрақама (`XXXXX-XXXXX`).

### `is_valid_corporate_id(corp_id: str) -> bool`
Санҷиши рамзи 11-рақамаи шахсони ҳуқуқӣ ва ширкатҳо.

### `is_valid_bill_and_payment(bill_id: str, pay_id: str) -> bool`
Санҷиши эътибори рамзи пардохт ва ҳисобномаҳои хидматрасонӣ.

### `extract_bill_details(bill_id: str, pay_id: str) -> dict`
Истихроҷи навъи хидмат, маблағи пардохт ва давраи ҳисобнома.

### `is_valid_plate(plate: str) -> bool`
Санҷиши сохтори рақами давлатии воситаҳои нақлиёт.

### `parse_plate(plate: str) -> dict`
Таҳлили рақамҳо, ҳарфи мобайн ва рамзи минтақаи рақами мошин.

### `detect(text: str) -> str | None`
Ташхиси худкор ва ҳушманди навъи маълумоти воридшуда (`national_code`, `mobile`, `card`, `sheba`, `email`, `url`, `ip`).
