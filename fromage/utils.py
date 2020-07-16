#utils
import numpy as np
def construct_Sx_Sy(config,C_vent=1,S_h1=8.2e-4*2,S_h2=1.62e-3+6.9e-4*2,\
                    S_h3=7e-4+1.1e-3,S_h4=7e-4/2,S_h5=7e-4/4,S_h6=8.2e-4,S_h7=1.62e-3):
    
    if config==1:
        S_h1,S_h2,S_h3 = C_vent*S_h1,C_vent*S_h2,C_vent*S_h3
        Sy = np.array([[S_h1,1,S_h1,1,S_h1,1,S_h1],
               [S_h2,1,S_h2,1,S_h2,1,S_h2],
               [S_h1,1,S_h1,1,S_h1,1,S_h1]])
        Sx=np.array([[1., 1., 1., 1., 1., 1.],
               [1., 1., 1., 1., 1., 1.],
               [1., 1., 1., 1., 1., 1.],
               [0., S_h3, 0., S_h3, 0., S_h3]])
    if config==2:
        S_h4,S_h5,S_h6,S_h7= C_vent*S_h4,C_vent*S_h5,\
                            C_vent*S_h6,C_vent*S_h7
        Sy=np.array([[S_h4,1,1,S_h5,1,1,S_h4],
                       [S_h4,1,1,S_h5,1,1,S_h4],
                       [S_h4,1,1,S_h5,1,1,S_h4]])
        Sx=np.array([[1., 1., 1., 1., 1., 1.],
               [S_h6, S_h7,S_h6, S_h6, S_h7, S_h6],
               [1., 1., 1., 1., 1., 1.],
               [S_h6, S_h7,S_h6, S_h6, S_h7, S_h6]])
    return Sx,Sy
def construct_Mcx_Mcy(config,Ce=0.07,Ci=0.0256,Cc=0.0128):
    if config==1:
        Mcy = np.array([[0,Ci,Cc,Ci,Cc,Ci,0],
               [0,Ci,Cc,Ci,Cc,Ci,0],
               [0,Ci,Cc,Ci,Cc,Ci,0]])
        #Mcy = np.array([[0,Ci,Cc,Ci,Cc,Ci,Ce],
         #      [0,Ci,Cc,Ci,Cc,Ci,Ce],
          #     [0,Ci,Cc,Ci,Cc,Ci,Ce]])
        Mcx = np.array([np.ones(6)*0,#ou Cc ???
               np.ones(6)*Ci,
               np.ones(6)*Ci,
               np.ones(6)*0])
               #np.ones(6)*Ce])
    
    return Mcx,Mcy
def construct_T_air(dt,tr1,T1,tr2=0,T2=0,tr3=0,T3=0):
    t00=240
    t0=640
    Ta=0
    T_0=np.ones(int(t0*60/dt+1))*Ta
    T_00=np.ones(int(t00*60/dt))*Ta
    T_r1=np.ones(int(tr1*60/dt))*T1#T°C Rupture 1
    T_r2=np.ones(int(tr2*60/dt))*T2#T°C Rupture 1
    T_r3=np.ones(int(tr3*60/dt))*T3#T°C Rupture 1
    t_tot=t0+tr1+tr2+t00+t00+tr2+t00+t00+tr3+17*t00;
    T=np.arange(0,60*t_tot+1,dt)
    #T_air=np.concatenate([T_0,T_r1,T_00,T_00,T_00,T_00,T_r2,T_00,T_00,\
           #T_00,T_00,T_r2,T_00,T_00,T_00,T_00,T_r3,T_00,T_00,T_00,T_00,T_00,T_00,T_00,T_00,T_00])
    T_air=np.concatenate([T_0,T_r1,T_00,T_00,T_00,T_00,T_r2,T_00,T_00,\
           T_00,T_00,T_r2,T_00,T_00,T_00,T_00,T_r3,T_0,T_0])
    return T,T_air 

def construct_T_air_bis(dt,Ta,debut_t1,durees,pauses,temperatures):
    t_tot=debut_t1
    t1=debut_t1*60/dt
    T_air=np.ones(int(t1))*Ta
    for duree,pause,temperature in zip(durees,pauses,temperatures):
        t_tot=t_tot+duree+pause
        duree=int(duree*60/dt)
        pause=int(pause*60/dt)
        T_air=np.concatenate([T_air,np.ones(duree)*temperature,np.ones(pause)*Ta])
    
    T=np.arange(0,60*t_tot,dt)
    
    return T,T_air

def generate(dict_loi):
    if dict_loi["loi"]=="normal":
        return np.random.normal(loc=dict_loi["loc"],scale=dict_loi["scale"])
    if dict_loi["loi"]=="exponential":
        return np.random.exponential(scale=dict_loi["lambda"])

def constructT_air_sans_rupture_chaine(chaine,dt=30):
    T_air = np.array([])
    t_tot = 0
    stages = chaine.stages
    dict_donnees = chaine.dict_donnees[chaine.donnees]
    list_stages=[]
    for stage in stages:
        T = generate(dict_donnees[stage]["intensite"])
        t = generate(dict_donnees[stage]["duree"]) * 3600*24

        T_air = np.concatenate([T_air, T * np.ones(int(t / dt))])
        list_stages.append((stage,(t_tot)/3600))

        t_tot = t_tot + int(t / dt) * dt

    T = np.arange(0, t_tot, dt)
    return T, T_air,list_stages


def constructT_air_sans_rupture(dt=30):
    
    T_plateforme,t_plateforme=np.random.normal(loc=3.4,scale=1.4),np.random.exponential(1.05)*3600*24
    T_camion,t_camion=np.random.normal(loc=3.3,scale=1.2),np.random.exponential(0.25)*3600*24
    T_chambre,t_chambre=np.random.normal(loc=3.4,scale=1.4),np.random.exponential(1.05)*3600*24
    T_air=np.array([])
    t_tot=0
    for T,t in zip([T_plateforme,T_camion,T_chambre],[t_plateforme,t_camion,t_chambre]):
        T_air=np.concatenate([T_air,T*np.ones(int(t/dt))])
        t_tot=t_tot+int(t/dt)*dt
    T=np.arange(0,t_tot,dt)
    return T,T_air


def constructT_air_abus(dt=30):
    T_plateforme, t_plateforme = np.random.normal(loc=3.4, scale=1.4), np.random.exponential(1.05) * 3600 * 24
    T_camion, t_camion = np.random.normal(loc=12, scale=4), np.random.exponential(0.25) * 3600 * 24
    T_chambre, t_chambre = np.random.normal(loc=3.4, scale=1.4), np.random.exponential(1.05) * 3600 * 24
    T_air = np.array([])
    t_tot = 0
    for T, t in zip([T_plateforme, T_camion, T_chambre], [t_plateforme, t_camion, t_chambre]):
        T_air = np.concatenate([T_air, T * np.ones(int(t / dt))])
        t_tot = t_tot + int(t / dt) * dt
    T = np.arange(0, t_tot, dt)
    return T, T_air

def constructT_air_avec_rupture(dt=30,lambda_rupture=0.05):
    """lambda_rupture: paramètre de la loi exponentielle qui génère la durée de la rupture
    """
    T_plateforme,t_plateforme=np.random.normal(loc=3.4,scale=1.4),np.random.exponential(1.05)*3600*24
    T_camion,t_camion=np.random.normal(loc=3.3,scale=1.2),np.random.exponential(0.25)*3600*24
    T_chambre,t_chambre=np.random.normal(loc=3.4,scale=1.4),np.random.exponential(1.05)*3600*24
    T_air=np.array([])
    t_tot=0
    rupture=np.random.randint(0,2)
    for T,t,r in zip([T_plateforme,T_camion,T_chambre],[t_plateforme,t_camion,t_chambre],range(3)):
        Temps=int(t/dt)
        T_air=np.concatenate([T_air,T*np.ones(Temps)])
        t_tot=t_tot+Temps*dt
        if rupture==r:
            temp_rupture=np.random.randint(6,25)
            Temps_rupture=np.random.normal(loc=lambda_rupture,scale=0.05)*3600*24
            Temps=int(Temps_rupture/dt)
            T_air=np.concatenate([T_air,temp_rupture*np.ones(Temps)])
            t_tot=t_tot+Temps*dt
    T=np.arange(0,t_tot,dt)
    return T,T_air


def constructT_air_avec_rupture_chaine(chaine,dt=30,lambda_rupture=0.3):
    """lambda_rupture: paramètre de la loi exponentielle qui génère la durée de la rupture
    """
    T_air=np.array([])
    ccbreak_bool = np.array([])
    list_stages=[]
    t_tot=0
    rupture=np.random.randint(0,len(chaine.stages)-1)
    stages = chaine.stages
    dict_donnees = chaine.dict_donnees[chaine.donnees]
    for r,stage in enumerate(stages):
        T = generate(dict_donnees[stage]["intensite"])
        t = generate(dict_donnees[stage]["duree"])* 3600*24
        T_air = np.concatenate([T_air, T * np.ones(int(t / dt))])
        ccbreak_bool = np.concatenate([ccbreak_bool, np.zeros(int(t/dt))])
        list_stages.append((stage,(t_tot)/3600))

        t_tot = t_tot + int(t / dt) * dt

        if rupture==r:
            temp_rupture=np.random.randint(6,25)
            Temps_rupture=np.random.normal(loc=lambda_rupture,scale=0.05)*3600
            Temps=int(Temps_rupture/dt)
            T_air=np.concatenate([T_air,temp_rupture*np.ones(Temps)])
            ccbreak_bool = np.concatenate([ccbreak_bool, np.ones(int(Temps))])
            list_stages.append(("rupture",(t_tot)/3600))

            t_tot=t_tot+Temps*dt

    T=np.arange(0,t_tot,dt)
    return T,T_air,list_stages,ccbreak_bool

def init_pression(palette,produit,Vfr=0.31,e=0,f=0,Pa=1):
    I,J=palette.I,palette.J
    rho=produit.rho
    if Vfr>0:
        Pa = 0.5*rho*Vfr**2
    Pc = np.zeros((I+2,J+2))
    Tc = np.zeros((I+2,J+2))
    for i in range(I):
        Pc[i+1,0]=Pa
    for j in range(J):
        Pc[I+1,j]=Pa*(f+(e-f)*(2*J+1-2*j)/(2*J))
    return Pc,Pa

def calcul_ij(k,I,J):
    i=int(k//J+(1*(k%J!=0)))-1
    j =int(k%J + (k%J==0)*(k/(k/J)))-1
    return i,j

def init_champs_temperature(Qx,Qy,produit,Cp=1005):
    rho=produit.rho
    Qxp=np.maximum(Qx,0)*rho*Cp
    Qxm=-np.minimum(Qx,0)*rho*Cp
    Qyp=np.maximum(Qy,0)*rho*Cp
    Qym=-np.minimum(Qy,0)*rho*Cp
    return Qxp,Qxm,Qyp,Qym
