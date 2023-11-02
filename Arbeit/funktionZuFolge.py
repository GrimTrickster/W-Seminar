# importing sympy library
from sympy import *
from sympy.abc import x

# calling doit() method on expression
geek = (2 * Integral(x, x)).doit()

print(geek)