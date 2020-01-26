# AAL - usun i wygraj
# Autor: Piotr Zmyslony
from distutils.core import setup
from Cython.Build import cythonize
import numpy

setup(
    ext_modules = cythonize("findmax.pyx"),
    include_dirs=[numpy.get_include()]
)