# Joint effort by: Jerry Smedley, Jacob Hilt, Melissa Barnes, Mark Montes, Anthony Chin
# This work is made available under the "MIT License". Please see the file LICENSE in this
# distribution for license terms.

# type = 0, dead; type = 1, stationary; type = 2, move along x pos; type = 3, move along y pos
class creature:
    typ = 0
    xpos = 0
    ypos = 0
    alive = 1
    direction = 1

    def __init__(self):
        typ = 1

    def movement(self, mapObj):
        if self.alive == 0:
            # mapObj.objArr[self.ypos][self.xpos] = '-'
            return [0, mapObj]
        if self.typ == 0 or self.typ == 1:
            return [1, mapObj]

        # moves along the x pos
        if self.typ == 2:
            return moveEnemy(self, mapObj, self.typ)

        # moves along the y pos
        if self.typ == 3:
            return moveEnemy(self, mapObj, self.typ)
        return [1, mapObj]

    def dead(self):
        self.alive = 0
        return 1

    def status(self):
        return self.alive


def moveEnemy(self, mapObj, selfType):
    if selfType ==2:
        selfPos = self.xpos
        maxVar = mapObj.maxX
    if selfType ==3:
        selfPos = self.ypos
        maxVar = mapObj.maxY
		
    desVar = 0
    if self.direction == 1:
        desVar = selfPos + 1
    else:
        desVar = selfPos - 1

    if desVar >= maxVar or desVar < 0:
        self.direction = self.direction * -1
        return [0, mapObj]
				
    if selfType ==2:
        left = self.ypos
        right = desVar
    if selfType ==3:
        left = desVar
        right = self.xpos
				
    if mapObj.objArr[left][right] == '-':
        mapObj.objArr[left][right] = str(selfType)
        mapObj.objArr[self.ypos][self.xpos] = '-'
        if selfType ==2: 
            self.xpos = desVar 
        if selfType ==3: 
            self.ypos = desVar 
        return [1, mapObj]

    # add a kill player here
    if mapObj.objArr[left][right] == 'p':
        return [2, mapObj]

    else:
        self.direction = self.direction * -1
        return [0, mapObj]