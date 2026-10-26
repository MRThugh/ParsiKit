const http = require('http');
const fs = require('fs');
const path = require('path');
const { execFile } = require('child_process');

const PORT = 3000;

function runPython(code, res) {
  execFile('python3', ['-c', code], { timeout: 5000 }, (err, stdout, stderr) => {
    if (err) {
      res.writeHead(500, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: stderr || err.message }));
      return;
    }
    try {
      const data = JSON.parse(stdout.trim());
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify(data));
    } catch {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ result: stdout.trim() }));
    }
  });
}

const server = http.createServer((req, res) => {
  const parsedUrl = new URL(req.url, `http://${req.headers.host || 'localhost'}`);
  const pathname = parsedUrl.pathname;

  // API Endpoints
  if (req.method === 'POST' && pathname === '/api/eval') {
    let body = '';
    req.on('data', chunk => { body += chunk; });
    req.on('end', () => {
      try {
        const { action, input } = JSON.parse(body);
        let pyScript = '';

        if (action === 'national_code') {
          pyScript = `
import json, parsikit
code = """${input.replace(/"/g, '\\"')}"""
valid = parsikit.is_valid_national_code(code)
loc = parsikit.detect_national_code_location(code) if valid else None
fmt = parsikit.format_national_code(code) if valid else code
masked = parsikit.mask_national_code(code)
print(json.dumps({
    "valid": valid,
    "formatted": fmt,
    "masked": masked,
    "location": loc
}))
`;
        } else if (action === 'mobile') {
          pyScript = `
import json, parsikit
mob = """${input.replace(/"/g, '\\"')}"""
valid = parsikit.is_valid_mobile(mob)
nat = parsikit.normalize_mobile(mob, "0") if valid else mob
intl = parsikit.normalize_mobile(mob, "+98") if valid else mob
op = parsikit.detect_mobile_operator(mob) if valid else None
masked = parsikit.mask_mobile(mob)
print(json.dumps({
    "valid": valid,
    "national": nat,
    "international": intl,
    "operator": op,
    "masked": masked
}))
`;
        } else if (action === 'card') {
          pyScript = `
import json, parsikit
card = """${input.replace(/"/g, '\\"')}"""
valid = parsikit.is_valid_card_number(card)
bank = parsikit.detect_bank_from_card(card) if valid else None
fmt = parsikit.format_card_number(card) if valid else card
masked = parsikit.mask_card(card)
print(json.dumps({
    "valid": valid,
    "bank": bank,
    "formatted": fmt,
    "masked": masked
}))
`;
        } else if (action === 'sheba') {
          pyScript = `
import json, parsikit
sheba = """${input.replace(/"/g, '\\"')}"""
valid = parsikit.is_valid_sheba(sheba)
bank = parsikit.detect_bank_from_sheba(sheba) if valid else None
acc = parsikit.extract_account_number_from_sheba(sheba) if valid else None
fmt = parsikit.format_sheba(sheba) if valid else sheba
print(json.dumps({
    "valid": valid,
    "bank": bank,
    "account": acc,
    "formatted": fmt
}))
`;
        } else if (action === 'text') {
          pyScript = `
import json, parsikit
t = """${input.replace(/"/g, '\\"')}"""
std = parsikit.standardize_persian(t)
reshaped = parsikit.reshape_for_graphics(std)
diag = parsikit.inspect_text(t)
slug = parsikit.slugify(t)
print(json.dumps({
    "standardized": std,
    "reshaped": reshaped,
    "diagnostics": diag,
    "slug": slug
}))
`;
        } else if (action === 'datetime') {
          pyScript = `
import json, parsikit
try:
    parts = [int(p) for p in """${input}""".split("-")]
    gy, gm, gd = parts[0], parts[1], parts[2]
    jy, jm, jd = parsikit.gregorian_to_jalali(gy, gm, gd)
    month_name = parsikit.get_jalali_month_name(jm)
    is_leap = parsikit.is_jalali_leap(jy)
    fmt = parsikit.format_jalali(jy, jm, jd)
    print(json.dumps({
        "jalali": f"{jy}/{jm:02d}/{jd:02d}",
        "month_name": month_name,
        "is_leap": is_leap,
        "formatted": fmt
    }))
except Exception as e:
    print(json.dumps({"error": str(e)}))
`;
        } else if (action === 'currency') {
          pyScript = `
import json, parsikit
try:
    num = int("""${input.replace(/,/g, '').replace(/،/g, '')}""")
    words = parsikit.number_to_words(num)
    toman_fmt = parsikit.format_currency(num, "toman", persian_digits=True)
    rial_fmt = parsikit.format_currency(parsikit.toman_to_rial(num), "rial", persian_digits=True)
    vat = parsikit.add_tax_and_toll(num)
    print(json.dumps({
        "words": words,
        "toman": toman_fmt,
        "rial": rial_fmt,
        "vat_total": vat["total"],
        "vat_tax": vat["tax"]
    }))
except Exception as e:
    print(json.dumps({"error": str(e)}))
`;
        } else {
          res.writeHead(400, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ error: "Unknown action" }));
          return;
        }

        runPython(pyScript, res);
      } catch (err) {
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: "Invalid JSON body" }));
      }
    });
    return;
  }

  // Read docs or markdown file
  if (pathname === '/api/doc') {
    const docPath = parsedUrl.searchParams.get('path') || 'docs/README.md';
    const safePath = path.normalize(docPath).replace(/^(\.\.[\/\\])+/, '');
    const fullPath = path.join(__dirname, safePath);
    if (fs.existsSync(fullPath)) {
      const content = fs.readFileSync(fullPath, 'utf-8');
      res.writeHead(200, { 'Content-Type': 'text/plain; charset=utf-8' });
      res.end(content);
    } else {
      res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
      res.end('Document not found: ' + safePath);
    }
    return;
  }

  // Serve Main Interactive UI
  res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
  res.end(`<!DOCTYPE html>
<html lang="fa" dir="rtl" id="html-root">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ParsiKit v3.3.1 — Four-Language Documentation & Interactive Hub</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
  <style>
    body { font-family: 'Vazirmatn', system-ui, -apple-system, sans-serif; }
    code, pre, .font-mono { font-family: 'JetBrains Mono', monospace; direction: ltr; text-align: left; }
    .markdown-body pre { background: #0f172a; padding: 1rem; border-radius: 0.75rem; border: 1px solid #334155; margin: 1rem 0; overflow-x: auto; }
    .markdown-body code { color: #38bdf8; font-size: 0.875rem; }
    .markdown-body pre code { color: #e2e8f0; }
    .markdown-body h1 { font-size: 1.75rem; font-weight: 800; color: #f8fafc; margin-bottom: 1rem; border-bottom: 1px solid #334155; padding-bottom: 0.5rem; }
    .markdown-body h2 { font-size: 1.35rem; font-weight: 700; color: #38bdf8; margin-top: 1.5rem; margin-bottom: 0.75rem; }
    .markdown-body h3 { font-size: 1.15rem; font-weight: 600; color: #a7f3d0; margin-top: 1.25rem; margin-bottom: 0.5rem; }
    .markdown-body p { margin-bottom: 0.75rem; line-height: 1.75; color: #cbd5e1; }
    .markdown-body ul { list-style-type: disc; margin-inline-start: 1.5rem; margin-bottom: 0.75rem; color: #cbd5e1; }
    .markdown-body ol { list-style-type: decimal; margin-inline-start: 1.5rem; margin-bottom: 0.75rem; color: #cbd5e1; }
    .markdown-body table { width: 100%; border-collapse: collapse; margin: 1rem 0; }
    .markdown-body th, .markdown-body td { border: 1px solid #334155; padding: 0.5rem 0.75rem; text-align: start; }
    .markdown-body th { background: #1e293b; color: #f1f5f9; }
    .markdown-body blockquote { border-inline-start: 4px solid #10b981; padding-inline-start: 1rem; color: #94a3b8; margin: 1rem 0; font-style: italic; }
    .markdown-body a { color: #38bdf8; text-decoration: underline; }
    .markdown-body a:hover { color: #7dd3fc; }
  </style>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen flex flex-col">
  <!-- Top Navigation Header -->
  <header class="border-b border-slate-800 bg-slate-900/90 backdrop-blur sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
      <div class="flex items-center gap-3">
        <div class="w-9 h-9 rounded-xl bg-emerald-500/20 border border-emerald-500/40 flex items-center justify-center text-emerald-400 font-bold text-lg">
          PK
        </div>
        <div>
          <div class="flex items-center gap-2">
            <span class="font-bold text-lg text-white">ParsiKit</span>
            <span class="text-xs px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400 font-mono border border-emerald-500/30">v3.3.1</span>
            <span class="text-xs px-2 py-0.5 rounded-full bg-indigo-500/20 text-indigo-400 border border-indigo-500/30">4 Languages</span>
          </div>
          <p id="header-tagline" class="text-xs text-slate-400 hidden sm:block">زیرساخت داده‌های فارسی در پایتون — علی کامرانی (MRThugh)</p>
        </div>
      </div>

      <!-- Main Tabs & Language Switcher -->
      <div class="flex items-center gap-2">
        <div class="flex items-center bg-slate-800/80 p-1 rounded-xl border border-slate-700/60">
          <button onclick="switchTab('docs')" id="btn-docs" class="px-3 py-1 rounded-lg text-xs font-medium bg-emerald-600 text-white transition">مستندات</button>
          <button onclick="switchTab('playground')" id="btn-playground" class="px-3 py-1 rounded-lg text-xs font-medium text-slate-300 hover:text-white transition">میز کار تعاملی</button>
          <button onclick="switchTab('audit')" id="btn-audit" class="px-3 py-1 rounded-lg text-xs font-medium text-slate-300 hover:text-white transition">گزارش ممیزی</button>
        </div>

        <!-- Language Selector Dropdown -->
        <div class="relative inline-block text-left">
          <select id="lang-select" onchange="changeLanguage(this.value)" class="bg-slate-800 border border-slate-700 text-slate-200 text-xs rounded-xl px-2.5 py-1.5 focus:outline-none focus:border-emerald-500 cursor-pointer">
            <option value="fa" selected>🇮🇷 فارسی (ایران)</option>
            <option value="fa-AF">🇦🇫 دری (افغانستان)</option>
            <option value="tg">🇹🇯 Тоҷикӣ (Тоҷикистон)</option>
            <option value="en">🇬🇧 English</option>
          </select>
        </div>

        <!-- External Links -->
        <a href="https://github.com/MRThugh/ParsiKit" target="_blank" rel="noopener noreferrer" class="hidden md:flex items-center gap-1.5 px-2.5 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs text-slate-300 transition border border-slate-700" title="GitHub Repository">
          <svg class="w-4 h-4 fill-current" viewBox="0 0 24 24"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/></svg>
          <span>GitHub</span>
        </a>
      </div>
    </div>
  </header>

  <!-- Metric Badges Banner -->
  <div class="border-b border-slate-800 bg-slate-900/40">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3">
      <div class="grid grid-cols-2 md:grid-cols-4 gap-2.5">
        <div class="p-2.5 rounded-xl bg-slate-900/90 border border-emerald-500/30 flex items-center gap-2.5">
          <div class="w-8 h-8 rounded-lg bg-emerald-500/10 flex items-center justify-center text-emerald-400 font-bold text-sm">✓</div>
          <div>
            <div id="m-test-title" class="text-[11px] text-slate-400">تست‌های خودکار</div>
            <div class="text-xs font-bold text-emerald-400">۱۵۷ / ۱۵۷ پاس شدند (۱۰۰٪)</div>
          </div>
        </div>
        <div class="p-2.5 rounded-xl bg-slate-900/90 border border-blue-500/30 flex items-center gap-2.5">
          <div class="w-8 h-8 rounded-lg bg-blue-500/10 flex items-center justify-center text-blue-400 font-bold text-sm">🌐</div>
          <div>
            <div id="m-lang-title" class="text-[11px] text-slate-400">زبان‌های مستندات</div>
            <div class="text-xs font-bold text-blue-400">۴ زبان (فارسی، دری، тоҷикӣ، en)</div>
          </div>
        </div>
        <div class="p-2.5 rounded-xl bg-slate-900/90 border border-amber-500/30 flex items-center gap-2.5">
          <div class="w-8 h-8 rounded-lg bg-amber-500/10 flex items-center justify-center text-amber-400 font-bold text-sm">🔗</div>
          <div>
            <div id="m-link-title" class="text-[11px] text-slate-400">لینک‌های معتبر</div>
            <div class="text-xs font-bold text-amber-400">۲۰۳ لینک تأیید شد (۰ خطا)</div>
          </div>
        </div>
        <div class="p-2.5 rounded-xl bg-slate-900/90 border border-purple-500/30 flex items-center gap-2.5">
          <div class="w-8 h-8 rounded-lg bg-purple-500/10 flex items-center justify-center text-purple-400 font-bold text-sm">🔒</div>
          <div>
            <div id="m-sec-title" class="text-[11px] text-slate-400">امنیت و پاکسازی</div>
            <div class="text-xs font-bold text-purple-400">ماسک دیتای حساس فعال</div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- TAB: DOCS (DEFAULT) -->
  <main id="tab-docs" class="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6">
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
      <!-- Sidebar Navigation -->
      <aside class="md:col-span-1 space-y-4">
        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4 sticky top-24 max-h-[calc(100vh-8rem)] overflow-y-auto space-y-3">
          <div class="flex items-center justify-between pb-2 border-b border-slate-800">
            <span id="nav-header" class="text-xs font-bold text-slate-300 uppercase tracking-wider">فهرست مستندات</span>
            <span id="current-lang-badge" class="text-[10px] px-2 py-0.5 rounded-md bg-emerald-500/20 text-emerald-400 font-mono">fa</span>
          </div>

          <div id="doc-menu" class="space-y-1 text-xs">
            <!-- Dynamically populated per language -->
          </div>
        </div>
      </aside>

      <!-- Document Content Viewer -->
      <section class="md:col-span-3 bg-slate-900 border border-slate-800 rounded-2xl p-6 sm:p-8 min-h-[600px]">
        <div class="flex items-center justify-between pb-4 border-b border-slate-800 mb-6 text-xs text-slate-400">
          <div class="flex items-center gap-2">
            <span class="text-slate-500">مسیر فایل:</span>
            <span id="doc-path-display" class="font-mono text-emerald-400 bg-slate-950 px-2.5 py-1 rounded-md border border-slate-800">docs/fa/index.md</span>
          </div>
          <div class="flex items-center gap-2">
            <button onclick="copyDocContent()" class="px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 transition flex items-center gap-1">
              <span>📋</span> <span id="btn-copy-label">کپی متن</span>
            </button>
          </div>
        </div>

        <article id="doc-render" class="markdown-body text-slate-200 leading-relaxed">
          <div class="text-center py-12 text-slate-500">در حال بارگذاری سند...</div>
        </article>
      </section>
    </div>
  </main>

  <!-- TAB: PLAYGROUND -->
  <main id="tab-playground" class="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6 hidden space-y-6">
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <!-- 1. National Code Validator -->
      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 space-y-4">
        <div class="flex items-center justify-between">
          <h3 id="card1-title" class="font-bold text-slate-200 flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
            اعتبارسنجی کد ملی ایران
          </h3>
          <span class="text-xs font-mono text-slate-400">parsikit.validators</span>
        </div>
        <div class="space-y-2">
          <label id="card1-lbl" class="text-xs text-slate-400">کد ملی ۱۰ رقمی (فارسی یا انگلیسی):</label>
          <div class="flex gap-2">
            <input id="nc-input" type="text" value="0010123458" class="flex-1 bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-sm font-mono text-white focus:outline-none focus:border-emerald-500" dir="ltr">
            <button onclick="evalNationalCode()" class="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-sm font-medium transition">بررسی</button>
          </div>
        </div>
        <div id="nc-res" class="p-3 rounded-lg bg-slate-950 border border-slate-800 text-xs font-mono space-y-1">
          <span class="text-slate-500">برای اجرای الگوریتم روی دکمه کلیک کنید.</span>
        </div>
      </div>

      <!-- 2. Mobile Number Validator -->
      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 space-y-4">
        <div class="flex items-center justify-between">
          <h3 id="card2-title" class="font-bold text-slate-200 flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-blue-400"></span>
            اعتبارسنجی و نرمال‌سازی شماره موبایل
          </h3>
          <span class="text-xs font-mono text-slate-400">parsikit.models.MobileNumber</span>
        </div>
        <div class="space-y-2">
          <label id="card2-lbl" class="text-xs text-slate-400">شماره موبایل (0912..., +989...):</label>
          <div class="flex gap-2">
            <input id="mob-input" type="text" value="+98۹۱۲۳۴۵۶۷۸۹" class="flex-1 bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-sm font-mono text-white focus:outline-none focus:border-blue-500" dir="ltr">
            <button onclick="evalMobile()" class="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-lg text-sm font-medium transition">بررسی</button>
          </div>
        </div>
        <div id="mob-res" class="p-3 rounded-lg bg-slate-950 border border-slate-800 text-xs font-mono space-y-1">
          <span class="text-slate-500">برای بررسی اپراتور و فرمت کلیک کنید.</span>
        </div>
      </div>

      <!-- 3. Bank Card & Luhn Check -->
      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 space-y-4">
        <div class="flex items-center justify-between">
          <h3 id="card3-title" class="font-bold text-slate-200 flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-purple-400"></span>
            شماره کارت بانکی (الگوریتم لان و تشخیص بانک)
          </h3>
          <span class="text-xs font-mono text-slate-400">parsikit.validators</span>
        </div>
        <div class="space-y-2">
          <label id="card3-lbl" class="text-xs text-slate-400">شماره کارت ۱۶ رقمی:</label>
          <div class="flex gap-2">
            <input id="card-input" type="text" value="6037991122334455" class="flex-1 bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-sm font-mono text-white focus:outline-none focus:border-purple-500" dir="ltr">
            <button onclick="evalCard()" class="px-4 py-2 bg-purple-600 hover:bg-purple-500 text-white rounded-lg text-sm font-medium transition">بررسی</button>
          </div>
        </div>
        <div id="card-res" class="p-3 rounded-lg bg-slate-950 border border-slate-800 text-xs font-mono space-y-1">
          <span class="text-slate-500">برای بررسی چک‌سام لان و بانک صادرکننده کلیک کنید.</span>
        </div>
      </div>

      <!-- 4. Jalali & Relative Time -->
      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 space-y-4">
        <div class="flex items-center justify-between">
          <h3 id="card4-title" class="font-bold text-slate-200 flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-amber-400"></span>
            تقویم نجومی شمسی (جلالی) و سال کبیسه
          </h3>
          <span class="text-xs font-mono text-slate-400">parsikit.datetime</span>
        </div>
        <div class="space-y-2">
          <label id="card4-lbl" class="text-xs text-slate-400">تاریخ میلادی (YYYY-MM-DD):</label>
          <div class="flex gap-2">
            <input id="date-input" type="text" value="2026-10-10" class="flex-1 bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-sm font-mono text-white focus:outline-none focus:border-amber-500" dir="ltr">
            <button onclick="evalDate()" class="px-4 py-2 bg-amber-600 hover:bg-amber-500 text-white rounded-lg text-sm font-medium transition">تبدیل</button>
          </div>
        </div>
        <div id="date-res" class="p-3 rounded-lg bg-slate-950 border border-slate-800 text-xs font-mono space-y-1">
          <span class="text-slate-500">برای تبدیل تاریخ نجومی و محاسبه کبیسه کلیک کنید.</span>
        </div>
      </div>

      <!-- 5. Numbers & Currency -->
      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 space-y-4">
        <div class="flex items-center justify-between">
          <h3 id="card5-title" class="font-bold text-slate-200 flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
            تبدیل عدد به حروف و فرمت تومان/ریال
          </h3>
          <span class="text-xs font-mono text-slate-400">parsikit.number & currency</span>
        </div>
        <div class="space-y-2">
          <label id="card5-lbl" class="text-xs text-slate-400">مبلغ به تومان:</label>
          <div class="flex gap-2">
            <input id="curr-input" type="text" value="12500000" class="flex-1 bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-sm font-mono text-white focus:outline-none focus:border-emerald-500" dir="ltr">
            <button onclick="evalCurrency()" class="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-sm font-medium transition">محاسبه</button>
          </div>
        </div>
        <div id="curr-res" class="p-3 rounded-lg bg-slate-950 border border-slate-800 text-xs font-mono space-y-1">
          <span class="text-slate-500">برای تبدیل به حروف و محاسبه ارزش افزوده کلیک کنید.</span>
        </div>
      </div>

      <!-- 6. Text Standardization & Reshaper -->
      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 space-y-4">
        <div class="flex items-center justify-between">
          <h3 id="card6-title" class="font-bold text-slate-200 flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-cyan-400"></span>
            استانداردسازی متن، نیم‌فاصله‌ها و بازآرایی گرافیکی
          </h3>
          <span class="text-xs font-mono text-slate-400">parsikit.text & reshaper</span>
        </div>
        <div class="space-y-2">
          <label id="card6-lbl" class="text-xs text-slate-400">متن ورودی (دارای حروف عربی يا نیم‌فاصله):</label>
          <div class="flex gap-2">
            <input id="text-input" type="text" value="ي كافيه كتاب ها رو برداري و بري" class="flex-1 bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-cyan-500">
            <button onclick="evalText()" class="px-4 py-2 bg-cyan-600 hover:bg-cyan-500 text-white rounded-lg text-sm font-medium transition">پردازش</button>
          </div>
        </div>
        <div id="text-res" class="p-3 rounded-lg bg-slate-950 border border-slate-800 text-xs font-mono space-y-1">
          <span class="text-slate-500">برای اصلاح حروف و آماده‌سازی گرافیک کلیک کنید.</span>
        </div>
      </div>
    </div>
  </main>

  <!-- TAB: AUDIT -->
  <main id="tab-audit" class="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6 hidden space-y-6">
    <div class="bg-slate-900 border border-slate-800 rounded-2xl p-6 sm:p-8">
      <div class="flex items-center justify-between pb-4 border-b border-slate-800 mb-6">
        <div>
          <h2 class="text-lg font-bold text-white">گزارش رسمی ممیزی نهایی (Final Release Audit Report v3.3.1)</h2>
          <p class="text-xs text-slate-400">مسیر فایل: docs/development/final-release-audit-3.3.1.md</p>
        </div>
        <span class="px-3 py-1 bg-emerald-500/20 text-emerald-400 rounded-lg text-xs font-mono border border-emerald-500/40">VERDICT: APPROVED</span>
      </div>
      <div id="audit-content" class="bg-slate-950 p-6 rounded-xl border border-slate-800 font-mono text-xs whitespace-pre-wrap text-slate-300 leading-relaxed overflow-x-auto max-h-[70vh]">
        در حال بارگذاری گزارش ممیزی نهایی...
      </div>
    </div>
  </main>

  <!-- Footer -->
  <footer class="border-t border-slate-800 bg-slate-900/60 mt-auto py-6">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-slate-400">
      <div>
        <p>ParsiKit v3.3.1 — <a href="https://github.com/MRThugh" target="_blank" class="text-emerald-400 hover:underline">Ali Kamrani (MRThugh)</a></p>
        <p class="text-[11px] text-slate-500">Official website: <a href="https://mrthugh.github.io/parsikit-website/" target="_blank" class="text-slate-400 hover:underline">mrthugh.github.io/parsikit-website</a></p>
      </div>
      <div class="flex items-center gap-4">
        <a href="https://github.com/MRThugh/ParsiKit" target="_blank" class="hover:text-emerald-400 transition">GitHub Repo</a>
        <span>•</span>
        <a href="https://github.com/MRThugh/parsikit-website" target="_blank" class="hover:text-emerald-400 transition">Website Repo</a>
        <span>•</span>
        <a href="https://pypi.org/project/parsikit/" target="_blank" class="hover:text-emerald-400 transition">PyPI Package</a>
      </div>
    </div>
  </footer>

  <script>
    let currentLang = 'fa';
    let currentDocPath = 'docs/fa/index.md';
    let rawDocContent = '';

    const I18N = {
      fa: {
        dir: 'rtl',
        tagline: 'زیرساخت داده‌های فارسی در پایتون — علی کامرانی (MRThugh)',
        btnDocs: 'مستندات',
        btnPlayground: 'میز کار تعاملی',
        btnAudit: 'گزارش ممیزی',
        navHeader: 'فهرست مستندات',
        copyLabel: 'کپی متن',
        copiedLabel: 'کپی شد!',
        categories: {
          overview: 'مقدمه و شروع',
          tutorials: 'آموزش‌های کاربردی',
          guides: 'راهنماهای تخصصی',
          api: 'مرجع کامل API',
          support: 'پشتیبانی و سوالات',
          readmes: 'فایل‌های README اصلی'
        },
        docTitles: {
          'index.md': 'صفحه اصلی مستندات',
          'installation.md': 'راهنمای نصب',
          'quickstart.md': 'شروع سریع در ۵ دقیقه',
          'tutorials/text_processing.md': 'پردازش متن و نیم‌فاصله',
          'tutorials/validation.md': 'اعتبارسنجی کد ملی و کارت',
          'tutorials/numbers_and_currency.md': 'اعداد، تومان و ریال',
          'tutorials/datetime.md': 'تقویم جلالی و زمان نسبی',
          'tutorials/models.md': 'مدل‌های دامنه شیءگرا',
          'guides/web_backends.md': 'بک‌اند وب (FastAPI و Django)',
          'guides/forms_and_security.md': 'امنیت فرم و ماسک داده',
          'guides/gui_integration.md': 'رابط گرافیکی و تصاویر',
          'api/index.md': 'فهرست ماژول‌های API',
          'api/text.md': 'ماژول متن (text)',
          'api/validators.md': 'ماژول اعتبارسنجی (validators)',
          'api/models.md': 'ماژول مدل‌ها (models)',
          'api/datetime.md': 'ماژول تاریخ (datetime)',
          'api/number_and_currency.md': 'ماژول اعداد و ارز',
          'api/reshaper.md': 'ماژول بازآرایی گرافیک (reshaper)',
          'api/cache.md': 'ماژول کش و Memoize',
          'api/dev_and_gui.md': 'ماژول Dev و GUI',
          'troubleshooting.md': 'عیب‌یابی و رفع خطا',
          'faq.md': 'سوالات متداول (FAQ)'
        }
      },
      'fa-AF': {
        dir: 'rtl',
        tagline: 'زیرساخت دیتای فارسی و دری در پایتون — علی کامرانی (MRThugh)',
        btnDocs: 'مستندات',
        btnPlayground: 'میز کار تعاملی',
        btnAudit: 'گزارش ممیزی',
        navHeader: 'فهرست رهنمودها',
        copyLabel: 'کاپی متن',
        copiedLabel: 'کاپی شد!',
        categories: {
          overview: 'مقدمه و آغاز',
          tutorials: 'رهنمودهای آموزشی',
          guides: 'رهنماهای تخصصی',
          api: 'مرجع مکمل API',
          support: 'حل مشکلات و سوالات',
          readmes: 'فایل‌های اصلی README'
        },
        docTitles: {
          'index.md': 'صفحه اصلی رهنمود',
          'installation.md': 'طریقه نصب و فعال‌سازی',
          'quickstart.md': 'آغاز سریع در ۵ دقیقه',
          'tutorials/text_processing.md': 'پروسس متن و نیم‌فاصله',
          'tutorials/validation.md': 'تصدیق اعتبار کودها و کارت',
          'tutorials/numbers_and_currency.md': 'ارقام، اسعار و حساب‌ها',
          'tutorials/datetime.md': 'تقویم هجری شمسی و زمان نسبی',
          'tutorials/models.md': 'مدل‌های دامنه شیءگرا',
          'guides/web_backends.md': 'سیستم‌های ویب (FastAPI و Django)',
          'guides/forms_and_security.md': 'امنیت فورم‌ها و دیتای شخصی',
          'guides/gui_integration.md': 'رابط گرافیکی و پروسس تصویر',
          'api/index.md': 'فهرست ماژول‌های API',
          'api/text.md': 'ماژول متن (text)',
          'api/validators.md': 'ماژول تصدیق اعتبار (validators)',
          'api/models.md': 'ماژول مدل‌ها (models)',
          'api/datetime.md': 'ماژول تقویم (datetime)',
          'api/number_and_currency.md': 'ماژول ارقام و اسعار',
          'api/reshaper.md': 'ماژول بازآرایی گرافیک (reshaper)',
          'api/cache.md': 'ماژول کش و Memoize',
          'api/dev_and_gui.md': 'ماژول Dev و GUI',
          'troubleshooting.md': 'رهنمای حل مشکلات',
          'faq.md': 'سوال‌های مکرر (FAQ)'
        }
      },
      tg: {
        dir: 'ltr',
        tagline: 'Зерсохтори додаҳои форсӣ ва тоҷикӣ дар Python — Алӣ Комронӣ (MRThugh)',
        btnDocs: 'Ҳуҷҷатгузорӣ',
        btnPlayground: 'Мизи кории амалӣ',
        btnAudit: 'Гузориши аудит',
        navHeader: 'Феҳристи ҳуҷҷатҳо',
        copyLabel: 'Нусхабардорӣ',
        copiedLabel: 'Нусха шуд!',
        categories: {
          overview: 'Муқаддима ва оғоз',
          tutorials: 'Дарсҳои омӯзишӣ',
          guides: 'Роҳнамоҳои корбурдӣ',
          api: 'Маълумотномаи API',
          support: 'Ҳалли мушкилот ва саволҳо',
          readmes: 'Файлҳои аслии README'
        },
        docTitles: {
          'index.md': 'Саҳифаи асосии ҳуҷҷатгузорӣ',
          'installation.md': 'Роҳнамои насб ва омодасозӣ',
          'quickstart.md': 'Оғози зуд дар 5 дақиқа',
          'tutorials/text_processing.md': 'Коркарди матн ва нимфосила (ZWNJ)',
          'tutorials/validation.md': 'Санҷиши рамзи миллӣ ва корт',
          'tutorials/numbers_and_currency.md': 'Ададҳо, тумон ва риёл',
          'tutorials/datetime.md': 'Тақвими ҳиҷрии шамсӣ ва вақти нисбӣ',
          'tutorials/models.md': 'Моделҳои объектгарои маълумот',
          'guides/web_backends.md': 'Системаҳои веб (FastAPI ва Django)',
          'guides/forms_and_security.md': 'Амнияти формаҳо ва ниқоббандӣ',
          'guides/gui_integration.md': 'Интерфейси графикӣ ва тасвирҳо',
          'api/index.md': 'Феҳристи модулҳои API',
          'api/text.md': 'Модули коркарди матн (text)',
          'api/validators.md': 'Модули санҷиши дурустӣ (validators)',
          'api/models.md': 'Модули моделҳо (models)',
          'api/datetime.md': 'Модули тақвим (datetime)',
          'api/number_and_currency.md': 'Модули ададҳо ва асъор',
          'api/reshaper.md': 'Модули бозсозии графикӣ (reshaper)',
          'api/cache.md': 'Модули кэш ва Memoize',
          'api/dev_and_gui.md': 'Модули Dev ва GUI',
          'troubleshooting.md': 'Роҳнамои ҳалли мушкилот',
          'faq.md': 'Саволҳои маъмул (FAQ)'
        }
      },
      en: {
        dir: 'ltr',
        tagline: 'Persian & Regional Data Infrastructure for Python — Ali Kamrani (MRThugh)',
        btnDocs: 'Documentation',
        btnPlayground: 'Interactive Playground',
        btnAudit: 'Audit Report',
        navHeader: 'Documentation Index',
        copyLabel: 'Copy Markdown',
        copiedLabel: 'Copied!',
        categories: {
          overview: 'Overview & Getting Started',
          tutorials: 'Tutorials',
          guides: 'Guides & Integration',
          api: 'API Reference',
          support: 'Troubleshooting & FAQ',
          readmes: 'Root README Files'
        },
        docTitles: {
          'index.md': 'Documentation Home',
          'installation.md': 'Installation Guide',
          'quickstart.md': 'Quickstart in 5 Minutes',
          'tutorials/text_processing.md': 'Text Processing & ZWNJ',
          'tutorials/validation.md': 'ID & Bank Card Validation',
          'tutorials/numbers_and_currency.md': 'Numbers & Currency',
          'tutorials/datetime.md': 'Jalali Calendar & Dates',
          'tutorials/models.md': 'Domain Models (OOP)',
          'guides/web_backends.md': 'Web Backends (FastAPI & Django)',
          'guides/forms_and_security.md': 'Forms & Security Best Practices',
          'guides/gui_integration.md': 'Desktop GUI & Graphics',
          'api/index.md': 'API Index & Overview',
          'api/text.md': 'Text Processing API',
          'api/validators.md': 'Validators API',
          'api/models.md': 'Models API',
          'api/datetime.md': 'Datetime API',
          'api/number_and_currency.md': 'Number & Currency API',
          'api/reshaper.md': 'Reshaper API',
          'api/cache.md': 'Cache & Memoize API',
          'api/dev_and_gui.md': 'Dev & GUI API',
          'troubleshooting.md': 'Troubleshooting Guide',
          'faq.md': 'Frequently Asked Questions (FAQ)'
        }
      }
    };

    function changeLanguage(lang) {
      currentLang = lang;
      const conf = I18N[lang];
      const htmlRoot = document.getElementById('html-root');
      htmlRoot.setAttribute('lang', lang);
      htmlRoot.setAttribute('dir', conf.dir);

      document.getElementById('header-tagline').innerText = conf.tagline;
      document.getElementById('btn-docs').innerText = conf.btnDocs;
      document.getElementById('btn-playground').innerText = conf.btnPlayground;
      document.getElementById('btn-audit').innerText = conf.btnAudit;
      document.getElementById('nav-header').innerText = conf.navHeader;
      document.getElementById('btn-copy-label').innerText = conf.copyLabel;
      document.getElementById('current-lang-badge').innerText = lang;

      renderSidebarMenu();
      loadDoc(\`docs/\${lang}/index.md\`);
    }

    function renderSidebarMenu() {
      const conf = I18N[currentLang];
      const menu = document.getElementById('doc-menu');
      
      const sections = [
        {
          cat: conf.categories.overview,
          pages: ['index.md', 'installation.md', 'quickstart.md']
        },
        {
          cat: conf.categories.tutorials,
          pages: ['tutorials/text_processing.md', 'tutorials/validation.md', 'tutorials/numbers_and_currency.md', 'tutorials/datetime.md', 'tutorials/models.md']
        },
        {
          cat: conf.categories.guides,
          pages: ['guides/web_backends.md', 'guides/forms_and_security.md', 'guides/gui_integration.md']
        },
        {
          cat: conf.categories.api,
          pages: ['api/index.md', 'api/text.md', 'api/validators.md', 'api/models.md', 'api/datetime.md', 'api/number_and_currency.md', 'api/reshaper.md', 'api/cache.md', 'api/dev_and_gui.md']
        },
        {
          cat: conf.categories.support,
          pages: ['troubleshooting.md', 'faq.md']
        }
      ];

      let html = '';
      sections.forEach(sec => {
        html += \`<div class="pt-2 text-[11px] font-semibold text-slate-400 uppercase tracking-wider">\${sec.cat}</div>\`;
        sec.pages.forEach(p => {
          const title = conf.docTitles[p] || p;
          const fullPath = \`docs/\${currentLang}/\${p}\`;
          const activeClass = (fullPath === currentDocPath) ? 'bg-emerald-600 text-white font-medium' : 'text-slate-300 hover:bg-slate-800 hover:text-white';
          html += \`<button onclick="loadDoc('\${fullPath}')" class="w-full text-start px-2.5 py-1.5 rounded-lg transition \${activeClass}">\${title}</button>\`;
        });
      });

      // Add README Links section
      html += \`<div class="pt-3 text-[11px] font-semibold text-slate-400 uppercase tracking-wider">\${conf.categories.readmes}</div>\`;
      const readmes = [
        { title: 'README.md (English)', path: 'README.md' },
        { title: 'README.fa.md (فارسی)', path: 'README.fa.md' },
        { title: 'README.fa-AF.md (دری)', path: 'README.fa-AF.md' },
        { title: 'README.tg.md (Тоҷикӣ)', path: 'README.tg.md' },
        { title: 'docs/README.md (Hub)', path: 'docs/README.md' }
      ];
      readmes.forEach(r => {
        const activeClass = (r.path === currentDocPath) ? 'bg-emerald-600 text-white font-medium' : 'text-slate-300 hover:bg-slate-800 hover:text-white';
        html += \`<button onclick="loadDoc('\${r.path}')" class="w-full text-start px-2.5 py-1.5 rounded-lg font-mono text-[11px] transition \${activeClass}">\${r.title}</button>\`;
      });

      menu.innerHTML = html;
    }

    async function loadDoc(docPath) {
      currentDocPath = docPath;
      document.getElementById('doc-path-display').innerText = docPath;
      renderSidebarMenu();

      try {
        const res = await fetch('/api/doc?path=' + encodeURIComponent(docPath));
        if (!res.ok) throw new Error('File not found');
        rawDocContent = await res.text();
        
        // Render Markdown using marked.js
        const renderedHtml = marked.parse(rawDocContent);
        document.getElementById('doc-render').innerHTML = renderedHtml;
      } catch (err) {
        document.getElementById('doc-render').innerHTML = \`<div class="text-rose-400 p-4 bg-rose-950/30 rounded-xl border border-rose-800">Error loading document: \${err.message}</div>\`;
      }
    }

    function copyDocContent() {
      if (!rawDocContent) return;
      navigator.clipboard.writeText(rawDocContent).then(() => {
        const btn = document.getElementById('btn-copy-label');
        const orig = btn.innerText;
        btn.innerText = I18N[currentLang].copiedLabel;
        setTimeout(() => { btn.innerText = orig; }, 2000);
      });
    }

    function switchTab(tab) {
      ['docs', 'playground', 'audit'].forEach(t => {
        document.getElementById('tab-' + t).classList.add('hidden');
        document.getElementById('btn-' + t).className = 'px-3 py-1 rounded-lg text-xs font-medium text-slate-300 hover:text-white transition';
      });
      document.getElementById('tab-' + tab).classList.remove('hidden');
      document.getElementById('btn-' + tab).className = 'px-3 py-1 rounded-lg text-xs font-medium bg-emerald-600 text-white transition';

      if (tab === 'audit') loadAudit();
    }

    async function loadAudit() {
      try {
        const res = await fetch('/api/doc?path=docs/development/final-release-audit-3.3.1.md');
        const text = await res.text();
        document.getElementById('audit-content').innerText = text;
      } catch (err) {
        document.getElementById('audit-content').innerText = 'Error loading audit report: ' + err.message;
      }
    }

    // Playground Interactive API Calls
    async function apiCall(action, input) {
      const res = await fetch('/api/eval', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action, input })
      });
      return await res.json();
    }

    async function evalNationalCode() {
      const val = document.getElementById('nc-input').value;
      const resBox = document.getElementById('nc-res');
      resBox.innerHTML = '<span class="text-slate-400">Processing...</span>';
      const data = await apiCall('national_code', val);
      resBox.innerHTML = \`
<div>صحت چک‌سام: \${data.valid ? '<span class="text-emerald-400 font-bold">معتبر (Valid ✓)</span>' : '<span class="text-rose-400 font-bold">نامعتبر (Invalid ✗)</span>'}</div>
<div>فرمت استاندارد: <span class="text-cyan-300">\${data.formatted}</span></div>
<div>ماسک امنیتی: <span class="text-amber-300">\${data.masked}</span></div>
\${data.location ? '<div>محل صدور: <span class="text-emerald-300">' + data.location.province + ' (' + data.location.city + ')</span></div>' : ''}
\`;
    }

    async function evalMobile() {
      const val = document.getElementById('mob-input').value;
      const resBox = document.getElementById('mob-res');
      resBox.innerHTML = '<span class="text-slate-400">Processing...</span>';
      const data = await apiCall('mobile', val);
      resBox.innerHTML = \`
<div>صحت شماره: \${data.valid ? '<span class="text-emerald-400 font-bold">معتبر (Valid ✓)</span>' : '<span class="text-rose-400 font-bold">نامعتبر (Invalid ✗)</span>'}</div>
<div>فرمت ملی: <span class="text-cyan-300">\${data.national}</span></div>
<div>فرمت بین‌المللی: <span class="text-cyan-300">\${data.international}</span></div>
<div>اپراتور: <span class="text-amber-300">\${data.operator || 'نامشخص'}</span></div>
<div>ماسک امنیتی: <span class="text-purple-300">\${data.masked}</span></div>
\`;
    }

    async function evalCard() {
      const val = document.getElementById('card-input').value;
      const resBox = document.getElementById('card-res');
      resBox.innerHTML = '<span class="text-slate-400">Processing...</span>';
      const data = await apiCall('card', val);
      resBox.innerHTML = \`
<div>صحت لان (Luhn): \${data.valid ? '<span class="text-emerald-400 font-bold">معتبر (Valid ✓)</span>' : '<span class="text-rose-400 font-bold">نامعتبر (Invalid ✗)</span>'}</div>
<div>بانک صادرکننده: <span class="text-cyan-300">\${data.bank ? data.bank.name : 'نامشخص'}</span></div>
<div>فرمت ۴ تایی: <span class="text-amber-300">\${data.formatted}</span></div>
<div>ماسک PII: <span class="text-purple-300">\${data.masked}</span></div>
\`;
    }

    async function evalDate() {
      const val = document.getElementById('date-input').value;
      const resBox = document.getElementById('date-res');
      resBox.innerHTML = '<span class="text-slate-400">Processing...</span>';
      const data = await apiCall('datetime', val);
      if (data.error) {
        resBox.innerHTML = '<span class="text-rose-400">' + data.error + '</span>';
        return;
      }
      resBox.innerHTML = \`
<div>تاریخ شمسی: <span class="text-emerald-400 font-bold">\${data.jalali}</span> (\${data.month_name})</div>
<div>سال کبیسه نجومی: \${data.is_leap ? '<span class="text-cyan-300 font-bold">بله (Leap Year)</span>' : '<span class="text-slate-400">خیر (Normal Year)</span>'}</div>
<div>نمایش فرمت‌شده: <span class="text-amber-300">\${data.formatted}</span></div>
\`;
    }

    async function evalCurrency() {
      const val = document.getElementById('curr-input').value;
      const resBox = document.getElementById('curr-res');
      resBox.innerHTML = '<span class="text-slate-400">Processing...</span>';
      const data = await apiCall('currency', val);
      if (data.error) {
        resBox.innerHTML = '<span class="text-rose-400">' + data.error + '</span>';
        return;
      }
      resBox.innerHTML = \`
<div>حروف: <span class="text-emerald-300 font-bold">\${data.words} تومان</span></div>
<div>فرمت تومان: <span class="text-cyan-300">\${data.toman}</span></div>
<div>معادل ریال: <span class="text-slate-300">\${data.rial}</span></div>
<div>مبلغ با مالیات (۱۰٪): <span class="text-amber-300 font-bold">\${data.vat_total.toLocaleString()} تومان</span> (مالیات: \${data.vat_tax.toLocaleString()})</div>
\`;
    }

    async function evalText() {
      const val = document.getElementById('text-input').value;
      const resBox = document.getElementById('text-res');
      resBox.innerHTML = '<span class="text-slate-400">Processing...</span>';
      const data = await apiCall('text', val);
      resBox.innerHTML = \`
<div>متن استانداردشده: <span class="text-emerald-300 font-bold">\${data.standardized}</span></div>
<div>اسلاگ سئو: <span class="text-cyan-300 font-mono">\${data.slug}</span></div>
<div>بازآرایی برای موتور گرافیک: <span class="text-purple-300 font-bold">\${data.reshaped}</span></div>
<div>تحلیل ساختار: حروف عربی: \${data.diagnostics.has_arabic_chars} | نیم‌فاصله: \${data.diagnostics.has_zwnj_issues} | ارقام انگلیسی: \${data.diagnostics.has_english_digits}</div>
\`;
    }

    // Initialize UI on page load
    changeLanguage('fa');
    evalNationalCode();
    evalMobile();
    evalCard();
    evalDate();
    evalCurrency();
    evalText();
  </script>
</body>
</html>
`);
});

server.listen(PORT, '0.0.0.0', () => {
  console.log(`ParsiKit Four-Language Hub running at http://0.0.0.0:${PORT}`);
});
