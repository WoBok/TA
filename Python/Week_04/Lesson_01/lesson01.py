def fun(x, y, mode):
    def f1(x):
        print(x+y)
    
    def f2(z):
        print(x+y+z)

    return f1 if mode==1 else f2

fun(1,2,1)(3)
fun(1,2,0)(3)

"""
result:
5
6
"""

def func(x, y, mode):
    f1 = lambda: print(x+y)
    f2 = lambda: print(x-y)

    return f1 if mode==1 else f2
func(1,2,1)()

def func(x, y, mode):
    f1 = lambda z: print(x+y+z)
    f2 = lambda z: print(x-y-z)

    return f1 if mode==1 else f2
func(1,2,1)(1)