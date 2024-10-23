import pymel.core as pm
import math


#math_extensions
def clamp(value, min, max):
    if value < min:
        value = min
    elif value > max:
        value = max
    return value


# modul Vector2---------------------------------------------------------------------
class Vector2:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, num):
        return Vector2(self.x * num, self.y * num)

    def __truediv__(self, num):
        try:
            return Vector2(self.x / num, self.y / num)
        except ZeroDivisionError:
            print("The divisor cannot be zero. The result remains unchanged.")
            return self

    def magnitude(v):
        return math.sqrt(v.x * v.x + v.y * v.y)

    def sqrMagnitude(v):  # the squared length of this vector
        return v.x * v.x + v.y * v.y

    def normalize(v):
        mag = Vector2.magnitude(v)
        if mag < 1e-15:
            return Vector2(0, 0)
        return v / mag

    def dot(v1, v2):
        return v1.x * v2.x + v1.y * v2.y

    def cross(v1, v2):  # 用于判断向量的方位
        return v1.x * v2.y + v1.y * v2.x

    def rad(v1, v2):
        v1SqrMagnitude = Vector2.sqrMagnitude(v1)
        v2SqrMagnitude = Vector2.sqrMagnitude(v2)
        num1 = math.sqrt(v1SqrMagnitude * v2SqrMagnitude)
        if num1 < 1e-15:
            return 0
        v1dotv2 = Vector2.dot(v1, v2)
        num2 = clamp(v1dotv2 / num1, -1, 1)
        return math.acos(num2)


# modul Vector2---------------------------------------------------------------------

brickSize = {"w": 0.053, "d": 0.24, "h": 0.115}

radius = 1.25
height = 3.5

horizPos = 0.25
horizWidth = 0.75

vertiPos = 0.65
vertiHeight = 0.25

horizRadPivot = clamp(horizPos, 0, 1) * (2 * math.pi)
horizRadHalfWidth = clamp(horizWidth, 0, 1) * math.pi
horizRadRange = (
    horizRadPivot - horizRadHalfWidth,
    horizRadPivot + horizRadHalfWidth,
)

vertiPivot = clamp(vertiPos, 0, 1) * height
vertiHalfHight = clamp(vertiHeight, 0, 1) * height / 2
vertiRange = (max(0, vertiPivot - vertiHalfHight),
              min(height + brickSize["h"],
                  vertiPivot + vertiHalfHight + brickSize["h"]))
print(vertiRange)

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

rightVec = Vector2(radius, 0)

while y <= height + yOffset:
    while currentRad <= 2 * math.pi:

        currentLayerRad = currentRad + layers * perRad / 2
        currentRad += perRad

        x = radius * math.cos(currentLayerRad) + originPoint.x
        z = radius * math.sin(currentLayerRad) + originPoint.z

        brickHeadVecL = (Vector2(
            math.cos(currentLayerRad - horizRadRange[0]),
            math.sin(currentLayerRad - horizRadRange[0]),
        ) * radius)
        brickForwardVecL = Vector2.normalize(
            Vector2(-brickHeadVecL.y, brickHeadVecL.x))
        brickTailVecL = brickHeadVecL + (brickForwardVecL * brickSize["d"])

        brickHeadVecR = (Vector2(
            math.cos(currentLayerRad - horizRadRange[1]),
            math.sin(currentLayerRad - horizRadRange[1]),
        ) * radius)
        brickForwardVecR = Vector2.normalize(
            Vector2(-brickHeadVecR.y, brickHeadVecR.x))
        brickTailVecR = brickHeadVecR + (brickForwardVecR * brickSize["d"])

        scale = (brickSize["w"], brickSize["h"], brickSize["d"])
        position = (x, y, z)
        if (y >= vertiRange[0]) and (y < vertiRange[1]):
            if horizWidth <= 0.5:
                if horizWidth > 0:
                    if (Vector2.cross(rightVec, brickHeadVecL) > 0
                            and Vector2.cross(rightVec,
                                              brickTailVecR) < 0):  # 中间部位不生成
                        continue
                    elif (Vector2.cross(rightVec, brickHeadVecL) < 0
                          and Vector2.cross(rightVec,
                                            brickTailVecL) > 0):  # 左侧部位裁剪
                        d = Vector2.magnitude(rightVec - brickHeadVecL)
                        scale = (brickSize["w"], brickSize["h"], d)
                    elif (Vector2.cross(rightVec, brickHeadVecR) < 0
                          and Vector2.cross(rightVec,
                                            brickTailVecR) > 0):  # 右侧部位裁剪
                        offset = rightVec * radius - brickHeadVecR
                        position = (
                            radius * math.cos(horizRadRange[1]) +
                            originPoint.x,
                            position[1],
                            radius * math.sin(horizRadRange[1]) +
                            originPoint.z,
                        )
                        d = Vector2.magnitude(brickTailVecR - rightVec)
                        scale = (brickSize["w"], brickSize["h"], d)
                    else:  # 不裁剪
                        scale = (brickSize["w"], brickSize["h"],
                                 brickSize["d"])
            else:
                if horizWidth >= 1:
                    continue
                if (Vector2.cross(rightVec, brickHeadVecR) > 0
                        and Vector2.cross(rightVec, brickTailVecL) < 0):
                    scale = (brickSize["w"], brickSize["h"], brickSize["d"])
                elif (Vector2.cross(rightVec, brickHeadVecL) < 0 and
                      Vector2.cross(rightVec, brickTailVecL) > 0):  # 左侧部位裁剪
                    d = Vector2.magnitude(rightVec - brickHeadVecL)
                    scale = (brickSize["w"], brickSize["h"], d)
                elif (Vector2.cross(rightVec, brickHeadVecR) < 0 and
                      Vector2.cross(rightVec, brickTailVecR) > 0):  # 右侧部位裁剪
                    offset = rightVec * radius - brickHeadVecR
                    position = (
                        radius * math.cos(horizRadRange[1]) + originPoint.x,
                        position[1],
                        radius * math.sin(horizRadRange[1]) + originPoint.z,
                    )
                    d = Vector2.magnitude(brickTailVecR - rightVec)
                    scale = (brickSize["w"], brickSize["h"], d)
                else:
                    continue

        cube = pm.polyCube()
        cube[0].scalePivot.set(0.5, -0.5, -0.5)
        cube[0].rotatePivot.set(0.5, -0.5, -0.5)
        cube[0].translate.set(position[0] - 0.5, position[1] + 0.5,
                              position[2] + 0.5)
        cube[0].rotateY.set(-math.degrees(currentLayerRad + perRad / 2))
        cube[0].scale.set(scale[0], scale[1], scale[2])

        pm.parent(cube[0], bricks)
    currentRad = 0
    layers += 1
    y += brickSize["h"]
