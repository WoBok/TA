import math

radius = 1

height = 3

brickSize = {"w": 0.24, "d": 0.053, "h": 0.115}

rad = brickSize["w"] / radius

currentRad = 0
y = 0

while currentRad <= 2 * math.pi:
    x = radius * math.cos(currentRad)
    z = radius * math.sin(currentRad)
    print(f"rad:{currentRad}, angle: {math.degrees(currentRad)}")
    currentRad += rad
# while y <= height:

#     currentRad = 0
#     y += brickSize['h']

v1 = (2, 3)
v2 = (1, 1)
# print(v1 - v2)


class Test1:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        print(x, y)


def dot(v1, v2):
    return v1.x * v2.x + v1.y * v2.y


t1 = Test1(9, 2)
t2 = Test1(2, 1)
d = dot(t1, t2)
print(d)