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
}

# Standard Lam-Alef ligatures: (Isolated, Final)
_LIGATURES: dict[tuple[str, str], tuple[str, str]] = {
    ('ل', 'ا'): ('\uFEFB', '\uFEFC'),
    ('ل', 'آ'): ('\uFEF5', '\uFEF6'),
    ('ل', 'أ'): ('\uFEF7', '\uFEF8'),
    ('ل', 'إ'): ('\uFEF9', '\uFEFA'),
}


def _is_rtl_char(c: str) -> bool:
    """Check if the given character belongs to the RTL Persian/Arabic Unicode blocks."""
    o = ord(c)
    return (0x0600 <= o <= 0x06FF) or (0xFB50 <= o <= 0xFDFF) or (0xFE70 <= o <= 0xFEFF) or c == '\u200C'


def _reshape_word(text: str) -> str:
    """Core logic to shape Persian letters according to their surrounding characters."""
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
            # Process Lam-Alef ligature
            connects_prev = False
            if i > 0:
                prev_item = processed_chars[i-1]
                if not isinstance(prev_item, tuple) and prev_item in _SHAPES:
                    connects_prev = _SHAPES[prev_item][5]  # connects_left of previous char
            
            isolated, final = _LIGATURES[item]
            shape = final if connects_prev else isolated
            result.append(shape)
        else:
            char = item
            if char not in _SHAPES:
                result.append(char)
                continue

            # Check previous character connection
            connects_prev = False
            if i > 0:
                prev_item = processed_chars[i-1]
                if isinstance(prev_item, tuple):
                    # Previous was ligature (ends with Alef which doesn't connect left)
                    connects_prev = False
                elif prev_item in _SHAPES:
                    connects_prev = _SHAPES[prev_item][5] and _SHAPES[char][4]

            # Check next character connection
            connects_next = False
            if i < n_processed - 1:
                next_item = processed_chars[i+1]
                if isinstance(next_item, tuple):
                    # Next is ligature (starts with Lam which connects right)
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
    """Prepare Persian text for rendering inside engines that lack RTL/Shaping support.

    Separates RTL and LTR blocks, shapes the Persian characters, and optionally
    reverses the RTL parts so they display in correct reading order on LTR canvases.

    Args:
        text:    Standard Persian/English input string.
        reverse: If True, reverses the layout of the RTL chunks for LTR graphic cards.

    Returns:
        The transformed string containing reshaped presentation forms.
    """
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