# مرجع عمومی توابع و ماژول‌های ParsiKit (API Reference)

فهرست کامل تمامی ماژول‌ها و توابع عمومی موجود در **ParsiKit v3.3.1**:

| ماژول | شرح وظیفه | رهنمود تفصیلی |
|---|---|---|
| `parsikit.text` | معیارسازی حروف، تنظیم نیم‌فاصله‌ها، حذف اعراب، استخراج اطلاعات و پنهان‌سازی | [مرجع ماژول متن](text.md) |
| `parsikit.validators` | اعتبارسنجی کود ملی، شماره مبایل، تلفون ثابت، کارت‌های بانکی، شبا، قبوض و نمبر پلیت | [مرجع ماژول اعتبارسنجی](validators.md) |
| `parsikit.models` | مودل‌های دامنه‌ی شی‌گرا با پشتیبانی مستقیم از Pydantic v2 | [مرجع مودل‌های شی‌گرا](models.md) |
| `parsikit.datetime` | تبدیل تاریخ‌های هجری شمسی و میلادی، سال کبیسه، نام ماه‌ها و زمان نسبی | [مرجع ماژول تاریخ و زمان](datetime.md) |
| `parsikit.number` و `parsikit.currency` | تبدیل ارقام، نوشتن عدد به حروف، تبدیلات مالی، مالیات و محاسبه‌ی اقساط | [مرجع ارقام و مالی](number_and_currency.md) |
| `parsikit.dev` و `parsikit.gui` | تراز دیداری، عیب‌یابی متن، گزارش دسته‌ای و اتصال به واسط‌های گرافیکی | [مرجع عیب‌یابی و گرافیک](dev_and_gui.md) |
| `parsikit.reshaper` | بازآرایی و اتصال حروف برای موتورهای گرافیکی و رسم تصویر | [مرجع بازآرایی حروف](reshaper.md) |
| `parsikit.cache` | زیرساخت کش (Cache) پرشتاب و مصئون در محیط چندریسمانی | [مرجع کش و بهینه‌سازی](cache.md) |
| `parsikit.config` و `parsikit.exceptions` | تنظیمات عمومی و استثنائات ساختاریافته | [تنظیمات و استثنائات](#تنظیمات-عمومی-و-استثنائات) |

---

## تنظیمات عمومی و استثنائات

### تنظیمات عمومی (`parsikit.config`)
- `default_tax_rate: float`: نرخ پیش‌فرض مالیات (پیش‌فرض: `0.10`).
- `default_currency: str`: واحد پولی پیش‌فرض سیستم، `"toman"` یا `"rial"` (پیش‌فرض: `"toman"`).
- `enable_cache: bool`: فعال‌سازی کش LRU برای محاسبات پرهزینه (پیش‌فرض: `True`).

### صنف‌های استثنا (`parsikit.exceptions`)
تمامی خطاهای اختصاصی از `ParsiKitError` و `ValidationError` (زیرصنف `ValueError`) ارث‌بری دارند:
- `InvalidNationalCodeError`
- `InvalidMobileError`
- `InvalidCardNumberError`
- `InvalidShebaError`
- `InvalidPostalCodeError`
- `InvalidPlateError`
- `InvalidBillError`
