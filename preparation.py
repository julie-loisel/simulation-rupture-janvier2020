import fromage
from fromage import *
import numpy as np
import pandas as pd
import adtk
import sklearn
import matplotlib.pyplot as plt
from adtk.detector import ThresholdAD
from adtk.data import validate_series
from adtk.metrics import recall,precision,iou,f1_score
from adtk.data import to_events
import time
#### Modèle thermique
palette = palette()
produit = produit()

# data["T"] = pd.DatetimeIndex(data["T"])
# print(data.dtypes)
# print(data)
# thresh = ThresholdAD(high = 5, low=-2)
# anomalies = thresh.detect(data.loc[0].set_index("T")["T_produit_zone1"])
# true = data.loc[0].set_index("T")["Rupture"]
# print(precision(true,anomalies))
t0 = time.time()
for i in range(30):
    circuit=np.random.randint(8,size=1)
    chaine = objects.chaine(circuit=circuit)
    T,T_air,liste_stages,ccbreak_bool=constructT_air_avec_rupture_chaine(chaine=chaine)
    Tprod,T_az=calculs.calcul_profils(palette,produit,T_air)
    #####
    Tprod = pd.DataFrame(Tprod.T,\
                         columns=["T_produit_zone"+str(i) for i in range(1,19)],\
                         index = np.full(len(T),i,dtype=int))
    T_az= pd.DataFrame(T_az.T,\
                         columns=["T_air_zone"+str(i) for i in range(1,19)],\
                         index = np.full(len(T),i,dtype=int))

    ccbreak_bool = pd.DataFrame(ccbreak_bool,\
                         columns=["Rupture"],\
                         index = np.full(len(T),i,dtype=int))

    T_air = pd.DataFrame(T_air,\
                         columns = ["T_air"],\
                         index = np.full(len(T),i,dtype=int))

    data = pd.concat([Tprod,T_air,T_az,ccbreak_bool],axis=1)
    data["T"]=T
    data.to_csv("index_simulation.csv",mode='a')


print("temps écoulé : {:.2f} min ".format((time.time()-t0)/60))
print("ok")