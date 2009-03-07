import math

class Helper(object):
    def getAngledPoint(ang,longueur,cx,cy):
        t = ang*math.pi/180.0
        x = (math.cos(t)*longueur)+cx
        y = (math.sin(t)*longueur)+cy
        return (x,y)
    getAngledPoint = staticmethod(getAngledPoint)
    
    def calcAngle(x1,y1,x2,y2):
         dx = x2-x1
         dy = y2-y1
         angle = (math.atan2(dy,dx) % (2*math.pi)) * (180/math.pi)
         return angle
    calcAngle = staticmethod(calcAngle)
    
    def calcDistance(x1,y1,x2,y2):
         dx = abs(x2-x1)**2
         dy = abs(y2-y1)**2
         distance=math.sqrt(dx+dy)
         return distance
    calcDistance = staticmethod(calcDistance)