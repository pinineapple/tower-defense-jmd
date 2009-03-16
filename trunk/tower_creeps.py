from helper import *

class Vague(object):
    def __init__(self,parent,chemin,typeCreep,force,point):
        self.parent=parent    
        self.chemin=chemin
        self.creeps=[typeCreep(self,self.chemin[:],force,point)]
        self.vagueNbr=10
        if typeCreep==Boss_fantome:
            self.vagueNbr=1
        self.creeptype=typeCreep
        self.point=point
        self.force=force
        self.creepmort=[]
        
    def anime(self):
            for i in self.creeps:
                i.deplace()
        
    def newCreep(self):
        if self.creeps and self.vagueNbr>1:
            i=self.creeps[len(self.creeps)-1]
            if i.espace>(i.taille*1.5) :
                self.prochainCreep()
                self.vagueNbr=self.vagueNbr-1
        elif not self.creeps:
            self.prochainCreep()
            self.vagueNbr=self.vagueNbr-1
                
    def prochainCreep(self):
        self.creeps.append(self.creeptype(self,self.chemin[:],self.force,self.point))
        #print "VAGUE",self,self.vagueNbr

class Creep(object):
    no=0
    def __init__(self,parent,chemin,force,point):
        self.id=Creep.no
        self.nom="generique"
        Creep.no=Creep.no+1
        self.parent=parent
        self.chemin=chemin
        self.x=self.chemin.pop(0)
        self.y=self.chemin.pop(0)
        self.setPath()
        self.espace=0
        self.vitesse=3
        self.taille=10
        self.force=force
        self.forceorigine=force
        self.point=point
        
    def setPath(self):
        self.dx=self.chemin.pop(0)
        self.dy=self.chemin.pop(0)
        self.angle=Helper.calcAngle(self.x,self.y,self.dx,self.dy)
        
    def deplace(self):
        self.x,self.y= Helper.getAngledPoint(self.angle,self.vitesse,self.x,self.y)
        if self.x>self.dx-self.vitesse and self.x<self.dx+self.vitesse and self.y>self.dy-self.vitesse and self.y<self.dy+self.vitesse:
            if self.chemin:
                self.setPath()
            else:
                self.parent.creepmort.append(self)
                self.parent.parent.vie=self.parent.parent.vie-1                    
        self.espace=self.espace+self.vitesse
 
class Etoile(Creep):
    def __init__(self,parent,chemin,force,point):
        Creep.__init__(self,parent,chemin,force,point) 
        self.nom="etoile"           
        self.force=self.force*0.5
        self.forceorigine=self.force
        self.point=self.point*1.4
        self.vitesse=self.vitesse*1.5
        
class Tank(Creep):
    def __init__(self,parent,chemin,force,point):
        Creep.__init__(self,parent,chemin,force,point) 
        self.nom="tank"           
        self.force=self.force*0.5
        self.forceorigine=self.force
        self.point=self.point*2
        self.vitesse=self.vitesse*0.7

class Boss_fantome(Creep):
    def __init__(self,parent,chemin,force,point):
        Creep.__init__(self,parent,chemin,force,point) 
        self.nom="boss_fantome"           
        self.force=self.force*10
        self.forceorigine=self.force
        self.point=self.point*100
        self.vitesse=self.vitesse*0.5
        