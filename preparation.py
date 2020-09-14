import fromage
from fromage import *
import numpy as np
import pandas as pd

import time
#### Modèle thermique
palette = palette()
produit = produit()
#path = "/home/loisel/simulation-rupture-janvier2020/"
#name ="index_simulation3000_ANIA.csv"
#N = 1
def preparation(N,source_donnees,path):
    name = "simulation_" + source_donnees + "_" + str(N)

    t0 = time.time()
    headers = ["T_produit_zone"+str(i) for i in range(1,19)]\
        + ["T_air_zone"+str(i) for i in range(1,19)]\
        + ["Rupture"]\
        + ["T_air"]\
        + ["T"]\
        + ["No"]
    data = pd.DataFrame(columns=headers)



    data.to_csv(path+name, header=1)

    for i in range(N):

        circuit=np.random.randint(8,size=1)
        chaine = objects.chaine(circuit=circuit,donnees=source_donnees)
        T,T_air,liste_stages,ccbreak_bool=constructT_air_avec_rupture_chaine(chaine=chaine)
        Tprod,T_az=calculs.calcul_profils(palette,produit,T_air)
        #####
        Tprod = pd.DataFrame(Tprod.T,\
                             columns=["T_produit_zone"+str(k) for k in range(1,19)])
        T_az= pd.DataFrame(T_az.T,\
                             columns=["T_air_zone"+str(k) for k in range(1,19)])
        ccbreak_bool = pd.DataFrame(ccbreak_bool,\
                             columns=["Rupture"])

        T_air = pd.DataFrame(T_air,\
                             columns = ["T_air"])

        data = pd.concat([Tprod,T_az,ccbreak_bool,T_air],axis=1)
        data["T"]=T
        data["No"]=i
        data.to_csv(path+name,mode='a',header=None)
        del data

    return name
    print("temps écoulé : {:.2f} min ".format((time.time()-t0)/60))
    print("ok")
    #print(data.columns)
    #print(data["Rupture"])

