import pymel.core as pm
import math


# modul Vector2---------------------------------------------------------------------
class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)


def clamp(value, min, max):
    if value < min:
        value = min
    elif value > max:
        value = max
    return value


def magnitude(v):
    return math.sqrt(v.x * v.x + v.y * v.y)


def sqrMagnitude(v):  # the squared length of this vector
    return v.x * v.x + v.y * v.y


def dot(v1, v2):
    return v1.x * v2.x + v1.y * v2.y


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

horizontalPos = 0.2
horizontalWidth = 0.2

horizRadPivot = horizontalPos * 2 * math.pi
horizRadHalfWidth = horizontalWidth * 2 * math.pi / 2
horizRadRange = (
    horizRadPivot - horizRadHalfWidth,
    horizRadPivot + horizRadHalfWidth,
)

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

compVecZero = Vector2(math.cos(0), math.sin(0))
compVecPI = Vector2(math.cos(math.pi), math.sin(math.pi))

while y <= height + yOffset:
    while currentRad <= 2 * math.pi:
        currentLayerRad = currentRad + layers * perRad / 2
        currentRad += perRad

        cosValue = math.cos(currentLayerRad)
        sinValue = math.sin(currentLayerRad)
        x = radius * cosValue + originPoint.x
        z = radius * sinValue + originPoint.z

        if currentLayerRad < math.pi:
            compVec = compVecZero
        else:
            compVec = compVecPI

        brickHeadVec = Vector2(cosValue, sinValue)
        brickForwardVec = Vector2(sinValue, -cosValue)
        brickTailVec = brickHeadVec + brickForwardVec

        hcRad = rad(brickHeadVec, compVec)
        tcRad = rad(brickTailVec, compVec)

        if not (hcRad > horizRadRange[1] or tcRad < horizRadRange[0]):
            print("Is in range...")
            cube = pm.polyCube(w=brickSize["w"], d=brickSize["d"], h=brickSize["h"],sx=5,sy=5,sz=5)
        else:
            cube = pm.polyCube(w=brickSize["w"], d=brickSize["d"], h=brickSize["h"])

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
