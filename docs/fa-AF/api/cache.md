# مرجع ماژول کش (`parsikit.cache`)

زیرساخت حافظه‌ی موقت (کاشه / Cache) پرشتاب و مصئون در برابر ریسمان‌های همزمان (Thread-safe) جهت بهینه‌سازی محاسبات سنگین ریاضی و متنی.

---

## بررسی کلی

ماژول `parsikit.cache` سازوکار ذخیره‌سازی موقت در حافظه (In-Memory LRU) را فراهم می‌آورد که توسط توابع سنگین مانند `parsikit.number.number_to_words` مورد استفاده قرار می‌گیرد.

---

## صنف‌ها (Classes)

### `ThreadSafeLRUCache`

```python
class ThreadSafeLRUCache:
    def __init__(self, maxsize: int = 1024) -> None
```

یک ساختار سبک ذخیره‌سازی موقت که توسط قفل بازورود `threading.RLock` محافظت می‌شود تا بدون ایجاد قفل‌شدگی متقابل (Deadlock)، دسترسی همزمان و بازگشتی امن را تضمین نماید.

#### شروط ظرفیت (Capacity Rules)
- `maxsize` باید یک عدد صحیح (`int`) باشد. در غیر این صورت استثنای `TypeError` پرتاب می‌شود.
- `maxsize >= 0`. مقادیر منفی استثنای `ValueError` ایجاد می‌کنند.
- `maxsize == 0`: در حالت بدون ذخیره‌سازی عمل می‌نماید.

#### متدها و خصوصیات
- **`get(key: Any, default: Any = None) -> Any`**: بازیابی مقدار از کش و به‌روزرسانی موقعیت کلید به عنوان تازه‌ترین مورد مصرف‌شده (MRU).
- **`set(key: Any, value: Any) -> None`**: افزودن یا به‌روزرسانی مقدار در کش با اخراج قدیمی‌ترین مورد در صورت پر بودن ظرفیت.
- **`clear() -> None`**: پاک‌سازی تمامی اطلاعات ذخیره‌شده و بازنشانی آمارها.
- **`pop(key: Any, default: Any = ...) -> Any`**: حذف و بازگرداندن مقدار مرتبط با کلید.
- **`keys_order`**: لستی از کلیدهای ذخیره‌شده از قدیمی‌ترین تا تازه‌ترین.
- **`__len__()` و `__contains__(key)`**: شمارش تعداد اقلام و بررسی وجود کلید در کش.

---

## دیکوریتورها (Decorators)

### `@memoize`

```python
def memoize(maxsize: int = 1024) -> Callable[[Callable[..., _T]], Callable[..., _T]]
```

دیکوریتوری که خروجی توابع را با استفاده از یک نمونه اختصاصی `ThreadSafeLRUCache` ذخیره می‌سازد.

#### ویژگی‌ها
- **احترام به تنظیمات عمومی**: تابع متغیر `parsikit.config.enable_cache` را بررسی کرده و در صورت غیرفعال بودن، مستقیماً تابع اصلی را فراخوانی می‌کند.
- **امنیت ریسمانی**: تضمین امنیت در برنامه‌های چندریسمانی با استفاده از `threading.RLock`.
- **مدیریت آرگومان‌های Unhashable**: در صورت دریافت ورودی‌هایی که قابلیت هش شدن ندارند (مانند لست یا دیکشنری)، فراخوانی به صورت عادی اجرا شده و بدون پرتاب خطای `TypeError` عمل می‌کند.
- **متدهای کنترلی اضافه شده به تابع**:
  - `func.cache`: ارجاع مستقیم به شیء کش.
  - `func.cache_clear()`: پاک‌سازی کش و بازنشانی آمار.
  - `func.cache_info()`: بازگرداندن تاپل `CacheInfo(hits, misses, maxsize, currsize)`.

#### نمونه کد کاربردی

```python
import parsikit
from parsikit.cache import memoize

@memoize(maxsize=512)
def compute_complex_financials(base_amount: int, tier: str = "standard") -> int:
    # محاسبات سنگین ریاضی
    return base_amount * 2

res1 = compute_complex_financials(1000000, tier="A")
res2 = compute_complex_financials(1000000, tier="A")  # فورا از حافظه کش بازگردانده می‌شود
assert res1 == res2

info = compute_complex_financials.cache_info()
print(f"Hits: {info.hits}, Misses: {info.misses}")
```
