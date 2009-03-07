
from Tkinter import *
from helper  import *
import random

class Vue(object):
    def __init__(self,parent):
        self.parent=parent
        self.largeur=800
        self.hauteur=600
        self.root=Tk()
        self.root.title("Tower defense 2010")
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
  