import math
import math_extensions as mathex

"""封装便于操作二维向量的类"""


class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    """加法运算符重载"""

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    """减法运算符重载"""

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    """乘法运算符重载"""

    def __mul__(self, num):
        return Vector2(self.x * num, self.y * num)

    """除法运算符重载"""

    def __truediv__(self, num):
        try:
            return Vector2(self.x / num, self.y / num)
        except ZeroDivisionError:
            print("The divisor cannot be zero. The result remains unchanged.")
            return self

    """向量模长"""

    def magnitude(v):
        return math.sqrt(v.x * v.x + v.y * v.y)

    """向量平方模长"""

    def sqrMagnitude(v):
        return v.x * v.x + v.y * v.y

    """向量单位化"""

    def normalize(v):
        mag = Vector2.magnitude(v)
        if mag < 1e-15:
            return Vector2(0, 0)
        return v / mag

    """向量点积"""

    def dot(v1, v2):
        return v1.x * v2.x + v1.y * v2.y

    """向量叉积"""

    def cross(v1, v2):  # 用于判断向量之间的方向
        return v1.x * v2.y + v1.y * v2.x

    """计算两向量间的弧度"""

    def rad(v1, v2):
        v1SqrMagnitude = Vector2.sqrMagnitude(v1)
        v2SqrMagnitude = Vector2.sqrMagnitude(v2)
        num1 = math.sqrt(v1SqrMagnitude * v2SqrMagnitude)
        if num1 < 1e-15:
            return 0
        v1dotv2 = Vector2.dot(v1, v2)
        num2 = mathex.clamp(v1dotv2 / num1, -1, 1)
        return math.acos(num2)
