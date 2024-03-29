from helper import *
import random
import time   
   
class Tour(object):
    no=0
    def __init__(self,parent,x=100,y=100,rayon=100,point=1):
        self.id=Tour.no
        Tour.no=Tour.no+1
        self.nom="tour"
        self.typeobus="obus"
        self.parent=parent
        self.rythme=40
        self.etat=self.rythme
        self.x=x
        self.y=y
        self.taille=16
        self.rayon=rayon
        self.puissance=1
        self.obus=[]
        self.obusmort=[]
        self.force=1
        self.niveauDistance=1
        self.coutDistance={2:10,3:25,4:60,5:100}
        self.niveauForce=1
        self.coutForce={2:10,3:25,4:60,5:100}
        self.vitesse=9
        self.point=point
        self.valeur={1:7,2:14,3:21,4:28,5:35,20:100,}
        
    def updateDistance(self):
        n=self.niveauDistance+1
        if n in self.coutDistance and self.parent.argent>= self.coutDistance[n]:
            self.niveauDistance=self.niveauDistance+1
            self.rayon=self.rayon+50
            self.vitesse=self.vitesse*1.1
            if self.rythme>1:
                self.rythme=self.rythme-1
            self.parent.argent=self.parent.argent-self.coutDistance[n]
        else:
            self.parent.parent.message("Pas assez d'argent")
        self.parent.parent.paintTour()
        
    def updateForce(self):
        n=self.niveauForce+1
        if n in self.coutForce and self.parent.argent>= self.coutForce[n] :
            self.niveauForce=self.niveauForce+1
            self.force=self.force*2
            self.parent.argent=self.parent.argent-self.coutForce[n]
        else:
            self.parent.parent.message("Pas assez d'argent")
        self.parent.parent.paintTour()
        
    def chasseCreeps(self,vagues):
        creeps=[]
        for j in vagues:
            for i in j.creeps:
                distance=Helper.calcDistance(self.x,self.y,i.x,i.y)
                if distance < self.rayon:
                    creeps.append(i)
        if creeps:
            i=creeps[random.randrange(len(creeps))]
            if self.typeobus=="obus":
                self.obus.append(Obus(self,i,self.typeobus))
            elif self.typeobus=="lazer" and len(self.obus)==0:
                self.obus.append(Lazer(self,i,self.typeobus))
            elif self.typeobus=="fusee":
                self.obus.append(Fusee(self,i,self.typeobus))
            elif self.typeobus=="eclair":
                self.obus.append(Eclair(self,i,self.typeobus))
            return
            
    def deplace(self):
        if self.etat==0:
            self.chasseCreeps(self.parent.vagues)
            self.etat=self.rythme
        else:
            self.etat=self.etat-1

        for i in self.obus:
            i.deplace()
            
        for i in self.obusmort:
            if i in self.obus:
                self.obus.remove(i)
        self.obusmort=[]
        
class Minaret(Tour):
    def __init__(self,parent,x=100,y=100,rayon=100,point=1):
        Tour.__init__(self,parent,x,y,rayon,point) 
        self.nom="minaret"
        self.typeobus="lazer"
        self.cout={2:100,3:250,4:600,5:1000}
        
    def update(self):
        n=self.niveau+1
        if n in self.cout and self.parent.argent>= self.cout[n]:
            self.niveau=self.niveau+1
            self.force=self.force*1.5
            self.rayon=self.rayon+30
            if self.rythme>1:
                self.rythme=self.rythme-1
            self.parent.argent=self.parent.argent-self.cout[n]
        else:
            self.parent.parent.message("Pas assez d'argent")
        self.parent.parent.paintTour()
        
class Paralyseur(Tour):
    def __init__(self,parent,x=100,y=100,rayon=100,point=1):
        Tour.__init__(self,parent,x,y,rayon,point) 
        self.nom="paralyseur"
        self.typeobus="eclair"
        self.cout={2:300,3:500}
     
class Generateur(Tour):
    def __init__(self,parent,x=100,y=100,rayon=100,point=1):
        Tour.__init__(self,parent,x,y,rayon,point) 
        self.nom="generateur"
        self.typeobus="onde"       
  
class Lanceur(Tour):
    def __init__(self,parent,x=100,y=100,rayon=100,point=1):
        Tour.__init__(self,parent,x,y,rayon,point) 
        self.nom="lanceur"
        self.typeobus="fusee"   
        self.taille=3
        self.vitesse=5
        self.rythme=50
        self.etat=self.rythme
        self.force=self.force*10
        self.cout={2:250,3:600,4:600,5:1200}
              
    def update(self):
        n=self.niveau+1
        if n in self.cout and self.parent.argent>= self.cout[n]:
            self.niveau=self.niveau+1
            self.force=self.force*2
            self.rayon=self.rayon+70
            self.vitesse=self.vitesse*1.1
            if self.rythme>1:
                self.rythme=self.rythme-1
            self.parent.argent=self.parent.argent-self.cout[n]
        else:
            self.parent.parent.message("Pas assez d'argent")
        self.parent.parent.paintTour()

class Obus(object):
    def __init__(self, parent,cible,typeobus):
        self.parent=parent
        self.cible=cible
        self.nom=typeobus
        self.dx=cible.x
        self.dy=cible.y
        self.x=parent.x
        self.y=parent.y
        self.xo=self.x
        self.yo=self.y
        self.angle=Helper.calcAngle(self.x,self.y,self.dx,self.dy)
        self.vitesse=self.parent.vitesse
        self.taille=6
        self.distance=self.parent.rayon
        self.force=self.parent.force
        self.hit=0
        
    def deplace(self):        
        dist=Helper.calcDistance(self.x,self.y,self.xo,self.yo)
        if dist>self.distance:
            self.parent.obusmort.append(self)
        self.x,self.y= Helper.getAngledPoint(self.angle,self.vitesse,self.x,self.y)
        
class Lazer(Obus):
    def __init__(self, parent,cible,typeobus):
        Obus.__init__(self, parent, cible, typeobus)
        self.force=self.parent.force/33.0
        
    def deplace(self):
        dist=Helper.calcDistance(self.cible.x,self.cible.y,self.xo,self.yo)
        if dist>self.distance:
            self.parent.obusmort.append(self)
 
class Fusee(Obus):
    def __init__(self, parent,cible,typeobus):
        Obus.__init__(self, parent, cible, typeobus)
        
    def deplace(self):
        self.angle=Helper.calcAngle(self.x,self.y,self.cible.x,self.cible.y)
        self.x,self.y= Helper.getAngledPoint(self.angle,self.vitesse,self.x,self.y)       
  
class Eclair(Obus):
    def __init__(self, parent,cible,typeobus):
        Obus.__init__(self, parent, cible, typeobus)
        self.taille=4
        self.ralentisseur=0.9
        self.force=self.parent.force/10.0
        self.vitesse=self.vitesse*1.2