"""
parsikit.dev
~~~~~~~~~~~~
Developer tools, debugging aids, text inspectors, and pretty printers.
"""

from __future__ import annotations
import logging
import sys
import string
from typing import Any, Callable, Type
import re

# Import core utilities and exceptions
from parsikit.text import standardize_persian, beautify_persian_spacing, is_persian
from parsikit.number import english_to_persian
from parsikit.exceptions import ValidationError

# ANSI Codes for colored terminal outputs
COLOR_RESET = "\033[0m"
COLOR_BOLD = "\033[1m"
COLOR_RED = "\033[31m"
COLOR_GREEN = "\033[32m"
COLOR_YELLOW = "\033[33m"
COLOR_BLUE = "\033[34m"
COLOR_MAGENTA = "\033[35m"
COLOR_CYAN = "\033[36m"
COLOR_GRAY = "\033[90m"


def _supports_color() -> bool:
    """
    Check if the current terminal environment supports ANSI escape sequences.
    """
    plat = sys.platform
    supported_platform = plat != "win32" or "ANSICON" in sys.environ
    is_a_tty = hasattr(sys.stdout, "isatty") and sys.stdout.isatty()
    return bool(supported_platform and is_a_tty)


class PersianFormatter(string.Formatter):
    """
    Custom string Formatter that accounts for zero-width Persian characters 
    (like ZWNJs and diacritics) to ensure flawless alignment and provides 
    auto Persian-digit conversion via the 'fa' or 'p' suffix.
    """
    _SPEC_REGEX = re.compile(
        r"^(?:(?P<fill>.)?(?P<align>[<>=^]))?"
        r"(?P<sign>[-+ ]+)?"
        r"(?P<alt>#)?"
        r"(?P<zero>0)?"
        r"(?P<width>\d+)?"
        r"(?P<grouping>[_,])?"
        r"(?:\.(?P<precision>\d+))?"
        r"(?P<type>[a-zA-Z%]+)?$"
    )

    def format_field(self, value: Any, format_spec: str) -> str:
        # Detect 'fa' or 'p' suffix for Persian digit translation
        to_persian_digits = False
        if format_spec.endswith("fa"):
            to_persian_digits = True
            format_spec = format_spec[:-2]
        elif format_spec.endswith("p"):
            to_persian_digits = True
            format_spec = format_spec[:-1]

        match = self._SPEC_REGEX.match(format_spec)
        if not match:
            # Fallback to python standard format
            res = format(value, format_spec)
            if to_persian_digits:
                res = english_to_persian(res)
            return res

        gd = match.groupdict()
        width_str = gd.get("width")

        if not width_str:
            res = format(value, format_spec)
            if to_persian_digits:
                res = english_to_persian(res)
            return res

        # Alignments & custom sizes parameters
        width = int(width_str)
        fill = gd.get("fill") or " "
        align = gd.get("align")

        # Set default python alignments
        if not align:
            align = ">" if isinstance(value, (int, float, complex)) else "<"

        # Construct safe spec omitting width and alignment details
        clean_spec_parts = []
        if gd.get("sign"): clean_spec_parts.append(gd["sign"])
        if gd.get("alt"): clean_spec_parts.append(gd["alt"])
        if gd.get("zero"): clean_spec_parts.append(gd["zero"])
        if gd.get("grouping"): clean_spec_parts.append(gd["grouping"])
        if gd.get("precision"): clean_spec_parts.append(f".{gd['precision']}")
        if gd.get("type"): clean_spec_parts.append(gd["type"])
        clean_spec = "".join(clean_spec_parts)

        # Base formatting
        base_str = format(value, clean_spec)

        if to_persian_digits:
            base_str = english_to_persian(base_str)

        # Calculate exact visual width (omitting ZWNJs & Arabic Diacritics)
        zero_width_chars = re.compile(r"[\u200C\u064B-\u065F\u0670]")
        visual_len = len(zero_width_chars.sub("", base_str))

        if visual_len >= width:
            return base_str

        padding_needed = width - visual_len
        if align == "<":
            return base_str + (fill * padding_needed)
        elif align == ">":
            return (fill * padding_needed) + base_str
        elif align == "^":
            left_pad = padding_needed // 2
            right_pad = padding_needed - left_pad
            return (fill * left_pad) + base_str + (fill * right_pad)
        elif align == "=":
            if base_str and base_str[0] in "+- ":
                return base_str[0] + (fill * padding_needed) + base_str[1:]
            return (fill * padding_needed) + base_str

        return base_str


_formatter = PersianFormatter()


def pformat(template: str, *args: Any, **kwargs: Any) -> str:
    """
    Format a template string with Persian-aware visual width adjustments 
    and optional digit conversions.
    
    Supports standard alignments (<, >, ^, =), custom padding characters, 
    and a special 'fa' or 'p' suffix in placeholders (e.g., '{:fa}', '{:>10,fa}')
    to automatically translate digits to standard Persian script.
    
    :param template: Format string template.
    :param args: Positional arguments for formatting.
    :param kwargs: Keyword arguments for formatting.
    :return: Cleanly aligned and formatted Persian string.
    """
    return _formatter.format(template, *args, **kwargs)


def persian_fstring(template: str, **kwargs: Any) -> str:
    """
    Evaluate an f-string-like template with Persian-aware visual alignment 
    and placeholder formatting. Local and global variables from the caller's 
    context are automatically captured if not explicitly passed as arguments.
    
    :param template: The target f-string template (e.g. "Name: {name:fa}").
    :param kwargs: Explicit variables override.
    :return: Cleanly aligned and formatted Persian string.
    """
    try:
        frame = sys._getframe(1)
        caller_vars = {**frame.f_globals, **frame.f_locals}
    except Exception:
        caller_vars = {}

    merged = {**caller_vars, **kwargs}
    return _formatter.format(template, **merged)


def persian_repr(obj: Any) -> str:
    """
    Generate a human-readable representation of Python objects containing Persian text,
    ensuring that Unicode characters are rendered cleanly instead of escaped.
    
    :param obj: The target object to format.
    :return: A cleanly formatted string representation.
    """
    if isinstance(obj, str):
        return f"'{obj}'"
    elif isinstance(obj, dict):
        items = [f"{persian_repr(k)}: {persian_repr(v)}" for k, v in obj.items()]
        return "{" + ", ".join(items) + "}"
    elif isinstance(obj, list):
        items = [persian_repr(x) for x in obj]
        return "[" + ", ".join(items) + "]"
    elif isinstance(obj, tuple):
        items = [persian_repr(x) for x in obj]
        return "(" + ", ".join(items) + ")"
    elif isinstance(obj, set):
        items = [persian_repr(x) for x in obj]
        return "{" + ", ".join(items) + "}"
    elif hasattr(obj, "to_dict"):
        try:
            return f"{obj.__class__.__name__}({persian_repr(obj.to_dict())})"
        except Exception:
            return repr(obj)
    else:
        return repr(obj)


def pretty_print(obj: Any, title: str | None = None, style: str = "persian", color: bool = True) -> None:
    """
    Prints list, dict, and ParsiKit models with dynamic alignment and optional terminal coloring.
    
    :param obj: The structure or model to output.
    :param title: Optional header text.
    :param style: Aesthetic output style.
    :param color: If True, uses ANSI escape codes to add colors on compatible terminals.
    """
    use_color = color and _supports_color()

    def colored(text: str, color_code: str) -> str:
        return f"{color_code}{text}{COLOR_RESET}" if use_color else text

    # Handle domain models with serialization support
    if hasattr(obj, "to_dict"):
        data = obj.to_dict()
    elif hasattr(obj, "dict"):
        data = obj.dict()
    else:
        data = obj

    if title:
        banner = f"=== {title} ==="
        print(colored(banner, COLOR_CYAN + COLOR_BOLD))

    def _format_value(val: Any) -> str:
        if isinstance(val, str):
            return colored(f"'{val}'", COLOR_GREEN)
        elif isinstance(val, bool):
            return colored(str(val), COLOR_MAGENTA)
        elif val is None:
            return colored("None", COLOR_MAGENTA)
        elif isinstance(val, (int, float)):
            return colored(str(val), COLOR_YELLOW)
        return colored(persian_repr(val), COLOR_GRAY)

    def _dump(current: Any, indent: int = 0) -> None:
        pad = "  " * indent
        if isinstance(current, dict):
            if not current:
                print(f"{pad}{{}}")
                return
            print(f"{pad}{{}}")
            for k, v in current.items():
                key_str = colored(f"'{k}'", COLOR_BLUE + COLOR_BOLD)
                if isinstance(v, (dict, list)):
                    print(f"{pad}  {key_str}:")
                    _dump(v, indent + 2)
                else:
                    print(f"{pad}  {key_str}: {_format_value(v)}")
            print(f"{pad}}}")
        elif isinstance(current, (list, tuple, set)):
            char_open = "[" if isinstance(current, list) else "(" if isinstance(current, tuple) else "{"
            char_close = "]" if isinstance(current, list) else ")" if isinstance(current, tuple) else "}"
            if not current:
                print(f"{pad}{char_open}{char_close}")
                return
            print(f"{pad}{char_open}")
            for item in current:
                if isinstance(item, (dict, list, tuple, set)):
                    _dump(item, indent + 1)
                else:
                    print(f"{pad}  {_format_value(item)}")
            print(f"{pad}{char_close}")
        else:
            print(f"{pad}{_format_value(current)}")

    _dump(data)


def inspect_text(text: str) -> dict[str, Any]:
    """
    Analyze a Persian string to inspect potential layout, spacing, and character issues.
    
    :param text: String to analyze.
    :return: A dictionary containing metrics and suggestions.
    """
    if not text:
        return {
            "length": 0,
            "word_count": 0,
            "is_persian": False,
            "has_arabic_chars": False,
            "has_english_digits": False,
            "has_arabic_digits": False,
            "has_diacritics": False,
            "has_zwnj_issues": False,
            "has_spacing_issues": False,
            "is_mixed_script": False,
            "suggestions": []
        }

    length = len(text)
    word_count = len(text.split())
    is_pers_flag = is_persian(text)

    # Specific Arabic letters check
    has_arabic_chars = bool(re.search(r"[\u064A\u0649\u0643\u0629]", text))
    
    # Digits validation
    has_english_digits = bool(re.search(r"[0-9]", text))
    has_arabic_digits = bool(re.search(r"[\u0660-\u0669]", text))

    # Diacritics detection
    has_diacritics = bool(re.search(r"[\u064B-\u065F\u0670]", text))

    # Check ZWNJ (half-space) issues
    std_text = standardize_persian(text)
    has_zwnj_issues = (std_text != text)

    # Check Spacing issues
    beautified = beautify_persian_spacing(text)
    has_spacing_issues = (beautified != text)

    # Mixed-script detection (English letters + Persian script)
    has_english_letters = bool(re.search(r"[a-zA-Z]", text))
    is_mixed_script = is_pers_flag and has_english_letters

    suggestions = []
    if has_arabic_chars:
        suggestions.append("Replace Arabic letters (ي, ك, ة) with standard Persian equivalents (ی, ک, ه).")
    if has_english_digits or has_arabic_digits:
        suggestions.append("Standardize digits into Persian format using parsikit.english_to_persian.")
    if has_zwnj_issues:
        suggestions.append("Add proper zero-width non-joiners (ZWNJs) around prefixes/suffixes.")
    if has_spacing_issues:
        suggestions.append("Normalize redundant spaces and correct punctuation layout using beautify_persian_spacing.")
    if is_mixed_script:
        suggestions.append("Script has mixed Persian and English elements. Check keyboard layout.")

    return {
        "length": length,
        "word_count": word_count,
        "is_persian": is_pers_flag,
        "has_arabic_chars": has_arabic_chars,
        "has_english_digits": has_english_digits,
        "has_arabic_digits": has_arabic_digits,
        "has_diacritics": has_diacritics,
        "has_zwnj_issues": has_zwnj_issues,
        "has_spacing_issues": has_spacing_issues,
        "is_mixed_script": is_mixed_script,
        "suggestions": suggestions
    }


def debug_text(text: str) -> None:
    """
    Performs interactive textual analysis on a string and prints a structured, colored report.
    
    :param text: String to debug.
    """
    analysis = inspect_text(text)
    use_color = _supports_color()

    def colored(t: str, c: str) -> str:
        return f"{c}{t}{COLOR_RESET}" if use_color else t

    print(colored("┌────────────────────────────────────────────────────────┐", COLOR_GRAY))
    print(colored("│ ParsiKit Text Debugger Analysis                        │", COLOR_CYAN + COLOR_BOLD))
    print(colored("├────────────────────────────────────────────────────────┤", COLOR_GRAY))
    print(f"  Raw Text: {colored(f'\"{text}\"', COLOR_GREEN)}")
    print(colored("├────────────────────────────────────────────────────────┤", COLOR_GRAY))
    print(f"  Length: {colored(str(analysis['length']), COLOR_YELLOW)} characters")
    print(f"  Word Count: {colored(str(analysis['word_count']), COLOR_YELLOW)}")

    def format_bool(status: bool) -> str:
        return colored("Yes ✔", COLOR_GREEN) if status else colored("No ✘", COLOR_GRAY)

    print(f"  Is Persian Script: {format_bool(analysis['is_persian'])}")
    print(f"  Has Arabic Letters: {format_bool(analysis['has_arabic_chars'])}")
    print(f"  Has English Digits: {format_bool(analysis['has_english_digits'])}")
    print(f"  Has Arabic Digits: {format_bool(analysis['has_arabic_digits'])}")
    print(f"  Has Diacritics: {format_bool(analysis['has_diacritics'])}")
    print(f"  Has Layout/ZWNJ Issues: {format_bool(analysis['has_zwnj_issues'])}")
    print(f"  Has Spacing Issues: {format_bool(analysis['has_spacing_issues'])}")
    print(f"  Is Mixed English/Persian: {format_bool(analysis['is_mixed_script'])}")
    print(colored("├────────────────────────────────────────────────────────┤", COLOR_GRAY))

    if analysis['suggestions']:
        print(colored("  Recommended Actions:", COLOR_YELLOW + COLOR_BOLD))
        for i, suggestion in enumerate(analysis['suggestions'], 1):
            print(f"    {i}. {suggestion}")
    else:
        print(colored("  Clean text! No structural or layout issues found.", COLOR_GREEN + COLOR_BOLD))
    print(colored("└────────────────────────────────────────────────────────┘", COLOR_GRAY))


def validate_batch(items: list[Any], model_class: Type[Any], silent: bool = False) -> dict[str, Any]:
    """
    Performs validation on a collection of inputs using a designated ParsiKit Domain Model.
    
    :param items: List of candidate strings or structures to validate.
    :param model_class: The ParsiKit domain model (e.g. NationalCode, MobileNumber).
    :param silent: If True, suppresses outputting reports to stdout.
    :return: A dictionary containing structural metrics, valid instances, and errors.
    """
    valid_instances = []
    errors = []

    for index, item in enumerate(items):
        try:
            instance = model_class(item)
            valid_instances.append(instance)
        except ValidationError as e:
            errors.append({
                "index": index,
                "item": item,
                "error": str(e)
            })
        except Exception as e:
            errors.append({
                "index": index,
                "item": item,
                "error": f"Unexpected Error: {str(e)}"
            })

    total = len(items)
    valid_count = len(valid_instances)
    invalid_count = len(errors)

    report = {
        "total": total,
        "valid_count": valid_count,
        "invalid_count": invalid_count,
        "valid_items": valid_instances,
        "errors": errors
    }

    if not silent:
        use_color = _supports_color()

        def colored(t: str, c: str) -> str:
            return f"{c}{t}{COLOR_RESET}" if use_color else t

        print(colored(f"\n--- Batch Validation Summary for {model_class.__name__} ---", COLOR_CYAN + COLOR_BOLD))
        print(f"Total Evaluated: {colored(str(total), COLOR_YELLOW)}")
        print(f"Valid Elements : {colored(str(valid_count), COLOR_GREEN)}")
        print(f"Invalid Elements: {colored(str(invalid_count), COLOR_RED if invalid_count > 0 else COLOR_GRAY)}")

        if errors:
            print(colored("\nValidation Errors:", COLOR_RED + COLOR_BOLD))
            for error in errors:
                item_str = f"'{error['item']}'" if isinstance(error['item'], str) else str(error['item'])
                print(f"  Index {error['index']} | Item: {colored(item_str, COLOR_YELLOW)} | Reason: {colored(error['error'], COLOR_RED)}")
        else:
            print(colored("\nExcellent! All items processed without validation issues.", COLOR_GREEN + COLOR_BOLD))

    return report


class PersianLogFormatter(logging.Formatter):
    """
    Custom formatter ensuring raw Persian strings within containers
    are printed cleanly in log outputs.
    """
    def format(self, record: logging.LogRecord) -> str:
        if isinstance(record.msg, (list, dict, tuple, set)):
            record.msg = persian_repr(record.msg)
        return super().format(record)


def setup_logging(level: str = "INFO") -> logging.Logger:
    """
    Configures standard python logger to display Persian characters correctly in log output.
    
    :param level: Target logging level (e.g. "INFO", "DEBUG").
    :return: A configured logging instance.
    """
    logger = logging.getLogger("parsikit")
    logger.setLevel(level)

    if logger.handlers:
        logger.handlers.clear()

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)

    formatter = PersianLogFormatter(
        fmt="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False

    return logger