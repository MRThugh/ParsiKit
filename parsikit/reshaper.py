"""
parsikit.reshaper
~~~~~~~~~~~~~~~~~
A lightweight, zero-dependency Persian text shaper and layout reorganizer for graphical applications.
"""

from __future__ import annotations

# Standard Persian and Arabic characters presentation forms mapping
# Format: 'char': (Isolated, Initial, Medial, Final, connects_right, connects_left)
_SHAPES: dict[str, tuple[str, str, str, str, bool, bool]] = {
    'آ': ('\uFE81', '', '', '\uFE82', True, False),
    'ا': ('\uFE8D', '', '', '\uFE8E', True, False),
    'ب': ('\uFE8F', '\uFE91', '\uFE92', '\uFE90', True, True),
    'پ': ('\uFB56', '\uFB58', '\uFB59', '\uFB57', True, True),
    'ت': ('\uFE95', '\uFE97', '\uFE98', '\uFE96', True, True),
    'ث': ('\uFE99', '\uFE9B', '\uFE9C', '\uFE9A', True, True),
    'ج': ('\uFE9D', '\uFE9F', '\uFEA0', '\uFE9E', True, True),
    'چ': ('\uFB7A', '\uFB7C', '\uFB7D', '\uFB7B', True, True),
    'ح': ('\uFEA1', '\uFEA3', '\uFEA4', '\uFEA2', True, True),
    'خ': ('\uFEA5', '\uFEA7', '\uFEA8', '\uFEA6', True, True),
    'د': ('\uFEA9', '', '', '\uFEAA', True, False),
    'ذ': ('\uFEAB', '', '', '\uFEAC', True, False),
    'ر': ('\uFEAD', '', '', '\uFEAE', True, False),
    'ز': ('\uFEAF', '', '', '\uFEB0', True, False),
    'ژ': ('\uFB8A', '', '', '\uFB8B', True, False),
    'س': ('\uFEB1', '\uFEB3', '\uFEB4', '\uFEB2', True, True),
    'ش': ('\uFEB5', '\uFEB7', '\uFEB8', '\uFEB6', True, True),
    'ص': ('\uFEB9', '\uFEBB', '\uFEBC', '\uFEBA', True, True),
    'ض': ('\uFEBD', '\uFEBF', '\uFEC0', '\uFEBE', True, True),
    'ط': ('\uFEC1', '\uFEC3', '\uFEC4', '\uFEC2', True, True),
    'ظ': ('\uFEC5', '\uFEC7', '\uFEC8', '\uFEC6', True, True),
    'ع': ('\uFEC9', '\uFECB', '\uFECC', '\uFECA', True, True),
    'غ': ('\uFECD', '\uFECF', '\uFED0', '\uFECE', True, True),
    'ف': ('\uFED1', '\uFED3', '\uFED4', '\uFED2', True, True),
    'ق': ('\uFED5', '\uFED7', '\uFED8', '\uFED6', True, True),
    'ک': ('\uFED9', '\uFEDB', '\uFEDC', '\uFEDA', True, True),
    'گ': ('\uFB92', '\uFB94', '\uFB95', '\uFB93', True, True),
    'ل': ('\uFEDD', '\uFEDF', '\uFEE0', '\uFEDE', True, True),
    'م': ('\uFEE1', '\uFEE3', '\uFEE4', '\uFEE2', True, True),
    'ن': ('\uFEE5', '\uFEE7', '\uFEE8', '\uFEE6', True, True),
    'و': ('\uFEED', '', '', '\uFEEE', True, False),
    'ه': ('\uFEE9', '\uFEEB', '\uFEEC', '\uFEEA', True, True),
    'ی': ('\uFEF1', '\uFEF3', '\uFEF4', '\uFEF2', True, True),
    'ئ': ('\uFE89', '\uFE8B', '\uFE8C', '\uFE8A', True, True),
    'ء': ('\uFE80', '', '', '', False, False),
    'ة': ('\uFE93', '', '', '\uFE94', True, False),
    'أ': ('\uFE83', '', '', '\uFE84', True, False),
    'إ': ('\uFE87', '', '', '\uFE88', True, False),
    'ؤ': ('\uFE85', '', '', '\uFE86', True, False),
}

# Standard Lam-Alef ligatures: (Isolated, Final)
_LIGATURES: dict[tuple[str, str], tuple[str, str]] = {
    ('ل', 'ا'): ('\uFEFB', '\uFEFC'),
    ('ل', 'آ'): ('\uFEF5', '\uFEF6'),
    ('ل', 'أ'): ('\uFEF7', '\uFEF8'),
    ('ل', 'إ'): ('\uFEF9', '\uFEFA'),
}

# Persian/Arabic diacritics Unicode set to ignore during connectivity checks
_DIACRITICS = {
    '\u064B', '\u064C', '\u064D', '\u064E', '\u064F', '\u0650', 
    '\u0651', '\u0652', '\u0653', '\u0654', '\u0655', '\u0670'
}


def _is_rtl_char(c: str) -> bool:
    """Check if the given character belongs to the RTL Persian/Arabic Unicode blocks."""
    o = ord(c)
    return (0x0600 <= o <= 0x06FF) or (0xFB50 <= o <= 0xFDFF) or (0xFE70 <= o <= 0xFEFF) or c == '\u200C'


def _reshape_word(text: str) -> str:
    """Core logic to shape Persian letters according to their surrounding characters (ignores diacritics)."""
    n = len(text)
    if n == 0:
        return text

    # Pre-process to identify Lam-Alef ligatures
    processed_chars: list[str | tuple[str, str]] = []
    i = 0
    while i < n:
        if i < n - 1 and (text[i], text[i+1]) in _LIGATURES:
            processed_chars.append((text[i], text[i+1]))
            i += 2
        else:
            processed_chars.append(text[i])
            i += 1

    n_processed = len(processed_chars)
    result: list[str] = []

    for i in range(n_processed):
        item = processed_chars[i]

        if isinstance(item, tuple):
            # Process Lam-Alef ligature (find previous non-diacritic)
            prev_item = None
            for j in range(i - 1, -1, -1):
                temp = processed_chars[j]
                if isinstance(temp, tuple) or temp not in _DIACRITICS:
                    prev_item = temp
                    break
            
            connects_prev = False
            if prev_item:
                if isinstance(prev_item, tuple):
                    connects_prev = False
                elif prev_item in _SHAPES:
                    connects_prev = _SHAPES[prev_item][5]
            
            isolated, final = _LIGATURES[item]
            shape = final if connects_prev else isolated
            result.append(shape)
        else:
            char = item
            if char in _DIACRITICS:
                result.append(char)
                continue

            if char not in _SHAPES:
                result.append(char)
                continue

            # Find previous non-diacritic neighbor
            prev_item = None
            for j in range(i - 1, -1, -1):
                temp = processed_chars[j]
                if isinstance(temp, tuple) or temp not in _DIACRITICS:
                    prev_item = temp
                    break

            # Find next non-diacritic neighbor
            next_item = None
            for j in range(i + 1, n_processed):
                temp = processed_chars[j]
                if isinstance(temp, tuple) or temp not in _DIACRITICS:
                    next_item = temp
                    break

            # Check previous character connection
            connects_prev = False
            if prev_item:
                if isinstance(prev_item, tuple):
                    connects_prev = False
                elif prev_item in _SHAPES:
                    connects_prev = _SHAPES[prev_item][5] and _SHAPES[char][4]

            # Check next character connection
            connects_next = False
            if next_item:
                if isinstance(next_item, tuple):
                    connects_next = _SHAPES[char][5] and True
                elif next_item in _SHAPES:
                    connects_next = _SHAPES[char][5] and _SHAPES[next_item][4]

            isolated, initial, medial, final, _, _ = _SHAPES[char]

            if connects_prev and connects_next:
                shape = medial or initial or isolated
            elif connects_prev:
                shape = final or isolated
            elif connects_next:
                shape = initial or isolated
            else:
                shape = isolated

            result.append(shape)

    return "".join(result)


def reshape_for_graphics(text: str, reverse: bool = True) -> str:
    """Prepare Persian text for rendering inside engines that lack RTL/Shaping support."""
    if not text:
        return text

    # Shape the standard letters
    shaped_text = _reshape_word(text)

    if not reverse:
        return shaped_text

    # Split string into RTL and LTR blocks to avoid reversing English text
    blocks: list[tuple[bool, str]] = []
    current_block: list[str] = []
    current_is_rtl: bool | None = None

    for char in shaped_text:
        is_rtl = _is_rtl_char(char)
        if current_is_rtl is None:
            current_is_rtl = is_rtl
            current_block.append(char)
        elif is_rtl == current_is_rtl:
            current_block.append(char)
        else:
            blocks.append((current_is_rtl, "".join(current_block)))
            current_block = [char]
            current_is_rtl = is_rtl

    if current_block:
        blocks.append((current_is_rtl, "".join(current_block)))

    # Reconstruct blocks (reverse RTL character order while preserving LTR blocks)
    output: list[str] = []
    for is_rtl, block_text in blocks:
        if is_rtl:
            output.append("".join(reversed(block_text)))
        else:
            output.append(block_text)

    return "".join(output)


def reshape_paragraph_for_graphics(text: str, max_chars_per_line: int, reverse: bool = True) -> list[str]:
    """Reshape a long paragraph, automatically wrapping it into multiple lines of a max length.
    
    Perfect for graphical applications (like Pillow, Pygame, OpenCV) that lack multiline wrapping and shaping.
    """
    if not text:
        return []
    words = text.split(" ")
    lines = []
    current_line = []
    current_length = 0
    for word in words:
        word_len = len(word)
        if current_length + word_len + (1 if current_line else 0) <= max_chars_per_line:
            current_line.append(word)
            current_length += word_len + (1 if len(current_line) > 1 else 0)
        else:
            if current_line:
                lines.append(" ".join(current_line))
            current_line = [word]
            current_length = word_len
    if current_line:
        lines.append(" ".join(current_line))
    return [reshape_for_graphics(line, reverse=reverse) for line in lines]