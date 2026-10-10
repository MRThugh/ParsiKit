# Frequently Asked Questions (FAQ)

### 1. Which Python versions does ParsiKit support?
ParsiKit supports Python **3.10 and newer** (including 3.10, 3.11, 3.12, and 3.13).

---

### 2. Does ParsiKit have external dependencies?
No. ParsiKit is 100% pure Python with zero external runtime dependencies. It installs instantly and has minimal overhead.

---

### 3. How does ParsiKit differ from Hazm or PersianJS?
- **Hazm** is focused on Natural Language Processing (NLP), part-of-speech tagging, and morphological analysis.
- **ParsiKit** is a full software infrastructure library for real-world web applications, financial software, database normalization, national ID validation, and secure PII handling.

---

### 4. Is ParsiKit thread-safe?
Yes. Global configurations and the internal cache use Python's re-entrant locks (`threading.RLock`) to guarantee thread safety in multi-threaded application servers like Gunicorn and Uvicorn.

---

### 5. Does ParsiKit expose sensitive customer data in logs?
No. In v3.3.1, exceptions like `InvalidCardNumberError` sanitize messages, and all domain models provide a `.masked` property for safe logging and administration dashboards.

---

### 6. What is the software license?
ParsiKit is licensed under the permissive **MIT License**. You are free to use it in commercial, open-source, and private projects.
