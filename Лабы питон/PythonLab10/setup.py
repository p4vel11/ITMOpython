
from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize("integrate_nogil.pyx", annotate=True),
    zip_safe=False,
)