import pymel.core as pm
import math

def generateCube(scaleValue,posValue):
    cube = pm.polyCube()[0]
    cube.scale.set(scaleValue)
    cube.rotateY.set(-6*i)
    cube.translate.set(posValue)

x,y,z = 0,0,0
clock_face = pm.PyNode("Dial|Panel")
bbox = clock_face.getBoundingBox()
origin = clock_face.getTranslation(space='world')
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
        clock_face.addAttr(key, at='double', min=0, max=value, dv=0, k=True)

floatMaths = []
for i in range(5):
    floatMaths.append(pm.createNode("floatMath"))

operations = [2, 2, 0, 0, 2]
for i in range(5):
    floatMaths[i].operation.set(operations[i])

floatBs = {0:3600, 1:60, 4:-6}
for key,value in floatBs.items():
    floatMaths[key].floatB.set(value)

connections = {
    pm.PyNode("Dial|Panel").Hours: floatMaths[0].floatA,
    pm.PyNode("Dial|Panel").Minutes : floatMaths[1].floatA,
    pm.PyNode("Dial|Panel").Seconds: floatMaths[3].floatB, 
    floatMaths[0].outFloat : floatMaths[2].floatA,
    floatMaths[1].outFloat : floatMaths[2].floatB,
    floatMaths[2].outFloat : floatMaths[3].floatA,
    floatMaths[3].outFloat : floatMaths[4].floatA,
    floatMaths[4].outFloat : pm.PyNode("Dial|Second").rotateY,
    }
for key,value in connections.items():
    key >> value