# Роҳнамои насб ва танзими ParsiKit

Китобхонаи ParsiKit ба забони барномасозии Python версияи **3.10** ё болотар ниёз дорад ва бидуни вобастагиҳои беруна (Zero External Dependencies) кор мекунад.

---

## 1. Насб тавассути PyPI

Роҳи осонтарини насби китобхона истифодаи менеҷери бастаҳои `pip` мебошад:

```bash
pip install parsikit
```

Барои навсозӣ ба версияи устувори охирин:
```bash
pip install --upgrade parsikit
```

---

## 2. Насб дар муҳитҳои маҷозӣ (Virtual Environments)

### Бо истифода аз маҷмӯаи расмии `venv`
```bash
python3 -m venv .venv
source .venv/bin/activate  # Дар Windows: .venv\Scripts\activate
pip install parsikit
```

### Бо истифода аз Poetry
```bash
poetry add parsikit
```

### Бо истифода аз uv
```bash
uv pip install parsikit
```

---

## 3. Насб мустақиман аз рамзи ибтидоӣ (Source)

Барои рушд, таҳия ё истифода аз тағйироти охирин дар шохаи асосии GitHub:

```bash
git clone https://github.com/MRThugh/ParsiKit.git
cd ParsiKit
pip install -e .
```

---

## 4. Санҷиши дурустии насб

Барои боварӣ ҳосил кардан аз дурустии насб, фармони зеринро дар консол иҷро намоед:

```bash
python3 -c "import parsikit; print('ParsiKit version:', parsikit.__version__)"
```

Натиҷа бояд версияи `3.3.1`-ро нишон диҳад.
