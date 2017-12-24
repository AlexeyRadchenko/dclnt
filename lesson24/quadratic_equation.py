import math


def discriminant(a, b, c):
    return round(b ** 2 - 4 * a * c, 2)


def qe_roots(a, b, c):
    d = discriminant(a, b, c)
    if d > 0:
        return round((-b + math.sqrt(d)) / (2 * a), 2), round((-b - math.sqrt(d)) / (2 * a), 2)
    elif d == 0:
        return round(-b / (2 * a), 2)
