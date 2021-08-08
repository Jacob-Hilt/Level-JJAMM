#type = 0, dead; type = 1, stationary; type = 2, move along x pos; type = 3, move along y pos
class creature:
    typ = 0
    xpos = 0
    ypos = 0
    alive = 1
    direction = 1

    def __init__(self):
        typ = 1

    def movement(self, mapObj):
        if(self.alive == 0):
            #mapObj.objArr[self.ypos][self.xpos] = '-'
            return [0, mapObj]
        if(self.typ == 0 or self.typ == 1):
            return [1, mapObj]
        
        #moves along the x pos
        if(self.typ == 2):
            desx = 0
            if(self.direction == 1):
                desx = self.xpos + 1
            else:
                desx = self.xpos - 1
            
            if(desx >= mapObj.maxX or desx < 0):
                self.direction = self.direction * -1
                return [0, mapObj]

            if(mapObj.objArr[self.ypos][desx] == '-'):
                mapObj.objArr[self.ypos][desx] = str(self.typ)
                mapObj.objArr[self.ypos][self.xpos] = '-'
                self.xpos = desx
                return [1, mapObj]

            # add a kill player here
            if(mapObj.objArr[self.ypos][desx] == 'p'):
                return [2, mapObj]

            else:
                self.direction = self.direction * -1
                return [0, mapObj]

        #moves along the y pos
        if(self.typ == 3):
            desy = 0
            if(self.direction == 1):
                desy = self.ypos + 1
            else:
                desy = self.ypos - 1
            
            if(desy >= mapObj.maxY or desy < 0):
                self.direction = self.direction * -1
                return [0, mapObj] 

            if(mapObj.objArr[desy][self.xpos] == '-'):
                mapObj.objArr[desy][self.xpos] = str(self.typ)
                mapObj.objArr[self.ypos][self.xpos] = '-'
                self.ypos = desy
                return [1, mapObj]

            # add a kill player here
            if(mapObj.objArr[desy][self.xpos] == 'p'):
                return [2, mapObj]

            else:
                self.direction = self.direction * -1
                return [0, mapObj]

        return [1, mapObj]

        
    def dead(self):
        self.alive = 0
        return 1
    
    def status(self):
        return self.alive
