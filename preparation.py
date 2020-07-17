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
circuit=np.random.randint(8,size=1)
palette = palette()
produit = produit()
chaine = objects.chaine(circuit=circuit)
T,T_air,liste_stages,ccbreak_bool=constructT_air_avec_rupture_chaine(chaine=chaine)
Tprod,T_az=calculs.calcul_profils(palette,produit,T_air)
#####

Tprod_data = validate_series(pd.DataFrame(Tprod.T,index=pd.DatetimeIndex(T)))
Taz_data = validate_series(pd.DataFrame(T_az.T,index=pd.DatetimeIndex(T)))
ccbreak_bool= validate_series(pd.DataFrame(ccbreak_bool,index=pd.DatetimeIndex(T)))[0].astype(bool)
T_air_data = validate_series(pd.DataFrame(T_air,index=pd.DatetimeIndex(T)))
#########

## CAS 1 :
plt.plot(T,T_air)
plt.show()
threshold_produit = ThresholdAD(high=8, low=0)
threshold_az = ThresholdAD(high=5, low=0)
threshold_air = ThresholdAD(high=5, low=0)

anomalies_produit = threshold_produit.detect(Tprod_data)
anomalies_air = threshold_air.detect(T_air_data)[0]
anomalies_az = threshold_az.detect(Taz_data)


for metric in [precision,recall,iou]:
    print(np.mean([metric(anomalies_produit[i], anomalies_az[i]) for i in range(18)]))
print(np.mean([sklearn.metrics.f1_score(anomalies_produit[i], anomalies_az[i], labels=anomalies_az[i]) for i in range(18)]))
for True_labels in [ccbreak_bool,anomalies_air]:
    for Pred_labels in [anomalies_produit,anomalies_az]:
        print(np.mean([metric(True_labels, Pred_labels[i]) for i in range(18)]))

