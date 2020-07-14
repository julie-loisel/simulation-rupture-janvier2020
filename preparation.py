import fromage
from fromage import *
import numpy as np
circuit=np.random.randint(8,size=1)
palette = palette()
produit = produit()
T,T_air,liste_stages=constructT_air_avec_rupture_chaine(chaine=objects.chaine(circuit=circuit))
Tprod,T_az=calculs.calcul_profils(palette,produit,T_air)
#%%
