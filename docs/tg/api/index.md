# Маълумотномаи мукаммали API (ParsiKit)

Феҳристи ҳамаи модулҳо ва функсияҳои расмии дастрас дар **ParsiKit v3.3.1**:

| Модул | Тавсифи вазифа | Ҳуҷҷатгузории муфассал |
|---|---|---|
| `parsikit.text` | Ҳамоҳангсозии ҳарфҳо, нимафосила, ҳазфи эъроб, истихроҷи додаҳо ва ниқоббандӣ | [Маълумотномаи матн](text.md) |
| `parsikit.validators` | Санҷиши рамзи миллӣ, телефон, кортҳои бонкӣ, суратҳисобҳо ва рақамҳои нақлиёт | [Маълумотномаи эътиборсанҷӣ](validators.md) |
| `parsikit.models` | Моделҳои сохторёфтаи OOP бо дастгирии бевосита аз Pydantic v2 | [Маълумотномаи моделҳо](models.md) |
| `parsikit.datetime` | Табдили тақвими шамсӣ ва милодӣ, соли кабиса, номи моҳҳо ва вақти нисбӣ | [Маълумотномаи сана ва вақт](datetime.md) |
| `parsikit.number` ва `parsikit.currency` | Табдили рақамҳо, адад ба калимаҳо, амалиёти молиявӣ ва ҳисоби фоизҳо | [Маълумотномаи рақамҳо ва молия](number_and_currency.md) |
| `parsikit.dev` ва `parsikit.gui` | Ҳамоҳангсозии визуалӣ, ташхиси матн, гузориши гурӯҳӣ ва интерфейси графикӣ | [Маълумотномаи ташхис ва GUI](dev_and_gui.md) |
| `parsikit.reshaper` | Бозсозии хатти пайваста барои муҳаррикҳои графикӣ ва тасвирҳо | [Маълумотномаи бозсозии хат](reshaper.md) |
| `parsikit.cache` | Зерсохтори кэши баландсуръат ва амн дар муҳити бисёрриштагӣ | [Маълумотномаи кэш](cache.md) |
| `parsikit.config` ва `parsikit.exceptions` | Танзимоти саросарӣ ва дарахти истисноҳои сохторёфта | [Танзимот ва истисноҳо](#танзимоти-саросарӣ-ва-истисноҳо) |

---

## Танзимоти саросарӣ ва истисноҳо

### Танзимоти саросарӣ (`parsikit.config`)
- `default_tax_rate: float`: Меъёри пешфарзи андоз (пешфарз: `0.10`).
- `default_currency: str`: Воҳиди пулии пешфарзи система, `"toman"` ё `"rial"` (пешфарз: `"toman"`).
- `enable_cache: bool`: Фаъолсозии кэши LRU барои ҳисобҳои вазнин (пешфарз: `True`).

### Синфҳои истисно (`parsikit.exceptions`)
Ҳамаи хатогиҳои махсус аз `ParsiKitError` ва `ValidationError` (зери синфи `ValueError`) мерос мегиранд:
- `InvalidNationalCodeError`
- `InvalidMobileError`
- `InvalidCardNumberError`
- `InvalidShebaError`
- `InvalidPostalCodeError`
- `InvalidPlateError`
- `InvalidBillError`
