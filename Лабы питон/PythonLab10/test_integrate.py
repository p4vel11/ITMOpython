
import math
from integrate import integrate

def test_known_integral_cos():
    result = integrate(math.cos, 0, math.pi / 2, n_iter=100000)
    assert abs(result - 1.0) < 1e-4

def test_known_integral_x_squared():
    result = integrate(lambda x: x ** 2, 0, 2, n_iter=100000)
    assert abs(result - 8/3) < 1e-4

def test_convergence():
    res1 = integrate(math.sin, 0, math.pi, n_iter=10000)
    res2 = integrate(math.sin, 0, math.pi, n_iter=100000)
    assert abs(res1 - res2) < 1e-3