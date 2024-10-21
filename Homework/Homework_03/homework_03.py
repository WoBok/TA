import pymel.core as pm
import math

brickSize = {'w': 0.053, 'd': 0.24, 'h': 0.115}

radius = 1
height = 3

if pm.objExists('bricks'):
    bricks = pm.PyNode('bricks')
else:
    bricks = pm.group(n='bricks')
originPoint = bricks.getTranslation(s='world')

currentRad = 0
layers = 0
yOffset = originPoint.y + brickSize['h']/2
y = yOffset
rad = brickSize['d'] / radius

while y <= height + yOffset:
    while currentRad <= 2 * math.pi:
        currentLayerRad = currentRad + layers * rad / 2
        currentRad += rad

        x = radius * math.cos(currentLayerRad) + originPoint.x
        z = radius * math.sin(currentLayerRad) + originPoint.z

        cube = pm.polyCube(w=brickSize['w'], d=brickSize['d'], h=brickSize['h'])
        cube[0].scalePivot.set(brickSize['w']/2,-brickSize['h']/2,-brickSize['d']/2)
        cube[0].rotatePivot.set(brickSize['w']/2,-brickSize['h']/2,-brickSize['d']/2)
        cube[0].translate.set(x, y, z)
        cube[0].rotateY.set(-math.degrees(currentLayerRad+rad/2))
        
        pm.parent(cube[0], bricks)
    currentRad = 0
    layers += 1
    y += brickSize['h']