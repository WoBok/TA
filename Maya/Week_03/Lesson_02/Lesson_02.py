import maya.cmds as cmds
import math

def generateCube(index,scaleValue,posValue):
    cmds.polyCube(n=f"cube{index}")
    cmds.setAttr(f"cube{index}.scale", scaleValue[0], scaleValue[1], scaleValue[2], type="float3")
    cmds.setAttr(f"cube{index}.rotateY", -6*i)
    cmds.move(posValue[0], posValue[1], posValue[2])

x,y,z = 0,0,0
bbox = cmds.exactWorldBoundingBox("Panel")
origin = cmds.xform("Panel",q=1,t=1,ws=1)
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

def combineRotation(firstNode,secondNode,b,operation):
    floatMath = cmds.shadingNode("floatMath", au=1)
    cmds.connectAttr(f"{firstNode}.rotateY", f"{floatMath}.floatA", f=1)
    cmds.connectAttr(f"{floatMath}.outFloat", f"{secondNode}.rotateY", f=1)
    cmds.setAttr(f"{floatMath}.floatB", b)
    cmds.setAttr(f"{floatMath}.operation", operation)

combineRotation("Second", "Minute" ,60 ,3)
combineRotation("Minute", "Hour" ,12 ,3)

attributes = {"Seconds":59,"Minutes":59,"Hours":11}
for key,value in attributes.items():
    if not cmds.objExists(f"Panel.{key}"):
        cmds.addAttr("|Dial|Panel", ln=key, at="double", min=0, max=value, dv=0, k=1)

floatMaths = []
for i in range(5):
    floatMaths.append(cmds.shadingNode("floatMath", au=1))

operations = [2, 2, 0, 0, 2]
for i in range(5):
    cmds.setAttr(f"{floatMaths[i]}.operation", operations[i])

floatBs = {0:3600, 1:60, 4:-6}
for key,value in floatBs.items():       
    cmds.setAttr(f"{floatMaths[key]}.floatB", value)

connections = {
    "Panel.Hours" : f"{floatMaths[0]}.floatA",
    "Panel.Minutes" : f"{floatMaths[1]}.floatA",
    "Panel.Seconds" : f"{floatMaths[3]}.floatB", 
    f"{floatMaths[0]}.outFloat" : f"{floatMaths[2]}.floatA",
    f"{floatMaths[1]}.outFloat" : f"{floatMaths[2]}.floatB",
    f"{floatMaths[2]}.outFloat" : f"{floatMaths[3]}.floatA",
    f"{floatMaths[3]}.outFloat" : f"{floatMaths[4]}.floatA",
    f"{floatMaths[4]}.outFloat" : "Second.rotateY",
    }
for key,value in connections.items():
    cmds.connectAttr(key, value, f=1)