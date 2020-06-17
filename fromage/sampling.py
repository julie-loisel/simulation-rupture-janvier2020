#calculs
import numpy as np 
import pandas as pd 
from fromage import utils,objects,calculs
from scipy.stats import linregress

def generate_data(size,palette,produit,Vfr=0.31,proba_rupture=0.5,dt=30):
    """Fonction qui génère des profils de température, avec une certaine probabilité
    d'observer une rupture. Chaque profil est calculé grâce au modèle thermique 
    à partir d'un profil de T_air simulé, et une zone de la palette est choisie
    aléatoirement.
    Parameters:
    -----------
    size : nombre de profils à simuler
    palette : objet palette
        la palette que l'on considère 
    produit : objet produit
        le produit qui est dans la palette
    proba_rupture : probabilité d'observer une rupture 
    Vfr : vitesse frontale
    dt : pas de temps

    Returns:
    --------
    data: pd.DataFrame
    '''
    """
    
    id=0
    data0=[]
    for nb_it in range(size):
        rupture=(np.random.random()<proba_rupture)*1
        circuit=np.rupturendom.randint(8,size=1)
        if rupture:
            T,T_air,liste_stages=utils.constructT_air_avec_rupture_chaine(chaine=chaine(circuit=circuit))
        else:
            T,T_air,liste_stage=utils.constructT_air_sans_rupture_chaine(chaine=chaine(circuit=circuit))
        Tprod,T_az=calculs.calcul_profils(palette,produit,T_air,dt,Vfr)
        
        k=np.random.randint(1,19)
        data=pd.DataFrame(columns=['T','T_air','No_Produit','Rupture','id','T_prod'])
        len_T=len(T_air)
        data["T_air"]=T_air
        data["T"]=T
        data["id"]=nb_it
        data["T_air"]=T_air
        data["Rupture"]=rupture
        data["No_Produit"]=k
        data["T_prod"]=Tprod[k-1,:]
        data0.append(data)
        
    return pd.concat(data0).set_index(["id"])

def slope(x,y):
    return linregress(x,y)[0]

def vectorize_data(df):
    index = df.index.unique()
    data=pd.DataFrame(columns=['T', 'T_air', 'No_Produit', 'Rupture', 'T_prod'],index=index)
    for i in index:
        data.loc[i][["No_Produit","Rupture"]]=df.loc[i][["No_Produit","Rupture"]].values[0]
        data.loc[i]["T"]=df.loc[i]["T"].values

        data.loc[i]["T"]=df.loc[i]["T"].values
        data.loc[i]["T_air"]=df.loc[i]["T_air"].values
        data.loc[i]["T_prod"]=df.loc[i]["T_prod"].values
    return data
