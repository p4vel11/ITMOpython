import timeit
from integrate import integrate
import math

def benchmark(n_iter: int):
    time_taken = timeit.timeit(
        lambda: integrate(math.cos, 0, math.pi, n_iter=n_iter),
        number=10
    )
    print(f"n_iter={n_iter:>8} → {time_taken:.4f} сек (среднее за 10 запусков)")

if __name__ == "__main__":
    for n in [10_000, 100_000, 500_000, 1_000_000]:
        benchmark(n)