import maya.cmds as cmds

def combineRotation(firstNode,secondNode):
    floatMath = cmds.shadingNode("floatMath", au=1)
    cmds.connectAttr(f"{firstNode}.rotateY", f"{floatMath}.floatA", f=1)
    cmds.connectAttr(f"{floatMath}.outFloat", f"{secondNode}.rotateY", f=1)
    cmds.setAttr(f"{floatMath}.floatB",60)
    cmds.setAttr(f"{floatMath}.operation",3)

combineRotation("Second","Minute")
combineRotation("Minute","Hour")

