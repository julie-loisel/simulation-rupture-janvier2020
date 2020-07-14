import fromage
from fromage import *
import numpy as np
import pandas as pd
from adtk.detector import ThresholdAD
from adtk.data import validate_series
from adtk.metrics import recall,precision

#### Modèle thermique
circuit=np.random.randint(8,size=1)
palette = palette()
produit = produit()
T,T_air,liste_stages=constructT_air_avec_rupture_chaine(chaine=objects.chaine(circuit=circuit))
Tprod,T_az=calculs.calcul_profils(palette,produit,T_air)
#####

Tprod0_data = validate_series(pd.DataFrame(Tprod[0,:].T,index=pd.DatetimeIndex(T)))
T_az0_data = validate_series(pd.DataFrame(T_az[0,:].T,index=pd.DatetimeIndex(T)))


threshold_produit = ThresholdAD(high=4, low=0)
threshold_air = ThresholdAD(high=5, low=0)

anomalies_produit = threshold_produit.detect(Tprod0_data)
anomalies_air = threshold_air.detect(T_az0_data)
print(recall(anomalies_produit,anomalies_air))
print(precision(anomalies_produit,anomalies_air))