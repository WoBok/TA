import pymel.core as pm
import maya.cmds as cmds
import math

def generateCube(scaleValue,posValue):
    cube = pm.polyCube()[0]
    cube.scale.set(scaleValue)
    cube.rotateY.set(-6*i)
    cube.translate.set(posValue)

x,y,z = 0,0,0
clock_face = pm.PyNode("Dial|Panel")
bbox = clock_face.getBoundingBox()
origin = clock_face.translate.get()
radius = bbox.w / 2 - 0.5
angle = 2 * math.pi / 60
for i in range(60):
    currentAngle = angle * i
    x = radius * math.cos(currentAngle) + origin.x
    y = origin[1]
    z = radius * math.sin(currentAngle) + origin.z
    if i%5 == 0:
        generateCube((0.7,0.2,0.2),(x,y,z))
    else:
        generateCube((0.5,0.1,0.1),(x,y,z))

def combineRotation(firstNode,secondNode,b,operation):
    floatMath = pm.createNode("floatMath")
    firstNode.rotateY >> floatMath.floatA
    floatMath.outFloat >> secondNode.rotateY
    floatMath.floatB.set(b)
    floatMath.operation.set(operation)

combineRotation(pm.PyNode("Dial|Second"), pm.PyNode("Dial|Minute") ,60 ,3)
combineRotation(pm.PyNode("Dial|Minute"), pm.PyNode("Dial|Hour") ,12 ,3)

attributes = {"Seconds":59,"Minutes":59,"Hours":11}
for key,value in attributes.items():
    if not clock_face.hasAttr(key):
        clock_face.addAttr(ln=key, at='double', min=0, max=value, dv=0, k=True);
        #cmds.addAttr("|Dial|Panel", ln=key, at="double", min=0, max=value, dv=0, k=1)

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