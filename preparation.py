import fromage
from fromage import *
import numpy as np
import pandas as pd
import adtk
from adtk.detector import ThresholdAD
from adtk.data import validate_series
from adtk.metrics import recall,precision,iou,f1_score
from adtk.data import to_events
import time
#### Modèle thermique
t0 = time.time()
circuit=np.random.randint(8,size=1)
palette = palette()
produit = produit()
chaine = objects.chaine(circuit=circuit)
T,T_air,liste_stages,ccbreak_bool=constructT_air_avec_rupture_chaine(chaine=chaine)
Tprod,T_az=calculs.calcul_profils(palette,produit,T_air)
#####
metric = precision
Tprod_data = validate_series(pd.DataFrame(Tprod.T,index=pd.DatetimeIndex(T)))
Taz_data = validate_series(pd.DataFrame(T_az.T,index=pd.DatetimeIndex(T)))
ccbreak_bool= validate_series(pd.DataFrame(ccbreak_bool,index=pd.DatetimeIndex(T)))[0].astype(bool)
#ccbreak_bool=ccbreak_bool.astype(bool)
threshold_produit = ThresholdAD(high=3, low=0)
anomalies_produit = threshold_produit.detect(Tprod_data[0])
print(ccbreak_bool.shape==anomalies_produit.shape)

for metric in [recall,precision,iou,adtk.metrics.f1_score]:
    print(metric(ccbreak_bool,anomalies_produit))

#threshold_air = ThresholdAD(high=5, low=0)

#anomalies_air = threshold_air.detect(T_az0_data)
#print(recall(anomalies_produit,anomalies_air))
#print(len((T_air)))
#print(anomalies_produit)
#print(to_events(anomalies_produit))
#print(ccbreak_bool)