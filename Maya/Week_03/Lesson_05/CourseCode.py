import maya.cmds as cmds
import pymel.core as pm
import math

clock_face = pm.SCENE.Surface
second_pointer = pm.SCENE.second
minute_pointer = pm.SCENE.minute
hour_pointer = pm.SCENE.hour

bbox = clock_face.getBoundingBox()
radius = bbox.w/2-1
pi = 3.141592654

surface_location = clock_face.getTranslation(space='world')


for i in range(60):
    cube = cmds.polyCube()[0]
    arc = i*6*pi/180
    x,y,z=(
        radius*math.cos(arc)+surface_location.x,
        surface_location.y,
        radius*math.sin(arc)+surface_location.z
        )
    cube = pm.PyNode(cube)
    cube.t.set([x,y,z])

    if not i%5:
        cube.s.set([2, 1, 0.4])
    else:
        cube.s.set([1, 0.5, 0.2])
    cube.ry.set(-6*i)

math_node = pm.createNode('floatMath')
math_node.operation.set(3)
second_pointer.ry >> math_node.floatA
math_node.outFloat >> minute_pointer.ry
math_node.floatB.set(60)


math_node = pm.createNode('floatMath')
math_node.operation.set(3)
minute_pointer.ry >> math_node.floatA
math_node.outFloat >> hour_pointer.ry
math_node.floatB.set(12)


time_units = {'seconds': 59, 'minutes': 59, 'hours': 11}
for key,value in time_units.items():
    if clock_face.hasAttr(key):
        pass
    else:
        clock_face.addAttr(ln=key, at='double', min=0, max=value, dv=0, k=True)


math_nodes = [pm.createNode('floatMath') for i in range(5)]
for i,mode in enumerate([2, 0, 2, 0, 2]):
    math_nodes[i].operation.set(mode)

math_node_01 = math_nodes[0]
clock_face.hours >> math_node_01.floatA
math_node_01.floatB.set(60)

math_node_02 = math_nodes[1]
math_node_01.outFloat >> math_node_02.floatA
clock_face.minutes >> math_node_02.floatB

math_node_03 = math_nodes[2]
math_node_02.outFloat >> math_node_03.floatA
math_node_03.floatB.set(60)

math_node_04 = math_nodes[3]
math_node_03.outFloat >> math_node_04.floatA
clock_face.seconds >> math_node_04.floatB

math_node_05 = math_nodes[4]
math_node_04.outFloat >> math_node_05.floatA
math_node_05.floatB.set(-6)

math_node_05.outFloat >> second_pointer.ry