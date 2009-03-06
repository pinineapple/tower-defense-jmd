from Tkinter import *
import math
import random
import time

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
   
class Tour(object):
    no=0
    def __init__(self,parent,x=100,y=100,rayon=100,point=1):
        self.id=Tour.no
        Tour.no=Tour.no+1
        self.nom="tour"
        self.typeobus="obus"
        self.parent=parent
        self.rythme=10
        self.etat=self.rythme
        self.x=x
        self.y=y
        self.taille=16
        self.rayon=rayon
        self.puissance=1
        self.obus=[]
        self.obusmort=[]
        self.force=1
        self.niveau=1
        self.cout={2:10,3:25,4:60,5:100}
        self.vitesse=20
        self.point=point
        self.valeur={1:7,2:14,3:21,4:28,5:35,20:100}
        
    def update(self):
        n=self.niveau+1
        if n in self.cout and self.parent.argent>= self.cout[n]:
            self.niveau=self.niveau+1
            self.force=self.force*2
            self.rayon=self.rayon+50
            self.vitesse=self.vitesse*1.1
            if self.rythme>1:
                self.rythme=self.rythme-1
            self.parent.argent=self.parent.argent-self.cout[n]
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
     
class Lanceur(Tour):
    def __init__(self,parent,x=100,y=100,rayon=100,point=1):
        Tour.__init__(self,parent,x,y,rayon,point) 
        self.nom="lanceur"
        self.typeobus="fusee"       
        self.rythme=40 
        self.vitesse=5
        self.rayon=self.rayon*2
        
    def update(self):
        n=self.niveau+1
        if n in self.cout and self.parent.argent>= self.cout[n]:
            self.niveau=self.niveau+1
            self.force=self.force*2
            self.rayon=self.rayon+70
            self.vitesse=self.vitesse*1.1
            if self.rythme>1:
                self.rythme=self.rythme-4
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
        self.taille=4
        self.distance=self.parent.rayon
        self.force=self.parent.force
        
    def deplace(self):        
        dist=Helper.calcDistance(self.x,self.y,self.xo,self.yo)
        if dist>self.distance:
            self.parent.obusmort.append(self)
        self.x,self.y= Helper.getAngledPoint(self.angle,self.vitesse,self.x,self.y)
        
class Lazer(Obus):
    def __init__(self, parent,cible,typeobus):
        Obus.__init__(self, parent, cible, typeobus)
        self.force=self.parent.force/10.0
        
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
  
class Vague(object):
    def __init__(self,parent,chemin,typeCreep,force,point):
        self.parent=parent    
        self.chemin=chemin
        self.creeps=[typeCreep(self,self.chemin[:],force,point)]
        self.vagueNbr=3
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
        print "VAGUE",self,self.vagueNbr
        
class Jeutour(object):
    def __init__(self,parent):
        self.creepsTypes={"generique":Creep,"etoile":Etoile,"tank":Tank}
        self.tourTypes={"tour":Tour,"minaret":Minaret,"lanceur":Lanceur}
        self.parent=parent
        #self.chemin=[1,20,20,20,80,20,80,120,180,120,75,233,180,180,100,180,100,240,500,240,500,100,300,100,300,380,600,380]
        
#        self.chemin=[1,20,20,20,80,20,80,120,180,120,75,233,180,180,
#                    100,180,100,240,500,240,500,333,555,182,394,128,321,
#                    234,183,155,371,222,342,100,300,100,300,380,600,380,
#                     700,300,300,300,300,550,800,550]
        self.chemin=[1,20,400,300,450,300,450,250,350,250,350,350,500,350,500,200,300,200,300,400,550,400,
                   550,150,250,150,250,550,800,550]
        #self.chemin=[1,20,20,20,800,580]
        #self.chemin=[1,20,20,20,20,580,60,580,60,20,100,20,100,580,140,580,140,20,180,20,180,580,
        #           220,580,220,20,260,20,260,580]
        chtemp=self.chemin[:]
        self.vagues=[]
        self.vaguesmortes=[]
        self.tours=[]
        self.vie=20
        self.pointage=0
        self.argent=100
        self.cout={"tour":10,"minaret":25,"lanceur":100}
        self.force=1
        self.point=1

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
                    if j.cible.force<1:
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
        self.point=self.point*20
        self.vitesse=self.vitesse*0.7
        
class Vue(object):
    def __init__(self,parent):
        self.parent=parent
        self.largeur=800
        self.hauteur=600
        self.root=Tk()
        self.canevas=Canvas(self.root,width=self.largeur,
                            height=self.hauteur,bg="black")
        self.canevas.pack()
        self.cadredata=Frame(self.root)
        self.initcadredata()
        self.cadredata.pack(side=LEFT)
        
        self.tourimg = {"tour":PhotoImage(file="tour.gif"),"minaret":PhotoImage(file="minaret.gif"),"lanceur":PhotoImage(file="lanceur.gif")}
        
        self.creepimg= {"generique":PhotoImage(file="generique.gif"),"etoile":PhotoImage(file="creep4.gif"),"tank":PhotoImage(file="tank.gif")}
        
    def initcadredata(self):
        pointage=Label(self.cadredata,text="Points")
        self.pointage=Label(self.cadredata,text="110")
        pointage.pack(side=LEFT)
        self.pointage.pack(side=LEFT)
        argent=Label(self.cadredata,text="Argent")
        self.argent=Label(self.cadredata,text="0")
        argent.pack(side=LEFT)
        self.argent.pack(side=LEFT)
        vie=Label(self.cadredata,text="Vie")
        self.vie=Label(self.cadredata,text="0")
        vie.pack(side=LEFT)
        self.vie.pack(side=LEFT)
        
        nouvellevague=Button(self.cadredata,text="envoyer vague",command=self.parent.demarrevague)
        nouvellevague.pack(side=LEFT)
        
        vente=Button(self.cadredata,text="vendre",command=self.attendVente)
        vente.pack(side=LEFT)
        cadreBtn=Frame(self.cadredata)
        tour=Button(cadreBtn,text="Tour",command=self.attendTour)
        tour.grid(column=0,row=0)
        tour2=Button(cadreBtn,text="Minaret",command=self.attendMinaret)
        tour2.grid(column=0,row=1)
        tour2=Button(cadreBtn,text="Lanceur",command=self.attendLanceur)
        tour2.grid(column=0,row=2)
        cadreBtn.pack(side=LEFT)
        update=Button(self.cadredata,text="augmenter",command=self.attendUpdate)
        update.pack(side=LEFT)
            
        msg=Label(self.cadredata,text="MSG")
        self.msg=Label(self.cadredata,text=" ", bg="yellow")
        msg.pack(side=LEFT)
        self.msg.pack(side=LEFT)
        
        self.varDistance = IntVar()
        self.showdistance = Checkbutton(self.cadredata, text="Distance",variable=self.varDistance,command=self.parent.paintTour)
        self.showdistance.pack(side=LEFT)

        
    def attendVente(self):
        self.canevas.bind("<Button>",self.vendTour)    
      # je veux mettre des minaret - qu'est-ce que je passe au bouton, un type ???  
    def attendTour(self):
        self.prochainetour="tour"
        self.canevas.bind("<Button>",self.ajouteTour)       
    def attendMinaret(self):
        self.prochainetour="minaret"
        self.canevas.bind("<Button>",self.ajouteTour)   
    def attendLanceur(self):
        self.prochainetour="lanceur"
        self.canevas.bind("<Button>",self.ajouteTour)  
        
    def attendUpdate(self):
        self.canevas.tag_bind(("tour",),"<Button>",self.updateTour) 
    
    def vendTour(self,evt):
        obj=self.canevas.find_withtag(CURRENT)
        sestags=self.canevas.gettags(obj[0])
        self.parent.vendTour(int(sestags[1]))
        
    def ajouteTour(self,evt):
        x=evt.x
        y=evt.y
        x=self.canevas.canvasx(x)
        y=self.canevas.canvasx(y)
        self.canevas.unbind("<Button>")
        self.parent.ajoutetour(x,y,self.prochainetour)
        
    def updateTour(self,evt):
        obj=self.canevas.find_withtag(CURRENT)
        if obj:
            sestags=self.canevas.gettags(obj[0])
            self.canevas.tag_unbind("tour","<Button>")
            self.parent.updateTour(sestags[1])
        
    def paintAire(self,modele):
        self.canevas.create_line(modele.chemin,width=2,fill="blue")
        
    def paintTour(self,modele):
        self.canevas.delete("tour")
        for i in modele.tours:
            self.canevas.create_image(i.x,i.y,anchor=CENTER, image=self.tourimg[i.nom],tags=("tour",str(i.id),i.nom))
            if self.varDistance.get():
                self.canevas.create_oval(i.x-i.rayon,i.y-i.rayon,i.x+i.rayon,i.y+i.rayon,outline="lightyellow",dash=(6, 5, 2, 4),tags=("tour",str(i.id),"rayon",))
            
    def anime(self,vagues,tours,pointage,vie,argent):
        self.canevas.delete("creep")
        self.canevas.delete("obus")
        self.canevas.delete("creeplife")
        for j in vagues:
            for i in j.creeps:
                self.canevas.create_image(i.x,i.y,anchor=CENTER, image=self.creepimg[i.nom],tags=("creep",str(i.id)))
                vert=float(i.force)/float(i.forceorigine)*10.0
                rouge=10-vert
                v1=-1
                v2=vert-1
                r1=v2
                r2=9
                self.canevas.create_line(i.x+v1,i.y-12,i.x+v2,i.y-12,fill="lightblue",width=2,tags=("creeplife","green"))
                self.canevas.create_line(i.x+r1,i.y-12,i.x+r2,i.y-12,fill="red",width=2,tags=("creeplife","red"))
        for j in tours:
            for i in j.obus:
                if i.nom=="obus":
                    self.canevas.create_oval(i.x,i.y,i.x+i.taille,i.y+i.taille,outline="yellow",fill="red",tags=("obus"))
                elif i.nom=="lazer":
                    self.canevas.create_line(i.x,i.y,i.cible.x,i.cible.y,fill="lightgreen",width=2,tags=("obus","lazer"))
                    self.canevas.create_line(i.x+1,i.y+1,i.cible.x-1,i.cible.y-1,fill="yellow",tags=("obus","lazer"))
                    self.canevas.create_line(i.x-1,i.y-1,i.cible.x+1,i.cible.y+1,fill="red",tags=("obus","lazer"))
                    self.flameche(i.cible.x,i.cible.y)
                elif i.nom=="fusee":
                    
                    dist=Helper.calcDistance(i.cible.x,i.cible.y,i.x,i.y)
                    i.angle=Helper.calcAngle(i.x,i.y,i.cible.x,i.cible.y)  
                    x2,y2= Helper.getAngledPoint(i.angle,i.vitesse*3,i.x,i.y)  
                    x3,y3= Helper.getAngledPoint(i.angle,i.vitesse*2,i.x,i.y)  
                    x4,y4= Helper.getAngledPoint(i.angle-180,i.vitesse,i.x,i.y)  
        
                    self.canevas.create_line(x2,y2,i.x,i.y,fill="red",width=2,tags=("obus","fusee"))
                    self.canevas.create_line(x3,y3,i.x,i.y,fill="red",width=4,tags=("obus","fusee"))
                    self.canevas.create_line(i.x,i.y,x4,y4,fill="yellow",width=2,tags=("obus","fusee"))
                    
                
        self.pointage.config(text=str(pointage))
        self.vie.config(text=str(vie))
        self.argent.config(text=str(argent))
    def flameche(self,x,y):
        n=random.randrange(2,4)
        d=12
        x1=x-d
        y1=y-d
        for i in range(n):
            x2=random.randrange(d*2)
            y2=random.randrange(d*2)
            self.canevas.create_rectangle(x1+x2,y1+y2,x1+x2+1,y1+y2+1,fill="yellow",outline="yellow",tags=("obus","lazer","flameche"))
        
    def afficheMessage(self,txt):
        self.msg.config(text=txt)
        
    def afficheFinDePartie(self,modele):
        self.afficheMessage("FINI _PERDU")
            
class Controleur(object):
        def __init__(self):
            self.modele=Jeutour(self)
            self.partieActive=1
            self.vue=Vue(self)
            self.vue.paintAire(self.modele)
            
            self.animate()
            self.vue.root.mainloop()
            
        def paintTour(self):
            self.vue.paintTour(self.modele)
        def animate(self):
            if self.partieActive:
                if len(self.modele.vagues)==0:
                    self.modele.demarreVague()
                self.modele.anime()
            self.vue.root.after(50,self.animate)
            
        def dessineJeu(self):
            self.vue.anime(self.modele.vagues,self.modele.tours,self.modele.pointage,self.modele.vie,self.modele.argent)
        
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