
import cython
from libc.math cimport cos, M_PI

@cython.boundscheck(False)
@cython.wraparound(False)
def integrate_cy(double (*f)(double), double a, double b, int n_iter=100000):
    cdef double acc = 0.0
    cdef double step = (b - a) / n_iter
    cdef int i
    cdef double x
    for i in range(n_iter):
        x = a + i * step
        acc += f(x) * step
        return acc