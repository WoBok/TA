import pymel.core as pm
import math


# modul Vector2---------------------------------------------------------------------
class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __mul__(self, num):
        return Vector2(self.x * num, self.y * num)

    def __truediv__(self, num):
        try:
            return Vector2(self.x / num, self.y / num)
        except ZeroDivisionError:
            print("The divisor cannot be zero. The result remains unchanged.")
            return self


def clamp(value, min, max):  # 将下列函数封装到vector2,静态函数怎么定义？
    if value < min:
        value = min
    elif value > max:
        value = max
    return value


def magnitude(v):
    return math.sqrt(v.x * v.x + v.y * v.y)


def sqrMagnitude(v):  # the squared length of this vector
    return v.x * v.x + v.y * v.y


def normalize(v):
    mag = magnitude(v)
    if mag < 1e-15:
        return Vector2(0, 0)
    return v / mag


def dot(v1, v2):
    return v1.x * v2.x + v1.y * v2.y


def cross(v1, v2):  # 用于判断向量的方位
    return v1.x * v2.y + v1.y * v2.x


def rad(v1, v2):
    v1SqrMagnitude = sqrMagnitude(v1)
    v2SqrMagnitude = sqrMagnitude(v2)
    num1 = math.sqrt(v1SqrMagnitude * v2SqrMagnitude)
    if num1 < 1e-15:
        return 0
    v1dotv2 = dot(v1, v2)
    num2 = clamp(v1dotv2 / num1, -1, 1)
    return math.acos(num2)


# modul Vector2---------------------------------------------------------------------

brickSize = {"w": 0.053, "d": 0.24, "h": 0.115}

radius = 1
height = 3

horizontalPos = 0
horizontalWidth = 0.8


horizRadPivot = horizontalPos * (2 * math.pi)

horizRadHalfWidth = horizontalWidth * (2 * math.pi) / 2
horizRadRange = (
    horizRadPivot - horizRadHalfWidth,
    horizRadPivot + horizRadHalfWidth,
)

print(horizRadPivot)
print(horizRadHalfWidth)
print(horizRadRange)

horizRadLeftVec = Vector2(math.cos(horizRadRange[0]), math.sin(horizRadRange[0]))
horizRadRightVec = Vector2(math.cos(horizRadRange[1]), math.sin(horizRadRange[1]))
sphere = pm.polySphere(r=0.1)
sphere[0].translate.set(radius * horizRadLeftVec.x, 0, radius * horizRadLeftVec.y)
sphere = pm.polySphere(r=0.1)
sphere[0].translate.set(radius * horizRadRightVec.x, 0, radius * horizRadRightVec.y)

if pm.objExists("bricks"):
    bricks = pm.PyNode("bricks")
else:
    bricks = pm.group(n="bricks")
originPoint = bricks.getTranslation(s="world")

currentRad = 0
layers = 0
yOffset = originPoint.y + brickSize["h"] / 2
y = yOffset
perRad = brickSize["d"] / radius

spheres = pm.group(n="spheres")

rightVec = Vector2(1, 0)
while y <= height + yOffset:
    while currentRad <= 2 * math.pi:
        currentLayerRad = currentRad + layers * perRad / 2
        currentRad += perRad

        cosValue = math.cos(currentLayerRad)
        sinValue = math.sin(currentLayerRad)
        x = radius * cosValue + originPoint.x
        z = radius * sinValue + originPoint.z

        brickHeadVecL = (
            Vector2(
                math.cos(currentLayerRad - horizRadRange[0]),
                math.sin(currentLayerRad - horizRadRange[0]),
            )
            * radius
        )
        brickForwardVecL = normalize(Vector2(-brickHeadVecL.y, brickHeadVecL.x))
        brickTailVecL = brickHeadVecL + (brickForwardVecL * brickSize["d"])

        brickHeadVecR = (
            Vector2(
                math.cos(currentLayerRad - horizRadRange[1]),
                math.sin(currentLayerRad - horizRadRange[1]),
            )
            * radius
        )
        brickForwardVecR = normalize(Vector2(-brickHeadVecR.y, brickHeadVecR.x))
        brickTailVecR = brickHeadVecR + (brickForwardVecR * brickSize["d"])

        sphere = pm.polySphere(r=0.003)
        sphere[0].translate.set(brickHeadVecL.x, y, brickHeadVecL.y)
        pm.parent(sphere[0], spheres)
        sphere = pm.polySphere(r=0.003)
        sphere[0].translate.set(brickTailVecL.x, y, brickTailVecL.y)
        pm.parent(sphere[0], spheres)

        if horizontalWidth <= 0.5:
            if (
                cross(rightVec, brickHeadVecL) > 0
                and cross(rightVec, brickTailVecR) < 0
            ):
                cube = pm.polyCube(w=0.001, d=0.001, h=0.001)
            else:
                cube = pm.polyCube(w=brickSize["w"], d=brickSize["d"], h=brickSize["h"])
        else:
            if (
                cross(rightVec, brickHeadVecL) < 0
                and cross(rightVec, brickTailVecR) > 0
            ):
                cube = pm.polyCube(w=brickSize["w"], d=brickSize["d"], h=brickSize["h"])
            else:
                cube = pm.polyCube(w=0.001, d=0.001, h=0.001)

        cube[0].scalePivot.set(
            brickSize["w"] / 2, -brickSize["h"] / 2, -brickSize["d"] / 2
        )
        cube[0].rotatePivot.set(
            brickSize["w"] / 2, -brickSize["h"] / 2, -brickSize["d"] / 2
        )
        cube[0].translate.set(x, y, z)
        cube[0].rotateY.set(-math.degrees(currentLayerRad + perRad / 2))

        pm.parent(cube[0], bricks)
    currentRad = 0
    layers += 1
    y += brickSize["h"]
