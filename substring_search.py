# Алгоритми пошуку підрядка


# ============================================================
# 1. Алгоритм Кнута-Морріса-Пратта (KMP)
# ============================================================

def compute_prefix(pattern):
    """Обчислює префікс-функцію для шаблону."""
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
    """Пошук підрядка алгоритмом Кнута-Морріса-Пратта."""
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
    """Будує таблицю зсувів для алгоритму Боєра-Мура."""
    table = {}
    m = len(pattern)
    for i, char in enumerate(pattern[:-1]):
        table[char] = m - i - 1
    return table


def boyer_moore_search(text, pattern):
    """Пошук підрядка алгоритмом Боєра-Мура."""
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


if __name__ == "__main__":
    text = "Алгоритми пошуку використовуються в програмуванні"
    pattern = "пошуку"

    print(f"KMP      : позиція {kmp_search(text, pattern)}")
    print(f"Боєр-Мур : позиція {boyer_moore_search(text, pattern)}")