'''print("Введите коэффициенты для квадратного уравнения (ax^2 + bx + c = 0):")
a = float(input("a = "))
b = float(input("b = "))
c = float(input("c = "))'''
import math


def discriminant(a, b, c):
    return round(b ** 2 - 4 * a * c, 2)


def qe_roots(a, b, c):
    d = discriminant(a, b, c)
    if d > 0:
        return round((-b + math.sqrt(d)) / (2 * a), 2), round((-b - math.sqrt(d)) / (2 * a), 2)
    elif d == 0:
        return round(-b / (2 * a), 2)

'''
print(discriminant(2, 4, 2))
print(discriminant(3.2, -7.8, 1))
print(discriminant(8, 4, 2))'''