
import concurrent.futures as ftres
from functools import partial
from typing import Callable
from integrate import integrate

def integrate_async_thread(f: Callable[[float], float], a: float, b: float, *,
                           n_jobs: int = 2, n_iter: int = 100000) -> float:
    executor = ftres.ThreadPoolExecutor(max_workers=n_jobs)
    step = (b - a) / n_jobs
    spawn = partial(executor.submit, integrate, f, n_iter=n_iter // n_jobs)

    futures = [spawn(a + i * step, a + (i + 1) * step) for i in range(n_jobs)]
    return sum(f.result() for f in ftres.as_completed(futures))