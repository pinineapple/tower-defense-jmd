
from Tkinter import *
from helper  import *
import random, math

class Vue(object):
    def __init__(self,parent):
        self.root=Tk()
        self.parent=parent
        self.largeur=800
        self.hauteur=600
        self.tourimg = {"tour":PhotoImage(file="./images/tour_40.gif"),"tour_20":PhotoImage(file="./images/tour_20.gif"),
                        "minaret":PhotoImage(file="./images/minaret_40.gif"),"minaret_20":PhotoImage(file="./images/minaret_20.gif"),
                        "lanceur":PhotoImage(file="./images/lanceur_40.gif"),"lanceur_20":PhotoImage(file="./images/lanceur_20.gif"),
                        "paralyseur":PhotoImage(file="./images/paralyseur_40.gif"),"paralyseur_20":PhotoImage(file="./images/paralyseur_20.gif"),
                        "generateur":PhotoImage(file="./images/generateur_40.gif"),"generateur_20":PhotoImage(file="./images/generateur_20.gif")}
        
        self.creepimg= {"generique":PhotoImage(file="./images/generique.gif"),
                        "etoile":PhotoImage(file="./images/creep4.gif"),
                        "tank":PhotoImage(file="./images/tank.gif"),
                        "boss_fantome":PhotoImage(file="./images/boss_fantome.gif")}
        
        self.root.title("Tower defense 2010")
        self.canevas=Canvas(self.root,width=self.largeur,
                            height=self.hauteur,bg="black")
        self.canevas.pack()
        self.cadredata=Frame(self.root,bg="white")
        self.cadreCommande()
        self.cadredata.pack(side=LEFT)
        
    def cadreCommande(self):
        
        self.cadreOption()        
        self.cadreTour()
        self.cadreInfo()
            
        msg=Label(self.cadredata,text="MSG")
        self.msg=Label(self.cadredata,text=" ", bg="yellow")
        msg.pack(side=LEFT)
        self.msg.pack(side=LEFT)
        
    def cadreInfo(self):
        self.cadreinfo=Frame(self.cadredata)
        nbrVague=Label(self.cadreinfo,text="Vague")
        self.nbrVague=Label(self.cadreinfo,text="0")
        nbrVague.grid(column=0,row=0)
        self.nbrVague.grid(column=1,row=0)
        
        pointage=Label(self.cadreinfo,text="Points")
        self.pointage=Label(self.cadreinfo,text="110")
        pointage.grid(column=0,row=1)
        self.pointage.grid(column=1,row=1)
        argent=Label(self.cadreinfo,text="Argent")
        self.argent=Label(self.cadreinfo,text="0")
        argent.grid(column=0,row=2)
        self.argent.grid(column=1,row=2)
        vie=Label(self.cadreinfo,text="Vie")
        self.vie=Label(self.cadreinfo,text="0")
        vie.grid(column=0,row=3)
        self.vie.grid(column=1,row=3)
        self.cadreinfo.pack(side=LEFT)
    
    def cadreOption(self):
        cadreBtn=Frame(self.cadredata,bg="white")
        #self.tour=Button(cadreBtn,text="Tour",image=self.tourimg["tour_20"],command=self.attendTour)
        
        nouvellevague=Button(cadreBtn,text="envoyer vague",command=self.parent.demarrevague)
        nouvellevague.grid(column=0,row=0)
        nouvellepartie=Button(cadreBtn,text="nouvelle partie",command=self.parent.nouvellePartie)
        nouvellepartie.grid(column=0,row=1)
        nouvellepartie=Button(cadreBtn,text="sauver chemin",command=self.sauverChemin)
        nouvellepartie.grid(column=0,row=2)
        
        cadreBtn.pack(side=LEFT)
        
    def sauverChemin(self):
        self.parent.sauverChemin()
        
    def cadreTour(self):
        cadreBtn=Frame(self.cadredata,bg="white")
        #self.tour=Button(cadreBtn,text="Tour",image=self.tourimg["tour_20"],command=self.attendTour)
        self.tour=Button(cadreBtn,image=self.tourimg["tour_20"],command=self.attendTour,relief=GROOVE,bg="white")
        self.tour.grid(column=0,row=0)
        self.tour2=Button(cadreBtn,image=self.tourimg["minaret_20"],command=self.attendMinaret)
        self.tour2.grid(column=0,row=1)
        self.tour3=Button(cadreBtn,image=self.tourimg["lanceur_20"],command=self.attendLanceur)
        self.tour3.grid(column=0,row=2)
        self.tour4=Button(cadreBtn,image=self.tourimg["paralyseur_20"],command=self.attendParalyseur)
        self.tour4.grid(column=1,row=1)
        self.tour5=Button(cadreBtn,image=self.tourimg["generateur_20"],command=self.attendGenerateur)
        self.tour5.grid(column=1,row=2)
        
        self.varDistance = IntVar()
        self.showdistance = Checkbutton(cadreBtn, text="Distance",variable=self.varDistance,command=self.parent.paintTour)
        self.showdistance.grid(column=2,row=0)
        
        self.vendre=Button(cadreBtn,text="vendre",command=self.attendVente)
        self.vendre.grid(column=2,row=1)

        self.update=Button(cadreBtn,text="update",command=self.attendUpdate)
        self.update.grid(column=2,row=2)
        
        cadreBtn.pack(side=LEFT)
        
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
    def attendParalyseur(self):
        self.prochainetour="paralyseur"
        self.canevas.bind("<Button>",self.ajouteTour)  
    def attendGenerateur(self):
        self.prochainetour="generateur"
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
        self.canevas.delete("chemin")
        self.canevas.create_line(modele.chemin,width=2,fill="blue",tags=("chemin"))
        self.cheminActif=modele.chemin
        
    def paintTour(self,modele):
        self.canevas.delete("tour")
        for i in modele.tours:
            self.canevas.create_image(i.x,i.y,anchor=CENTER, image=self.tourimg[i.nom],tags=("tour",str(i.id),i.nom))
            if self.varDistance.get():
                self.canevas.create_oval(i.x-i.rayon,i.y-i.rayon,i.x+i.rayon,i.y+i.rayon,outline="lightyellow",dash=(6, 5, 2, 4),tags=("tour",str(i.id),"rayon",))
            
    def anime(self,modele):
        self.animeCreeps(modele.vagues)
        self.animeTours(modele.tours)
        self.afficheInfo(modele)
        
    def animeCreeps(self,vagues):
        self.canevas.delete("creep")
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
                
    def animeTours(self,tours):
        self.canevas.delete("obus")
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
                    x2,y2= Helper.getAngledPoint(i.angle,i.taille*3,i.x,i.y)  
                    x3,y3= Helper.getAngledPoint(i.angle,i.taille*2,i.x,i.y)  
                    x4,y4= Helper.getAngledPoint(i.angle-math.pi,i.taille,i.x,i.y)  
        
                    self.canevas.create_line(x2,y2,i.x,i.y,fill="red",width=2,tags=("obus","fusee"))
                    self.canevas.create_line(x3,y3,i.x,i.y,fill="red",width=4,tags=("obus","fusee"))
                    self.canevas.create_line(i.x,i.y,x4,y4,fill="yellow",width=2,tags=("obus","fusee"))
                    
                if i.nom=="eclair":
                    x3,y3= Helper.getAngledPoint(i.angle,i.vitesse,i.x,i.y)  
                    x4,y4= Helper.getAngledPoint(i.angle-math.pi,i.vitesse,i.x,i.y)  
                    self.canevas.create_line(x3,y3,i.x,i.y,fill="yellow",tags=("obus","eclair"))
                    self.canevas.create_line(i.x,i.y+1,x4,y4,fill="yellow",tags=("obus","eclair"))
                    
    def  afficheInfo(self,modele):
        self.pointage.config(text=str(modele.pointage))
        self.vie.config(text=str(modele.vie))
        self.argent.config(text=str(modele.argent))
        self.nbrVague.config(text=str(modele.nbrVague))
        
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
  