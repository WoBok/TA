def check_decorator(func):
    def wrapper():
        num = func()
        if num < 100:
            print("The return value is less than 100.")

    return wrapper


@check_decorator
def func1():
    print("func1")
    return 10


func1()


################################################################################

def check_decorator2(func):
    def wrapper2(*args):
        num = func(*args)
        if num < 100:
            print("The return value is less than 100.")

    return wrapper2


@check_decorator2
def func2(*args):
    print("func2: " + str(args[0]))
    return args[0]


func2((10))


################################################################################

def check_decorator3(func):
    def wrapper3(num):
        num = func(num)
        if num < 100:
            print("The return value is less than 100.")

    return wrapper3


@check_decorator3
def func3(num):
    print("func3: " + str(num))
    return num


func3(50)
