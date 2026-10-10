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
        const { action, input, options } = JSON.parse(body);
        let pyScript = '';

        if (action === 'national_code') {
          pyScript = `
import json, parsikit
from parsikit.exceptions import InvalidNationalCodeError
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

  // Read docs or audit
  if (pathname === '/api/doc') {
    const docPath = parsedUrl.searchParams.get('path') || 'docs/README.md';
    const safePath = path.normalize(docPath).replace(/^(\.\.[\/\\])+/, '');
    const fullPath = path.join(__dirname, safePath);
    if (fs.existsSync(fullPath)) {
      const content = fs.readFileSync(fullPath, 'utf-8');
      res.writeHead(200, { 'Content-Type': 'text/plain; charset=utf-8' });
      res.end(content);
    } else {
      res.writeHead(404, { 'Content-Type': 'text/plain' });
      res.end('Not found');
    }
    return;
  }

  // Serve Main Interactive UI
  res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
  res.end(`<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ParsiKit v3.3.1 — Interactive Documentation & Verification Hub</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
  <style>
    body { font-family: 'Vazirmatn', system-ui, sans-serif; }
    code, pre, .font-mono { font-family: 'JetBrains Mono', monospace; direction: ltr; text-align: left; }
  </style>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen">
  <!-- Top Navigation -->
  <header class="border-b border-slate-800 bg-slate-900/80 backdrop-blur sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
      <div class="flex items-center gap-3">
        <div class="w-9 h-9 rounded-xl bg-emerald-500/20 border border-emerald-500/40 flex items-center justify-center text-emerald-400 font-bold text-lg">
          PK
        </div>
        <div>
          <div class="flex items-center gap-2">
            <span class="font-bold text-lg text-white">ParsiKit</span>
            <span class="text-xs px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400 font-mono border border-emerald-500/30">v3.3.1</span>
            <span class="text-xs px-2 py-0.5 rounded-full bg-blue-500/20 text-blue-400 border border-blue-500/30">Release Ready</span>
          </div>
          <p class="text-xs text-slate-400 hidden sm:block">زیرساخت داده‌های فارسی در پایتون — علی کامرانی (MRThugh)</p>
        </div>
      </div>
      <div class="flex items-center gap-2">
        <button onclick="switchTab('playground')" id="btn-playground" class="px-3 py-1.5 rounded-lg text-sm font-medium bg-emerald-600 text-white transition">میز کار تعاملی</button>
        <button onclick="switchTab('audit')" id="btn-audit" class="px-3 py-1.5 rounded-lg text-sm font-medium bg-slate-800 text-slate-300 hover:bg-slate-700 transition">گزارش ممیزی (Audit)</button>
        <button onclick="switchTab('docs')" id="btn-docs" class="px-3 py-1.5 rounded-lg text-sm font-medium bg-slate-800 text-slate-300 hover:bg-slate-700 transition">مستندات</button>
      </div>
    </div>
  </header>

  <!-- Release Metric Banners -->
  <div class="border-b border-slate-800 bg-slate-900/40">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
      <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
        <div class="p-3 rounded-xl bg-slate-900/90 border border-emerald-500/30 flex items-center gap-3">
          <div class="w-10 h-10 rounded-lg bg-emerald-500/10 flex items-center justify-center text-emerald-400 font-bold">✓</div>
          <div>
            <div class="text-xs text-slate-400">تست‌های خودکار</div>
            <div class="text-sm font-bold text-emerald-400">۹۵ / ۹۵ پاس شدند (۱۰۰٪)</div>
          </div>
        </div>
        <div class="p-3 rounded-xl bg-slate-900/90 border border-blue-500/30 flex items-center gap-3">
          <div class="w-10 h-10 rounded-lg bg-blue-500/10 flex items-center justify-center text-blue-400 font-bold">📦</div>
          <div>
            <div class="text-xs text-slate-400">پکیج Wheel و Sdist</div>
            <div class="text-sm font-bold text-blue-400">ساخته و آزمایش شد</div>
          </div>
        </div>
        <div class="p-3 rounded-xl bg-slate-900/90 border border-amber-500/30 flex items-center gap-3">
          <div class="w-10 h-10 rounded-lg bg-amber-500/10 flex items-center justify-center text-amber-400 font-bold">🔗</div>
          <div>
            <div class="text-xs text-slate-400">لینک‌های مستندات</div>
            <div class="text-sm font-bold text-amber-400">۰ لینک شکسته (۷۴ بررسی شد)</div>
          </div>
        </div>
        <div class="p-3 rounded-xl bg-slate-900/90 border border-purple-500/30 flex items-center gap-3">
          <div class="w-10 h-10 rounded-lg bg-purple-500/10 flex items-center justify-center text-purple-400 font-bold">🔒</div>
          <div>
            <div class="text-xs text-slate-400">بهداشت امنیتی</div>
            <div class="text-sm font-bold text-purple-400">فاقد کلید، ماسک داده فعال</div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- TAB: PLAYGROUND -->
  <main id="tab-playground" class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <!-- 1. National Code Validator -->
      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 space-y-4">
        <div class="flex items-center justify-between">
          <h3 class="font-bold text-slate-200 flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
            اعتبارسنجی کد ملی ایران
          </h3>
          <span class="text-xs font-mono text-slate-400">parsikit.validators</span>
        </div>
        <div class="space-y-2">
          <label class="text-xs text-slate-400">کد ملی ۱۰ رقمی (فارسی یا انگلیسی):</label>
          <div class="flex gap-2">
            <input id="nc-input" type="text" value="0010123458" class="flex-1 bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-sm font-mono text-white focus:outline-none focus:border-emerald-500" dir="ltr">
            <button onclick="evalNationalCode()" class="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-sm font-medium transition">بررسی</button>
          </div>
        </div>
        <div id="nc-res" class="p-3 rounded-lg bg-slate-950 border border-slate-800 text-xs font-mono space-y-1">
          <span class="text-slate-500">برای اجرای الگوریتم روی دکمه «بررسی» کلیک کنید.</span>
        </div>
      </div>

      <!-- 2. Mobile Number Validator -->
      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 space-y-4">
        <div class="flex items-center justify-between">
          <h3 class="font-bold text-slate-200 flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-blue-400"></span>
            اعتبارسنجی و نرمال‌سازی شماره موبایل
          </h3>
          <span class="text-xs font-mono text-slate-400">parsikit.models.MobileNumber</span>
        </div>
        <div class="space-y-2">
          <label class="text-xs text-slate-400">شماره موبایل (0912..., +989...):</label>
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
          <h3 class="font-bold text-slate-200 flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-purple-400"></span>
            شماره کارت بانکی (الگوریتم لان و تشخیص بانک)
          </h3>
          <span class="text-xs font-mono text-slate-400">parsikit.validators</span>
        </div>
        <div class="space-y-2">
          <label class="text-xs text-slate-400">شماره کارت ۱۶ رقمی:</label>
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
          <h3 class="font-bold text-slate-200 flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-amber-400"></span>
            تقویم نجومی شمسی (جلالی) و سال کبیسه
          </h3>
          <span class="text-xs font-mono text-slate-400">parsikit.datetime</span>
        </div>
        <div class="space-y-2">
          <label class="text-xs text-slate-400">تاریخ میلادی (YYYY-MM-DD):</label>
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
          <h3 class="font-bold text-slate-200 flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
            تبدیل عدد به حروف و فرمت تومان/ریال
          </h3>
          <span class="text-xs font-mono text-slate-400">parsikit.number & currency</span>
        </div>
        <div class="space-y-2">
          <label class="text-xs text-slate-400">مبلغ به تومان:</label>
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
          <h3 class="font-bold text-slate-200 flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-cyan-400"></span>
            استانداردسازی متن، نیم‌فاصله‌ها و بازآرایی گرافیکی
          </h3>
          <span class="text-xs font-mono text-slate-400">parsikit.text & reshaper</span>
        </div>
        <div class="space-y-2">
          <label class="text-xs text-slate-400">متن ورودی (دارای حروف عربی يا نیم‌فاصله):</label>
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
  <main id="tab-audit" class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 hidden space-y-6">
    <div class="bg-slate-900 border border-slate-800 rounded-2xl p-6">
      <div class="flex items-center justify-between pb-4 border-b border-slate-800 mb-6">
        <div>
          <h2 class="text-xl font-bold text-white">گزارش رسمی ممیزی نهایی (Final Release Audit Report v3.3.1)</h2>
          <p class="text-sm text-slate-400">مسیر فایل: docs/development/final-release-audit-3.3.1.md</p>
        </div>
        <span class="px-3 py-1 bg-emerald-500/20 text-emerald-400 rounded-lg text-xs font-mono border border-emerald-500/40">VERDICT: APPROVED</span>
      </div>
      <div id="audit-content" class="bg-slate-950 p-6 rounded-xl border border-slate-800 font-mono text-xs whitespace-pre-wrap text-slate-300 leading-relaxed overflow-x-auto max-h-[70vh]">
        در حال بارگذاری گزارش ممیزی نهایی...
      </div>
    </div>
  </main>

  <!-- TAB: DOCS -->
  <main id="tab-docs" class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 hidden space-y-6">
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4 space-y-2">
        <h4 class="font-bold text-slate-300 text-xs uppercase tracking-wider mb-2">فهرست مستندات</h4>
        <button onclick="loadDoc('docs/README.md')" class="w-full text-right px-3 py-2 rounded-lg text-xs hover:bg-slate-800 text-slate-300">هاب مستندات (README)</button>
        <button onclick="loadDoc('docs/fa/index.md')" class="w-full text-right px-3 py-2 rounded-lg text-xs hover:bg-slate-800 text-slate-300">مستندات فارسی (fa/index.md)</button>
        <button onclick="loadDoc('docs/en/index.md')" class="w-full text-right px-3 py-2 rounded-lg text-xs hover:bg-slate-800 text-slate-300">English Documentation</button>
        <button onclick="loadDoc('docs/fa/api/index.md')" class="w-full text-right px-3 py-2 rounded-lg text-xs hover:bg-slate-800 text-slate-300">مرجع API فارسی</button>
        <button onclick="loadDoc('docs/en/api/index.md')" class="w-full text-right px-3 py-2 rounded-lg text-xs hover:bg-slate-800 text-slate-300">English API Reference</button>
        <button onclick="loadDoc('docs/fa/api/cache.md')" class="w-full text-right px-3 py-2 rounded-lg text-xs hover:bg-slate-800 text-slate-300">کش و Memoize (جدید)</button>
        <button onclick="loadDoc('docs/fa/api/reshaper.md')" class="w-full text-right px-3 py-2 rounded-lg text-xs hover:bg-slate-800 text-slate-300">بازآرایی گرافیکی (جدید)</button>
      </div>
      <div class="md:col-span-3 bg-slate-900 border border-slate-800 rounded-2xl p-6">
        <div id="doc-view" class="font-mono text-xs whitespace-pre-wrap text-slate-300 leading-relaxed overflow-x-auto max-h-[75vh]">
          یک سند را از منوی سمت راست انتخاب کنید.
        </div>
      </div>
    </div>
  </main>

  <script>
    function switchTab(tab) {
      ['playground', 'audit', 'docs'].forEach(t => {
        document.getElementById('tab-' + t).classList.add('hidden');
        document.getElementById('btn-' + t).className = 'px-3 py-1.5 rounded-lg text-sm font-medium bg-slate-800 text-slate-300 hover:bg-slate-700 transition';
      });
      document.getElementById('tab-' + tab).classList.remove('hidden');
      document.getElementById('btn-' + tab).className = 'px-3 py-1.5 rounded-lg text-sm font-medium bg-emerald-600 text-white transition';

      if (tab === 'audit') loadAudit();
      if (tab === 'docs') loadDoc('docs/fa/index.md');
    }

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
      resBox.innerHTML = '<span class="text-slate-400">در حال پردازش...</span>';
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
      resBox.innerHTML = '<span class="text-slate-400">در حال پردازش...</span>';
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
      resBox.innerHTML = '<span class="text-slate-400">در حال پردازش...</span>';
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
      resBox.innerHTML = '<span class="text-slate-400">در حال پردازش...</span>';
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
      resBox.innerHTML = '<span class="text-slate-400">در حال پردازش...</span>';
      const data = await apiCall('currency', val);
      if (data.error) {
        resBox.innerHTML = '<span class="text-rose-400">' + data.error + '</span>';
        return;
      }
      resBox.innerHTML = \`
<div>حروف فارسی: <span class="text-emerald-300 font-bold">\${data.words} تومان</span></div>
<div>فرمت تومان: <span class="text-cyan-300">\${data.toman}</span></div>
<div>معادل ریال: <span class="text-slate-300">\${data.rial}</span></div>
<div>مبلغ با مالیات (۱۰٪): <span class="text-amber-300 font-bold">\${data.vat_total.toLocaleString()} تومان</span> (مالیات: \${data.vat_tax.toLocaleString()})</div>
\`;
    }

    async function evalText() {
      const val = document.getElementById('text-input').value;
      const resBox = document.getElementById('text-res');
      resBox.innerHTML = '<span class="text-slate-400">در حال پردازش...</span>';
      const data = await apiCall('text', val);
      resBox.innerHTML = \`
<div>متن استانداردشده: <span class="text-emerald-300 font-bold">\${data.standardized}</span></div>
<div>اسلاگ سئو: <span class="text-cyan-300 font-mono">\${data.slug}</span></div>
<div>بازآرایی برای موتور گرافیک (Shaped): <span class="text-purple-300 font-bold">\${data.reshaped}</span></div>
<div>تحلیل ساختار: حروف عربی: \${data.diagnostics.has_arabic_chars} | نیم‌فاصله: \${data.diagnostics.has_zwnj_issues} | ارقام انگلیسی: \${data.diagnostics.has_english_digits}</div>
\`;
    }

    async function loadAudit() {
      const res = await fetch('/api/doc?path=docs/development/final-release-audit-3.3.1.md');
      const text = await res.text();
      document.getElementById('audit-content').innerText = text;
    }

    async function loadDoc(docPath) {
      const res = await fetch('/api/doc?path=' + docPath);
      const text = await res.text();
      document.getElementById('doc-view').innerText = text;
    }

    // Run initial evaluations
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
  console.log(`ParsiKit Documentation & Playground Hub running at http://0.0.0.0:${PORT}`);
});
