import maya.cmds as cmds

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