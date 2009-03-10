
from helper import *
import random
import time
from tower_vue import *
from tower_creeps import *
from tower_tours import *


        
class Jeutour(object):
    def __init__(self,parent):
        self.creepsTypes={"generique":Creep,"etoile":Etoile,"tank":Tank,"boss_fantome":Boss_fantome}
        self.tourTypes={"tour":Tour,"minaret":Minaret,"lanceur":Lanceur,"paralyseur":Paralyseur,"generateur":Generateur}
        self.parent=parent
        #self.chemin=[1,20,20,20,80,20,80,120,180,120,75,233,180,180,100,180,100,240,500,240,500,100,300,100,300,380,600,380]
        
#        self.chemin=[1,20,20,20,80,20,80,120,180,120,75,233,180,180,
#                    100,180,100,240,500,240,500,333,555,182,394,128,321,
#                    234,183,155,371,222,342,100,300,100,300,380,600,380,
#                     700,300,300,300,300,550,800,550]
       # self.chemin=[1,20,400,300,450,300,450,250,350,250,350,350,500,350,500,200,300,200,300,400,550,400,
        #           550,150,250,150,250,550,800,550]
        #self.chemin=[1,20,20,20,800,580]
        self.chemin=[1,20,20,20,20,580,60,580,60,20,100,20,100,580,140,580,140,20,180,20,180,580,
                   220,580,220,20,260,20,260,580,500,580,500,300,700,300,700,100,300,100,300,400,800,400]
        self.chemin=[1,1]
        self.getChemin(800,600)
        chtemp=self.chemin[:]
        self.vagues=[]
        self.vaguesmortes=[]
        self.tours=[]
        self.vie=20
        self.pointage=0
        self.argent=100
        self.cout={"tour":10,"minaret":25,"lanceur":100,"paralyseur":50,"generateur":500}
        self.force=1
        self.point=1
        self.nbrVague=0
        
    def getChemin(self,x,y):
        n= random.randrange(5,15)
        for i in range(n):
            xi=random.randrange(x)
            yi=random.randrange(y)
            self.chemin.append(xi)
            self.chemin.append(yi)
        self.chemin.append(x)
        self.chemin.append(y)

    def vendTour(self,tourid):
        for i in self. tours:
            if i.id==tourid:
                self.argent=self.argent+i.valeur[i.niveau]
                self.tours.remove(i)
                break
        self.parent.paintTour()
        
    def updateTour(self,tourid):
        for i in self.tours:
            if i.id==int(tourid):
                i.update()
                break
        self.parent.paintTour()
            
    def demarreVague(self):
        n= random.randrange(len(self.creepsTypes.keys()))
        ty=self.creepsTypes.keys()[n]
        ct=self.creepsTypes[ty]
        newwave=Vague(self,self.chemin[:],ct,self.force,self.point)
        self.vagues.append(newwave)
        self.force=self.force+3
        self.point=self.point+1
        self.nbrVague=self.nbrVague+1
        self.parent.dessineJeu()
        
    def augmenteTour(self,x,y):
        if self.argent>= self.cout["tour"]:
            self.tours.append(Tour(self,x,y))
            self.parent.paintTour()
            self.argent=self.argent-self.cout["tour"]
        else:
            self.parent.message("Pas assez d'argent")
        
    def ajouteTour(self,x,y,typetour):
        if self.argent>= self.cout[typetour]:
            self.tours.append(self.tourTypes[typetour](self,x,y))
            self.parent.paintTour()
            self.argent=self.argent-self.cout[typetour]
        else:
            self.parent.message("Pas assez d'argent")
            
    def ajouteCreep(self):
        self.vagueNbr=self.vagueNbr-1
        chtemp=self.chemin[:]
        self.creeps.append(Creep(self,chtemp,self.forcecreep,self.point))
        
    def verifieCreep(self):
        for i in self.tours:
            if i.typeobus=="obus" :
                for j in i.obus:
                    for m in self.vagues:
                        for k in m.creeps:
                            if (j.x>k.x and j.x<k.x+k.taille and j.y>k.y and j.y<k.y+k.taille) or ( j.x+j.taille>k.x and j.x+j.taille<k.x+k.taille and j.y+j.taille>k.y and j.y+j.taille<k.y+k.taille):
                                k.force=k.force-j.force
                                if k.force<1:
                                    m.creepmort.append(k)
                                    self.pointage=self.pointage+k.point
                                    self.argent=self.argent+(k.point*1.1)
                                i.obusmort.append(j)
                                break
                            
                        for m in i.obusmort:
                            if m in i.obus:
                                i.obus.remove(m)
                        i.obusmort=[]
            elif i.typeobus=="lazer":
                for j in i.obus:
                    j.cible.force=j.cible.force-j.force
                    if not j.cible.force>0:
                        j.cible.parent.creepmort.append(j.cible)
                        self.pointage=self.pointage+j.cible.point
                        self.argent=self.argent+(j.cible.point*1.1)
                        i.obusmort.append(j)
                            
                    for m in i.obusmort:
                        if m in i.obus:
                            i.obus.remove(m)
                    i.obusmort=[]
            elif i.typeobus=="fusee":
                for j in i.obus:
                     creep=0
                     for v in self.vagues:
                            if j.cible in v.creeps:
                                creep=1
                                break
                     if creep:
                        k=j.cible
                        if (j.x>k.x and j.x<k.x+k.taille and j.y>k.y and j.y<k.y+k.taille) or ( j.x+j.taille>k.x and j.x+j.taille<k.x+k.taille and j.y+j.taille>k.y and j.y+j.taille<k.y+k.taille):
    
                            j.cible.force=j.cible.force-j.force
                            if j.cible.force<1:
                                j.cible.parent.creepmort.append(j.cible)
                                self.pointage=self.pointage+j.cible.point
                                self.argent=self.argent+(j.cible.point*1.1)
                            i.obusmort.append(j)
                     else:
                            i.obusmort.append(j)
                            
                     for m in i.obusmort:
                        if m in i.obus:
                            i.obus.remove(m)
                     i.obusmort=[]            
    def anime(self):
        for i in self.vagues:
            i.anime()
            
        for i in self.tours:
            i.deplace()
                
        for k in self.vagues:
            for i in k.creepmort:
                k.creeps.remove(i)   
            k.creepmort=[] 
            if not k.creeps:
                self.vaguesmortes.append(k)
            
        for i in self.vaguesmortes:
                if i in self.vagues:
                    self.vagues.remove(i)   
            
        for i in self.vagues:
            i.newCreep()
            self.verifieCreep()
            
            for j in self.vagues:
                for i in j.creepmort:
                    if i in j.creeps:
                        j.creeps.remove(i)   
                j.creepmort=[] 
                if not j.creeps:
                    self.vaguesmortes.append(j)
            else:
                if j.vagueNbr>1:
                    j.newCreep()
                    
        for i in self.vaguesmortes:
                if i in self.vagues:
                    self.vagues.remove(i)   
            
        
        self.parent.dessineJeu()
        if self.vie==0:
            self.parent.afficheFinDePartie()
 
          
class Controleur(object):
        def __init__(self):
            self.vue=Vue(self)
            self.timerActif=0
            self.nouvellePartie()
            self.vue.root.mainloop()
        
        def nouvellePartie(self):
            self.vue.root.after_cancel(self.timerActif)
            self.vue.canevas.delete(ALL)
            self.modele=Jeutour(self)
            self.partieActive=1
            self.vue.paintAire(self.modele)
            self.animate()
                
        def paintTour(self):
            self.vue.paintTour(self.modele)
            
        def animate(self):
            if self.partieActive:
                if len(self.modele.vagues)==0:
                    self.modele.demarreVague()
                self.modele.anime()
            self.timerActif=self.vue.root.after(50,self.animate)
            
        def dessineJeu(self):
            self.vue.anime(self.modele)
        
        def demarrevague(self):
            self.modele.demarreVague()
        
        def ajoutetour(self,x,y,typetour):
            self.modele.ajouteTour(x,y,typetour)
            
        def message(self,txt):
            self.vue.afficheMessage(txt)
            
        def afficheFinDePartie(self):
            self.partieActive=0
            self.vue.afficheFinDePartie(self.modele)
            
        def vendTour(self,tourid):
            self.modele.vendTour(tourid)
        def updateTour(self,tourid):
            self.modele.updateTour(tourid)

def testDistance():
    n= Helper.calcDistance(200,20,360,50)
    print n
    
def testAngle():
    n= Helper.calcDistance(20,20,600,380)
    print Helper.getAngledPoint(n, 5, 20,20)
    
def fusee():
    root=Tk()
    can=Canvas(root,width=500,height=400,color="white")
    can.create_polygon(10,10)
    
if __name__ == '__main__':
    cont=Controleur()
    #testAngle()
    #testDistance()