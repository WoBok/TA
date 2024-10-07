import maya.cmds as cmds
import math

def generateCube(index,scaleValue,posValue):
    cmds.polyCube(n=f"cube{index}")
    cmds.setAttr(f"cube{index}.scale", scaleValue[0], scaleValue[1], scaleValue[2], type="float3")
    cmds.setAttr(f"cube{index}.rotateY", -6*i)
    cmds.move(posValue[0], posValue[1], posValue[2])

x,y,z = 0,0,0
bbox = cmds.exactWorldBoundingBox("pDisc1")
origin = cmds.xform("pDisc1",q=1,t=1,ws=1)
radius = abs(bbox[3] - bbox[0]) / 2 - 0.5
angle = 2 * math.pi / 60
for i in range(60):
    currentAngle = angle * i
    x = radius * math.cos(currentAngle) + origin[0]
    y = origin[1]
    z = radius * math.sin(currentAngle) + origin[2]
    if i%5 == 0:
        generateCube(i,(0.7,0.2,0.2),(x,y,z))
    else:
        generateCube(i,(0.5,0.1,0.1),(x,y,z))