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
headers = ["T_produit_zone"+str(i) for i in range(1,19)]\
    + ["T_air_zone"+str(i) for i in range(1,19)]\
    + ["Rupture"]\
    + ["T_air"]\
    + ["T"]\
    + ["No"]
data = pd.DataFrame(columns=headers)
data.to_csv("index_simulation10.csv", header=1)

for i in range(10):
    circuit=np.random.randint(8,size=1)
    chaine = objects.chaine(circuit=circuit)
    T,T_air,liste_stages,ccbreak_bool=constructT_air_avec_rupture_chaine(chaine=chaine)
    Tprod,T_az=calculs.calcul_profils(palette,produit,T_air)
    #####
    Tprod = pd.DataFrame(Tprod.T,\
                         columns=["T_produit_zone"+str(i) for i in range(1,19)])
    T_az= pd.DataFrame(T_az.T,\
                         columns=["T_air_zone"+str(i) for i in range(1,19)])
    ccbreak_bool = pd.DataFrame(ccbreak_bool,\
                         columns=["Rupture"])

    T_air = pd.DataFrame(T_air,\
                         columns = ["T_air"])

    data = pd.concat([Tprod,T_az,ccbreak_bool,T_air],axis=1)
    data["T"]=T
    data["No"]=i
    data.to_csv("index_simulation10.csv",mode='a',header=None)


print("temps écoulé : {:.2f} min ".format((time.time()-t0)/60))
print("ok")
print(data.columns)
print(data["Rupture"])