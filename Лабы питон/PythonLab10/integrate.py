import math
from typing import Callable

def integrate(f: Callable[[float], float], a: float, b: float, *, n_iter: int = 100000) -> float:

    if n_iter <= 0:
        raise ValueError()
    if a >= b:
        raise ValueError()

    acc = 0.0
    step = (b - a) / n_iter
    for i in range(n_iter):
        acc += f(a + i * step) * step
    return acc