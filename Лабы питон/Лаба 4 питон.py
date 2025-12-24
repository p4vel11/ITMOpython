import sys
import timeit
import math

try:
    import matplotlib.pyplot as plt
    import numpy as np
except Exception:
    import matplotlib.pyplot as plt
    import numpy as np

def fact_recursive(n):
    if n == 0 or n == 1:
        return 1
    return n * fact_recursive(n - 1)

def fact_iterative(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

numbers = list(range(1, 501, 25))
repeat_count = 5
exec_count = 1

recursive_times = []
iterative_times = []

rec_limit = sys.getrecursionlimit()

for n in numbers:
    if n >= rec_limit - 5:
        recursive_times.append(np.nan)
        print(f"n={n}: {rec_limit})")
    else:
        try:
            timer_r = timeit.Timer(lambda: fact_recursive(n))
            times_r = timer_r.repeat(repeat=repeat_count, number=exec_count)
            avg_r = sum(times_r) / len(times_r) / exec_count
        except RecursionError:
            avg_r = np.nan
        recursive_times.append(avg_r)

    try:
        timer_i = timeit.Timer(lambda: fact_iterative(n))
        times_i = timer_i.repeat(repeat=repeat_count, number=exec_count)
        avg_i = sum(times_i) / len(times_i) / exec_count
    except Exception as e:
        avg_i = np.nan

    iterative_times.append(avg_i)

print()
print("-" * 60)
for n, tr, ti in zip(numbers, recursive_times, iterative_times):
    s_r = f"{tr:.9f} с" if not math.isnan(tr) else""
    s_i = f"{ti:.9f} с" if not math.isnan(ti) else""
    print(f"n={n:<3} | рекурсивно: {s_r} | итеративно: {s_i}")

plt.figure(figsize=(10, 6))
x = np.array(numbers)
y_r = np.array(recursive_times, dtype=float)
y_i = np.array(iterative_times, dtype=float)

plt.plot(x, y_r, label='Рекурсивная реализация', marker='o')
plt.plot(x, y_i, label='Итеративная реализация', marker='s')
plt.title("Сравнение времени вычисления факториала")
plt.xlabel("Входное число n")
plt.ylabel("Время выполнения (секунды)")
plt.legend()
plt.grid(True)
plt.yscale('log')
plt.tight_layout()
plt.show()