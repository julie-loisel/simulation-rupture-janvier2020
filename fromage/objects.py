#objects
from fromage import utils

class palette:
    def __init__(self,config=1,l=0.57,L=0.25,nb_l=3,nb_L=2,Q=0.0,C_vent=1):
        self.l=l #longueur d'un carton
        self.L=L #largeur d'un carton
        self.nb_l=nb_l #nombre de zones dans un carton en longueur
        self.nb_L=nb_L #nombre de zones dans un carton en longueur
        self.config=config #configuration, 1 ou 2
        self.Dz=0.14#hauteur carton
        self.dz=0.025#hauteur lame d'air
        if config==1:
            self.I=nb_l
            self.J=3*nb_L
            self.Dx,self.Dy=l,3*L
        if config==2:
            self.I=int(1.5*nb_L)
            self.J=2*nb_l
            self.Dx,self.Dy=1.5*L,2*l
            
        self.dx,self.dy=self.Dx/self.I,self.Dy/self.J
        self.C_vent=C_vent
        self.Sx,self.Sy=utils.construct_Sx_Sy(config,C_vent)
        self.Q=Q#puissance thermique par maille, 0 = pas de chauffe
        self.nb_zones=nb_L*nb_l
class produit:
    def __init__(self,Tinit=4,Nproduit=10,poids=0.25,Cp_p=3200,Sp=0.0820325,h=5,rho=1.25,palette=palette()):
        self.Tinit=Tinit#température initiale du profuit
        self.Nproduit=Nproduit
        self.poids=poids
        self.Cp_p=Cp_p #Heat capacity
        self.Sp=Sp # m² Surface d'échange par zone en air et produit
        self.h=h #W m-2 °C-1 ; coefficient d'échange convectif
        self.mp=poids*Nproduit/palette.nb_zones#% kg - masse produit par zone 
        self.rho=rho

class chaine:
    def __init__(self, stages=["plateforme","camion","chambre"], donnees="derens_2009",circuit=0):
        self.stages=stages
        self.donnees=donnees
        self.dict_donnees={
            'ANIA':{'transport':\
                             {'duree':{'loi':'exponential','lambda':0.2},
                              'intensite':{'loi':'normal','loc':2.9,'scale':1.4}},\
                          'warehouse':\
                              {'duree':{'loi':'exponential','lambda':3.2},
                              'intensite':{'loi':'normal','loc':2.3,'scale':0.8}}, \
                          'platform': \
                              {'duree': {'loi':'exponential', 'lambda':1.2},
                              'intensite': {'loi':'normal', 'loc':3.2, 'scale':1.3}}, \
                          'cold_room': \
                              {'duree': {'loi': 'exponential', 'lambda': 1.6},
                              'intensite': {'loi': 'normal', 'loc': 3.4, 'scale': 1.7}
                            }
        },
        'derens_2009': {'transport':\
                             {'duree':{'loi':'exponential','lambda':0.076},
                              'intensite':{'loi':'normal','loc':3.6,'scale':2.7}},\
                          'warehouse':\
                              {'duree':{'loi':'exponential','lambda':0.7},
                              'intensite':{'loi':'normal','loc':3.6,'scale':2.8}}, \
                          'platform': \
                              {'duree': {'loi':'exponential', 'lambda':0.49},
                              'intensite': {'loi':'normal', 'loc':2.9, 'scale':2.9}}, \
                          'cold_room': \
                              {'duree': {'loi':'exponential', 'lambda':0.95},
                              'intensite': {'loi':'normal', 'loc':4.4, 'scale':1.9}}
        }
                        }
        self.circuit=circuit



