#!/usr/bin/env python3
"""
ParsiKit Documentation Completeness & Link Validation Engine (v3.3.1)
Author: Ali Kamrani (MRThugh)

Validates:
1. Presence and integrity of all four root README editions (en, fa, fa-AF, tg).
2. Language selector matrices across all root READMEs.
3. 100% 1-to-1 page coverage across all 4 documentation directories (docs/en, docs/fa, docs/fa-AF, docs/tg).
4. Content non-emptiness, minimum size, and absence of unresolved draft placeholders.
5. Regional character/script verification (e.g. Cyrillic for Tajik, Perso-Arabic for fa & fa-AF).
6. Comprehensive internal Markdown link resolution (0 broken links).
7. Official repository and documentation portal URLs.
"""

import sys
import re
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

LANGUAGES = {
    "en": {"name": "English", "dir": "LTR", "script": "latin"},
    "fa": {"name": "Iranian Persian", "dir": "RTL", "script": "persian"},
    "fa-AF": {"name": "Afghan Dari", "dir": "RTL", "script": "dari"},
    "tg": {"name": "Tajikistan Tajik", "dir": "LTR", "script": "cyrillic"},
}

CANONICAL_DOC_PAGES = [
    "index.md",
    "installation.md",
    "quickstart.md",
    "faq.md",
    "troubleshooting.md",
    "api/index.md",
    "api/cache.md",
    "api/datetime.md",
    "api/dev_and_gui.md",
    "api/models.md",
    "api/number_and_currency.md",
    "api/reshaper.md",
    "api/text.md",
    "api/validators.md",
    "guides/forms_and_security.md",
    "guides/gui_integration.md",
    "guides/web_backends.md",
    "tutorials/datetime.md",
    "tutorials/models.md",
    "tutorials/numbers_and_currency.md",
    "tutorials/text_processing.md",
    "tutorials/validation.md",
]

ROOT_READMES = {
    "en": "README.md",
    "fa": "README.fa.md",
    "fa-AF": "README.fa-AF.md",
    "tg": "README.tg.md",
}

FORBIDDEN_PLACEHOLDER_PATTERNS = [
    re.compile(r"\bTODO\b", re.IGNORECASE),
    re.compile(r"\bFIXME\b", re.IGNORECASE),
    re.compile(r"\bTBD\b", re.IGNORECASE),
    re.compile(r"\bLOREM\s+IPSUM\b", re.IGNORECASE),
    re.compile(r"TRANSLATION\s+MISSING", re.IGNORECASE),
    re.compile(r"COMING\s+SOON", re.IGNORECASE),
    re.compile(r"PLACEHOLDER_(CONTENT|TEXT)", re.IGNORECASE),
]

def check_root_readmes():
    errors = []
    print("--> Checking 4 Root README files...")
    for lang, fname in ROOT_READMES.items():
        fpath = ROOT_DIR / fname
        if not fpath.exists():
            errors.append(f"Missing root README file: {fname}")
            continue
        
        content = fpath.read_text(encoding="utf-8")
        if len(content.strip()) < 1000:
            errors.append(f"Root README {fname} is too short ({len(content)} bytes)")
            
        # Check for forbidden draft placeholders
        for pattern in FORBIDDEN_PLACEHOLDER_PATTERNS:
            if pattern.search(content):
                errors.append(f"Forbidden draft placeholder matching '{pattern.pattern}' found in {fname}")
                
        # Check cross-links to other READMEs
        for other_lang, other_fname in ROOT_READMES.items():
            if other_fname not in content and other_fname != fname:
                errors.append(f"{fname} lacks link or reference to {other_fname}")
                
        # Check official website link
        if "https://mrthugh.github.io/parsikit-website/" not in content:
            errors.append(f"{fname} lacks official website link 'https://mrthugh.github.io/parsikit-website/'")
            
        # Check version 3.3.1
        if "3.3.1" not in content:
            errors.append(f"{fname} lacks version 3.3.1 reference")
            
    return errors

def check_doc_coverage():
    errors = []
    print("--> Checking 4-language documentation page coverage...")
    docs_dir = ROOT_DIR / "docs"
    
    for lang in LANGUAGES:
        lang_dir = docs_dir / lang
        if not lang_dir.exists():
            errors.append(f"Missing documentation directory: docs/{lang}")
            continue
            
        for page in CANONICAL_DOC_PAGES:
            page_path = lang_dir / page
            if not page_path.exists():
                errors.append(f"Missing documentation page: docs/{lang}/{page}")
                continue
                
            content = page_path.read_text(encoding="utf-8")
            if len(content.strip()) < 150:
                errors.append(f"Documentation page too short: docs/{lang}/{page} ({len(content)} bytes)")
                
            for pattern in FORBIDDEN_PLACEHOLDER_PATTERNS:
                if pattern.search(content):
                    errors.append(f"Forbidden draft placeholder matching '{pattern.pattern}' found in docs/{lang}/{page}")
                    
            # Script-specific validation
            if lang == "tg":
                # Check for Cyrillic characters
                if not re.search(r"[\u0400-\u04FF]", content):
                    errors.append(f"docs/tg/{page} has no Cyrillic text! Must be in standard Tajik Cyrillic.")
            elif lang in ("fa", "fa-AF"):
                # Check for Arabic/Persian characters
                if not re.search(r"[\u0600-\u06FF]", content):
                    errors.append(f"docs/{lang}/{page} has no Persian/Arabic characters!")
                    
    return errors

def check_internal_markdown_links():
    errors = []
    print("--> Validating all internal Markdown links...")
    md_files = list(ROOT_DIR.glob("*.md")) + list((ROOT_DIR / "docs").rglob("*.md"))
    link_pattern = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
    checked_count = 0
    
    for f in md_files:
        content = f.read_text(encoding="utf-8")
        for m in link_pattern.finditer(content):
            target = m.group(2).strip()
            # Ignore web links and email
            if target.startswith(("http://", "https://", "mailto:", "#", "tel:")):
                continue
                
            # Strip anchors and query params
            clean_target = target.split("#")[0].split("?")[0]
            if not clean_target:
                continue
                
            resolved = (f.parent / clean_target).resolve()
            checked_count += 1
            if not resolved.exists():
                errors.append(f"Broken link in {f.relative_to(ROOT_DIR)}: [{m.group(1)}]({target}) -> {clean_target} not found")
                
    print(f"    Verified {checked_count} internal Markdown links.")
    return errors

def validate_all():
    all_errors = []
    all_errors.extend(check_root_readmes())
    all_errors.extend(check_doc_coverage())
    all_errors.extend(check_internal_markdown_links())
    
    if all_errors:
        print("\n❌ DOCUMENTATION VALIDATION FAILED WITH ERRORS:")
        for err in all_errors:
            print(f"  - {err}")
        return False
        
    print("\n✅ ALL FOUR-LANGUAGE DOCUMENTATION CHECKS PASSED PERFECTLY!")
    print(f"  - 4 Root READMEs verified ({', '.join(ROOT_READMES.values())})")
    print(f"  - 4 Language editions verified (en, fa, fa-AF, tg)")
    print(f"  - Total {len(CANONICAL_DOC_PAGES) * 4} localized documentation pages verified (100% coverage)")
    print("  - Zero broken internal Markdown links detected.")
    return True

def validate():
    return validate_all()

validate_all_docs = validate_all

if __name__ == "__main__":
    success = validate()
    sys.exit(0 if success else 1)
