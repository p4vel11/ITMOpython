
import threading
import math
import integrate_nogil

def worker(a: float, b: float, n_iter: int, results: list, index: int):
    result = integrate_nogil.integrate_cos_nogil(a, b, n_iter)
    results[index] = result

def integrate_parallel_nogil(a: float, b: float, n_jobs: int = 4, n_iter: int = 1000000):
    step = (b - a) / n_jobs
    threads = []
    results = [0.0] * n_jobs

    for i in range(n_jobs):
        t = threading.Thread(
            target=worker,
            args=(a + i * step, a + (i + 1) * step, n_iter // n_jobs, results, i)
        )
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return sum(results)

if __name__ == "__main__":
    # Интегрируем cos(x) от 0 до π
    result = integrate_parallel_nogil(0.0, math.pi, n_jobs=4, n_iter=1000000)
    print(f"Результат (многопоточный noGIL): {result:.8f}")