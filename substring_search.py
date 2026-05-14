import timeit


# ============================================================
# 1. Алгоритм Кнута-Морріса-Пратта (KMP)
# ============================================================

def compute_prefix(pattern):
    m = len(pattern)
    prefix = [0] * m
    k = 0
    for q in range(1, m):
        while k > 0 and pattern[k] != pattern[q]:
            k = prefix[k - 1]
        if pattern[k] == pattern[q]:
            k += 1
        prefix[q] = k
    return prefix


def kmp_search(text, pattern):
    n, m = len(text), len(pattern)
    if m == 0:
        return 0
    prefix = compute_prefix(pattern)
    q = 0
    for i in range(n):
        while q > 0 and pattern[q] != text[i]:
            q = prefix[q - 1]
        if pattern[q] == text[i]:
            q += 1
        if q == m:
            return i - m + 1
    return -1


# ============================================================
# 2. Алгоритм Боєра-Мура (Boyer-Moore)
# ============================================================

def build_shift_table(pattern):
    table = {}
    m = len(pattern)
    for i, char in enumerate(pattern[:-1]):
        table[char] = m - i - 1
    return table


def boyer_moore_search(text, pattern):
    n, m = len(text), len(pattern)
    if m == 0:
        return 0
    shift_table = build_shift_table(pattern)
    i = m - 1
    while i < n:
        j = m - 1
        k = i
        while j >= 0 and text[k] == pattern[j]:
            j -= 1
            k -= 1
        if j == -1:
            return k + 1
        i += shift_table.get(text[i], m)
    return -1


# ============================================================
# 3. Алгоритм Рабіна-Карпа (Rabin-Karp)
# ============================================================

def rabin_karp_search(text, pattern):
    n, m = len(text), len(pattern)
    if m == 0:
        return 0
    base = 256
    mod = 101
    pattern_hash = 0
    text_hash = 0
    h = 1
    for _ in range(m - 1):
        h = (h * base) % mod
    for i in range(m):
        pattern_hash = (base * pattern_hash + ord(pattern[i])) % mod
        text_hash = (base * text_hash + ord(text[i])) % mod
    for i in range(n - m + 1):
        if pattern_hash == text_hash:
            if text[i:i + m] == pattern:
                return i
        if i < n - m:
            text_hash = (base * (text_hash - ord(text[i]) * h) + ord(text[i + m])) % mod
            if text_hash < 0:
                text_hash += mod
    return -1


# ============================================================
# 4. Читання файлів та вимірювання часу
# ============================================================

def measure_time(func, text, pattern, runs=100):
    """Вимірює час виконання алгоритму через timeit."""
    timer = timeit.Timer(lambda: func(text, pattern))
    return timer.timeit(number=runs) / runs


def run_benchmark(text, text_name, existing, fake):
    """Запускає бенчмарк для одного тексту."""
    print(f"\n{'='*60}")
    print(f"  {text_name}")
    print(f"{'='*60}")

    for pattern, label in [(existing, "Існуючий підрядок"),
                           (fake, "Вигаданий підрядок")]:
        print(f"\n  Підрядок: '{pattern}' [{label}]")
        print(f"  {'-'*50}")

        results = {}
        for name, func in [("KMP", kmp_search),
                            ("Боєр-Мур", boyer_moore_search),
                            ("Рабін-Карп", rabin_karp_search)]:
            t = measure_time(func, text, pattern)
            results[name] = t
            found = func(text, pattern)
            status = f"позиція {found}" if found != -1 else "не знайдено"
            print(f"  {name:<12}: {t:.6f}с  [{status}]")

        winner = min(results, key=results.get)
        print(f"  Найшвидший: {winner} ✓")


def main():
    # Читання файлів
    with open("стаття_1.txt", "r", encoding="utf-8", errors="ignore") as f:
        text1 = f.read()

    with open("стаття_2.txt", "r", encoding="utf-8", errors="ignore") as f:
        text2 = f.read()

    # Стаття 1 — підрядки з коду Java який є в статті
    existing1 = "linearSearch"       # існує в статті 1
    fake1 = "interpolationSort"      # не існує в статті 1

    # Стаття 2 — підрядки з українського тексту
    existing2 = "структури даних"    # існує в статті 2 (позиція 11)
    fake2 = "штучний інтелект"       # не існує в статті 2

    run_benchmark(text1, "Стаття 1", existing1, fake1)
    run_benchmark(text2, "Стаття 2", existing2, fake2)

    print(f"\n{'='*60}")
    print("  Бенчмарк завершено!")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()