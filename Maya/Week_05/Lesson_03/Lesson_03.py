import pymel.core as pm

shapeNode = pm.PyNode('boombox').getShape()
#shapeNode = pm.selected()[0].getShape()#selected返回一个列表
if shapeNode:
    material = shapeNode.outputs(type='shadingEngine')[0]
    for f in material.history(type='file'):
        print(f.fileTextureName.get())
    
type = pm.selected()[0].type()