# Маълумотномаи рақамҳо ва амалиёти молиявӣ (`parsikit.number`, `parsikit.currency`)

---

## Рақамҳо (`parsikit.number`)

### `english_to_persian(text: str) -> str`
Табдили рақамҳои англисӣ (`0-9`) ба рақамҳои шарқӣ (`۰-۹`).

### `persian_to_english(text: str) -> str`
Табдили рақамҳои шарқӣ ва арабӣ ба рақамҳои стандартии англисӣ (`0-9`).

### `number_to_words(number: int | float) -> str`
Табдили ададҳо ба калимаҳои хаттӣ то септиллион бо истифода аз кэши зудамал.

---

## Амалиёти молиявӣ (`parsikit.currency`)

### `rial_to_toman(amount: int | float) -> int | float`
Табдили риёл ба тумон (тақсим ба 10).

### `toman_to_rial(amount: int | float) -> int | float`
Табдили тумон ба риёл (зарб ба 10).

### `format_currency(amount, currency="toman", *, persian_digits=False) -> str`
Қолаббандии маблағҳо бо ҷудокунандаи 3-рақама ва номи воҳиди пулӣ.

### `format_currency_to_words(amount, currency="toman") -> str`
Навиштани маблағи пулӣ бо калимаҳо ва номи асъор.

### `add_tax_and_toll(amount, tax_rate=None) -> dict`
Ҳисоби андоз аз арзиши иловашуда (ААИ) ва маблағи ниҳоии пардохт.

### `calculate_installments(principal, annual_interest_rate, months) -> dict`
Ҳисоби пардохтҳои моҳонаи қарз, фоизи умумӣ ва маблағи бозпардохт тибқи формулаи стандартии бонкӣ.
