import pymel.core as pm
import math
import math_extensions as mathex
from vector2 import Vector2

brickSize = {"w": 0.053, "d": 0.24, "h": 0.115}

radius = 1.25
height = 3.5

horizPos = 0.25  #水平方向上的位置百分比[0,1]
horizWidth = 0.75  #水平方向上宽度百分比[0,1]

vertiPos = 0.65  #垂直方向上的位置百分比[0,1]
vertiHeight = 0.25  #垂直方向上高度百分比[0,1]

horizRadPivot = mathex.clamp(horizPos, 0, 1) * (2 * math.pi)
horizRadHalfWidth = mathex.clamp(horizWidth, 0, 1) * math.pi
horizRadRange = (
    horizRadPivot - horizRadHalfWidth,
    horizRadPivot + horizRadHalfWidth,
)

vertiPivot = mathex.clamp(vertiPos, 0, 1) * height
vertiHalfHight = mathex.clamp(vertiHeight, 0, 1) * height / 2
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
