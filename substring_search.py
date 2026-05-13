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


if __name__ == "__main__":
    text = "Алгоритми пошуку використовуються в програмуванні"
    pattern = "пошуку"
    print(f"KMP: позиція {kmp_search(text, pattern)}")
