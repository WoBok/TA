def fun(x, y, mode):

    def f1(x):
        print(x + y)

    def f2(z):
        print(x + y + z)

    return f1 if mode == 1 else f2

fun(1, 2, 1)(3)
fun(1, 2, 0)(3)
"""
result:
5
6
"""

def func(x, y, mode):
    f1 = lambda: print(x + y)
    f2 = lambda: print(x - y)

    return f1 if mode == 1 else f2

func(1, 2, 1)()

def func(x, y, mode):
    f1 = lambda z: print(x + y + z)
    f2 = lambda z: print(x - y - z)

    return f1 if mode == 1 else f2

func(1, 2, 1)(1)

def fun(p1, p2, /, k1, k2):
    print(p1)
    print(p2)
    print(k1)

fun(1, 2, k2=4, k1=3)


def fun(p1, *, k1, k2):
    print(p1)
    print(k1)
    print(k2)


fun(1, k2=3, k1=2)


def fun(*args, **kwargs):
    print(args)
    print(kwargs)


fun(1, 23, 4, k=1, s=3, m=9)

def fun(p1,/,*,k1,k2):
    print(p1)
    print(k1)
    print(k2)

fun(1, 3, 2)