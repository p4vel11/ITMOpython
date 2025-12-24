
import cython
from libc.math cimport cos

@cython.boundscheck(False)
@cython.wraparound(False)
cdef double integrate_cos_core(double a, double b, int n_iter) nogil:
    cdef double acc = 0.0
    cdef double step = (b - a) / n_iter
    cdef int i
    for i in range(n_iter):
        acc += cos(a + i * step) * step
    return acc

def integrate_cos_nogil(double a, double b, int n_iter=100000):
    return integrate_cos_core(a, b, n_iter)