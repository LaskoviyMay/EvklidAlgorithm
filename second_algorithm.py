from math import gcd

def extended_gcd(a, b):
    """Расширенный алгоритм Евклида для нахождения НОД и коэффициентов x, y."""
    if b == 0:
        return a, 1, 0
    else:
        g, x, y = extended_gcd(b, a % b)
        return g, y, x - (a // b) * y

def mod_inverse(a, m):
    """Нахождение обратного элемента a по модулю m."""
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError(f"Обратный элемент для {a} по модулю {m} не существует.")
    return x % m

def solve_congruences(congruences):
    """
    Решение системы сравнений с использованием КТО.
    
    congruences: список кортежей вида [(a1, n1), (a2, n2), ...],
                 где ai - остаток, ni - модуль.
    """
    # Шаг 1: Вычисление общего модуля N
    N = 1
    for _, ni in congruences:
        N *= ni

    result = 0
    print(f"Общий модуль N = {N}")
    
    # Шаг 2: Вычисление частных модулей Ni и обратных элементов ui
    for ai, ni in congruences:
        Ni = N // ni
        ui = mod_inverse(Ni, ni)
        print(f"Для модуля {ni}:")
        print(f"  Частный модуль Ni = {Ni}")
        print(f"  Обратный элемент ui = {ui} (по модулю {ni})")
        result += ai * ui * Ni
    
    # Шаг 3: Приведение результата по модулю N
    result %= N
    print(f"Итоговое решение: x ≡ {result} (mod {N})")
    return result

# Пример использования
if __name__ == "__main__":
    # Система сравнений: x ≡ 13 (mod 17), x ≡ 15 (mod 27), x ≡ 7 (mod 10)
    congruences = [(13, 17), (15, 27), (7, 10)]
    solution = solve_congruences(congruences)
    print(f"Ответ: x ≡ {solution} (mod {17 * 27 * 10})")