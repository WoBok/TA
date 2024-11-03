"""
思路：
一、水平方向
    1. 根据水平位置和水平宽度构建弧度区域
    2. 判断砖块是否位于弧度区域内，分三种情况
        1. 砖块全部位于弧度区域内
        2. 砖块头部位于弧度区域内，尾部未位于弧度区域内
        3. 砖块尾部位于弧度区域内，头部未位于弧度区域内
    3. 情况1不构建砖块，情况2、3阶段砖块，并计算缩放以及位置偏移
二、垂直方向
    1. 根据垂直位置和垂直宽度构建高度区域
    2. 根据砖块轴心位置判断砖块是否位于高度区域内
    3. 轴心位置位于高度区域内则不构建砖块
"""

import pymel.core as pm
import math
import math_extensions as mathex
from vector2 import Vector2

brickSize = {"w": 0.053, "d": 0.24, "h": 0.115}  # 砖块尺寸

radius = 1.25  # 半径
height = 3.5  # 高度

horizPos = 0.25  # 水平方向上的位置百分比[0,1]
horizWidth = 0.15  # 水平方向上宽度百分比[0,1]

vertiPos = 0.65  # 垂直方向上的位置百分比[0,1]
vertiHeight = 0.25  # 垂直方向上高度百分比[0,1]

horizRadPivot = mathex.clamp(horizPos, 0, 1) * (2 * math.pi)  # 在圆周上的位置[0,2π]
horizRadHalfWidth = (mathex.clamp(horizWidth, 0, 1) * math.pi)  # 以Pivot为中心，两侧所占的宽度[0,π]
horizRadRange = (  # 宽度的范围
    horizRadPivot - horizRadHalfWidth,
    horizRadPivot + horizRadHalfWidth,
)

vertiPivot = mathex.clamp(vertiPos, 0, 1) * height  # 在圆柱垂直方向的位置[0,height]
vertiHalfHight = (mathex.clamp(vertiHeight, 0, 1) * height / 2)  # 以Pivot为中心，两侧所占的高度[0,height/2]
vertiRange = (
    max(0, vertiPivot - vertiHalfHight),
    min(height + brickSize["h"], vertiPivot + vertiHalfHight + brickSize["h"]),
)  # 高度的范围

if pm.objExists("bricks"):  # 若有bricks节点，则将bricks作为父节点，若无则创建空的组
    bricks = pm.PyNode("bricks")
else:
    bricks = pm.group(n="bricks")
originPoint = bricks.getTranslation(s="world")

currentLayer = 0  # 标识当前构建第几层砖块
yOffset = originPoint.y + brickSize["h"] / 2  # y轴向上的偏移量
y = yOffset  # 初始化y轴高度
perRad = brickSize["d"] / radius  # 砖块宽度所对应的弧度

rightVec = Vector2(radius, 0)  # right方向向量，用于做对比时的参考

while y <= height + yOffset:  # 达到指定高度后停止构建砖块
    currentRad = 0  # 构建下一层时将当前弧度重置
    while currentRad <= 2 * math.pi:  # 构建一整个圆周的砖块后停止构建
        currentLayerRad = (currentRad + currentLayer * perRad / 2)  # 根据当前层数做弧度的偏移，达到交错的效果
        currentRad += perRad  # 移动一个砖块的弧度

        x = radius * math.cos(currentLayerRad) + originPoint.x # 根据弧度计算在XZ平面上的x坐标
        z = radius * math.sin(currentLayerRad) + originPoint.z # 根据弧度计算在XZ平面上的z坐标

        brickHeadVecL = ( # 相对于弧度区域左边缘偏移至right方向向量位置时的砖块头部向量
            Vector2(
                math.cos(currentLayerRad - horizRadRange[0]),
                math.sin(currentLayerRad - horizRadRange[0]),
            )
            * radius
        )
        brickForwardVecL = Vector2.normalize(Vector2(-brickHeadVecL.y, brickHeadVecL.x)) # 垂直于砖块头部向量指砖块向尾向量的方向向量
        brickTailVecL = brickHeadVecL + (brickForwardVecL * brickSize["d"]) # 计算对应的砖块尾部向量

        brickHeadVecR = ( # 相对于弧度区域右边缘偏移至right方向向量位置时的砖块头部向量
            Vector2(
                math.cos(currentLayerRad - horizRadRange[1]),
                math.sin(currentLayerRad - horizRadRange[1]),
            )
            * radius
        )
        brickForwardVecR = Vector2.normalize(Vector2(-brickHeadVecR.y, brickHeadVecR.x)) # 垂直于砖块头部向量指砖块向尾向量的方向向量
        brickTailVecR = brickHeadVecR + (brickForwardVecR * brickSize["d"]) # 计算对应的砖块尾部向量

        scale = (brickSize["w"], brickSize["h"], brickSize["d"]) # 砖块缩放值
        position = (x, y, z) # 砖块位置
        if (y >= vertiRange[0]) and (y < vertiRange[1]) and vertiHeight > 0: # 判断砖块是否在孔洞垂直区域内
            if horizWidth <= 0.5: # 根据水平宽度大小判断是否要反转创建方式
                if horizWidth > 0: # 宽度小于等于0跳过判断
                    if (
                        Vector2.cross(rightVec, brickHeadVecL) > 0
                        and Vector2.cross(rightVec, brickTailVecR) < 0
                    ):  # 位于弧度区域中间部位的砖块不生成
                        continue
                    elif (
                        Vector2.cross(rightVec, brickHeadVecL) < 0
                        and Vector2.cross(rightVec, brickTailVecL) > 0
                    ):  # 对位于弧度区域左边缘上的砖块进行截断
                        d = Vector2.magnitude(rightVec - brickHeadVecL)
                        scale = (brickSize["w"], brickSize["h"], d)
                    elif (
                        Vector2.cross(rightVec, brickHeadVecR) < 0
                        and Vector2.cross(rightVec, brickTailVecR) > 0
                    ):  # 对位于弧度区域右边缘上的砖块进行截断
                        offset = rightVec * radius - brickHeadVecR
                        position = (
                            radius * math.cos(horizRadRange[1]) + originPoint.x,
                            position[1],
                            radius * math.sin(horizRadRange[1]) + originPoint.z,
                        )
                        d = Vector2.magnitude(brickTailVecR - rightVec)
                        scale = (brickSize["w"], brickSize["h"], d)
                    else:  # 不位于弧度区域内的砖块正常生成
                        scale = (brickSize["w"], brickSize["h"], brickSize["d"])
            else:
                if horizWidth >= 1: # 宽度大于等于1时不构建砖块
                    continue
                if (  # 位于弧度区域内的砖块正常生成
                    Vector2.cross(rightVec, brickHeadVecR) > 0
                    and Vector2.cross(rightVec, brickTailVecL) < 0
                ):
                    scale = (brickSize["w"], brickSize["h"], brickSize["d"])
                elif (
                    Vector2.cross(rightVec, brickHeadVecL) < 0
                    and Vector2.cross(rightVec, brickTailVecL) > 0
                ):  # 对位于弧度区域左边缘上的砖块进行截断
                    d = Vector2.magnitude(rightVec - brickHeadVecL)
                    scale = (brickSize["w"], brickSize["h"], d)
                elif (
                    Vector2.cross(rightVec, brickHeadVecR) < 0
                    and Vector2.cross(rightVec, brickTailVecR) > 0
                ):  # 对位于弧度区域右边缘上的砖块进行截断
                    offset = rightVec * radius - brickHeadVecR
                    position = (
                        radius * math.cos(horizRadRange[1]) + originPoint.x,
                        position[1],
                        radius * math.sin(horizRadRange[1]) + originPoint.z,
                    )
                    d = Vector2.magnitude(brickTailVecR - rightVec)
                    scale = (brickSize["w"], brickSize["h"], d)
                else:# 不位于弧度区域中间部位的砖块不生成
                    continue

        cube = pm.polyCube() # 创建Cube
        cube[0].scalePivot.set(0.5, -0.5, -0.5) # 设置缩放轴心
        cube[0].rotatePivot.set(0.5, -0.5, -0.5) # 设置旋转轴心
        cube[0].translate.set(position[0] - 0.5, position[1] + 0.5, position[2] + 0.5) # 设置位置
        cube[0].rotateY.set(-math.degrees(currentLayerRad + perRad / 2)) # 设置y轴旋转
        cube[0].scale.set(scale[0], scale[1], scale[2]) # 设置缩放

        pm.parent(cube[0], bricks) # 将Cube放入父节点
    currentLayer += 1 # 当前层数+1，开始构建下一层
    y += brickSize["h"] # 将y轴高度增加一个砖块的高度
