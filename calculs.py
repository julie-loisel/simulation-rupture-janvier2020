#calculs
import numpy as np 
from fromage import utils,objects
def calcul_conductence_X(sx,i,palette,produit,dz=0.025,a=1.5,b=0.1):
    '''Calcule la conductance pour les pertes de charge pour la zone Z_i.
    Parameters:
    -----------
    sx : float
        la surface d'ouverture selon x 
    i : int
        la position du produit selon l'axe x 
        (important car si on est au bord, on divise la distance par 2)
    produit : object produit
    dz : float
        hauteur lame d'air
    a : float, default 1.5
        coefficient de perte de charge singulière d'un orifice
    b: float, default 0.1 (lambdaf/2)
        coefficient de perte de charge linéaire de lame d'air 

    Returns:
        float
    '''
    I,dx,dy=palette.I,palette.dx,palette.dy
    rho=produit.rho
    return sx**2/(0.5*rho*(a+b*sx**2*((dx+dx*(i!=I))/2)/dz/(dy*dz)**2))

def calcul_conductence_Y(sy,j,palette,produit,dz=0.025,a=1.5,b=0.1):
    '''Calcule la conductance pour les pertes de charge pour la zone Z_.j
    Parameters:
    -----------
    sy : float
        la surface d'ouverture selon y
    i : int
        la position du produit selon l'axe y
        (important car si on est au bord, on divise la distance par 2)
    produit : object produit
    dz : float
        hauteur lame d'air
    a : float, default 1.5
        coefficient de perte de charge singulière d'un orifice
    b: float, default 0.1 (lambdaf/2)
        coefficient de perte de charge linéaire de lame d'air 

    Returns:
        float
    '''
    J,dx,dy=palette.J,palette.dx,palette.dy
    rho=produit.rho
    return sy**2/(0.5*rho*(a+b*sy**2*((dy+dy*(j%J!=0))/2)/dz/(dx*dz)**2))

def calcul_matrices_conductence(palette,produit):
    '''Calcule les matrices de conductance cx et cy pour les pertes de charge pour les 
    pertes de charge
    Parameters:
    -----------
    palette : objet palette
        la palette que l'on considère 
    produit : objet produit
        le produit qui est dans la palette

    Returns:
    --------
    cx,cy: np.array,np.array
        les matrices de conductances suivant respectivement les axes x et y
    '''
    I,J,dx,dy,Sx,Sy=palette.I,palette.J,palette.dx,palette.dy,palette.Sx,palette.Sy
    cx = np.zeros((I+1,J))
    cy = np.zeros((I,J+1))
    for j in range(J):
        for i in range(1,I+1):
            cx[i,j]=calcul_conductence_X(sx=Sx[i,j],i=i,palette=palette,produit=produit)
    for i in range(I):
        for j in range(J+1):
            cy[i,j]=calcul_conductence_Y(sy=Sy[i,j],j=j,palette=palette,produit=produit)
    return cx,cy

def calcul_M1_V1(M1,V1,Cx,Cy,Pa,I,J,e=0,f=0):
    '''Calcule la matrice et le vecteur correspondant au système linéaire de l'équation (****)
    Parameters:
    -----------

    Returns:
    --------

    np.array(),np.array() 

    '''
    for k in range(1,I*J+1):
        i,j= utils.calcul_ij(k,I,J)
        id_k=k-1
        M1[id_k,id_k]=-(Cx[i,j]+Cx[i+1,j]+Cy[i,j+1]+Cy[i,j]) #pour chaque case, la somme des charges resp 
        
        if (k>J):
            i,j= utils.calcul_ij(k,I,J)
            M1[id_k,id_k-J]= Cx[i,j]
        if (k<=(I-1)*J):
            i,j= utils.calcul_ij(k+J,I,J)
            M1[id_k,id_k+J]= Cx[i,j]
        if ((k%J!=0)&(k<I*J)):
            i,j= utils.calcul_ij(k+1,I,J)
            M1[id_k,id_k+1]= Cy[i,j]
        if (((k+1)%J!=1)&(k<I*J)):
            i,j= utils.calcul_ij(k+1,I,J)
            M1[id_k+1,id_k]= Cy[i,j]
        if(k%J==1):
            i,j= utils.calcul_ij(k,I,J)
            V1[id_k]=-Cy[i,j]*Pa
        if(k>(I-1)*J):
            i,j= utils.calcul_ij(k,I,J)
            V1[id_k]-=Cx[i+1,j]*Pa*(f+(e-f)*(2*J+1-2*j))/(2*J)*0
    return M1,V1

def calcul_Mci_Ce_V(I,J,config=1,Ce=0.07,Ci=0.0256,Cc=0.0128):
    '''Calcule la matrice et le vecteur correspondant au système linéaire de l'équation (****)
    Parameters:
    -----------

    Returns:
    --------

    np.array(),np.array() 

    '''
    Pa=0
    Mcx,Mcy=utils.construct_Mcx_Mcy(config,Ce,Ci,Cc)
    Mci=np.zeros((I*J,I*J))
    Ce_V=np.zeros(I*J)
    Mci,_=calcul_M1_V1(Mci,Ce_V,Mcx,Mcy,Pa,I,J,e=0,f=0)
    for k in range(1,I*J+1):
        id_k=k-1
        if ((k%J==1)|(k%J==0)):
            Ce_V[id_k]+=Ce
        if (k<J*(I-1)):
            Ce_V[id_k]+=Ce
    return Mci,Ce_V


def calcul_hydraulique(palette,produit,Vfr=0.31):
    
    evol=1
    dx,dz,Sy=palette.dx,palette.dz,palette.Sy
    I,J=palette.I,palette.J
    Q0=0.01*dz*dx
    Qmin=Q0/100
    relax=0.9
    Qinold=3*Q0
    Qxold=Q0*np.ones((I+1,J))
    Qyold=Q0*np.ones((I,J+1))
    Qx=np.zeros((I+1,J))
    Pc,Pa=utils.init_pression(palette,produit)
    cx,cy=calcul_matrices_conductence(palette,produit)
    V1=np.zeros(I*J)
    while evol>0.01:
        Cx=np.divide(cx,Qmin+np.absolute(Qxold))
        Cy=np.divide(cy,Qmin+np.absolute(Qyold))
        M1=np.zeros((I*J,I*J))
        M1,V1=calcul_M1_V1(M1,V1,Cx,Cy,Pa,I,J)
        P=np.linalg.solve(M1,V1)
        Pc[1:4,1:7]=P.reshape(3,6)
        Qy=np.multiply((Pc[1:4,:7]-Pc[1:4,1:8]),Cy)
        Qx[1:4,:]=np.multiply(Pc[1:4,1:7]-Pc[2:5,1:7],Cx[1:,:])
        Qxold=Qx*(1-relax)+Qxold*relax
        Qyold=Qy*(1-relax)+Qyold*relax
        Qin=Qy[0,0]+Qy[1,0]+Qy[2,0]
        evol=abs((Qin-Qinold)/Qinold)
        Qinold=Qin
    Vin=0.9*Vfr
    if Vin>0:
        fac=Vin/(Qin/np.sum(Sy[:,0]))
        Qx=Qx*fac 
        Qy=Qy*fac
        Qin=Vin*sum(Sy[:,0])
    return Qx,Qy

def calcul_M(Qxm,Qym,Qxp,Qyp,produit,palette):
    I,J=palette.I,palette.J
    h,Sp=produit.h,produit.Sp
    M=np.zeros((I*J,I*J))
    for k in range(1,I*J+1):
        i,j= utils.calcul_ij(k,I,J)
        id_k=k-1
        M[id_k,id_k]=-(Qxp[i,j]+Qxm[i+1,j]+Qym[i,j+1]+Qyp[i,j]+h*Sp) #pour chaque case, la somme des charges resp 
        if (k>J):
            i,j= utils.calcul_ij(k,I,J)
            M[id_k,id_k-J]= Qxp[i,j]
        if (k<=(I-1)*J):
            i,j= utils.calcul_ij(k+J,I,J)
            M[id_k,id_k+J]= Qxm[i,j]
        if ((k%J!=0)&(k<I*J)):
            i,j= utils.calcul_ij(k+1,I,J)
            M[id_k,id_k+1]= Qym[i,j]
        if (((k+1)%J!=1)&(k<I*J)):
            i,j= utils.calcul_ij(k+1,I,J)
            M[id_k+1,id_k]= Qyp[i,j]
    return M
    
def calcul_temperatures(M,T_air,dt,Qxm,Qym,Qxp,Qyp,palette,produit,conduction=True):
    I,J,Q=palette.I,palette.J,palette.Q
    mp,Cp_p,Tinit=produit.mp,produit.Cp_p,produit.Tinit
    Sp,h=produit.Sp,produit.h
    T_az=np.zeros((I*J,len(T_air)))
    V=np.zeros(I*J)
    IM=np.linalg.inv(M)
    Tprod=np.zeros((I*J,len(T_air)))
    Tprod[:,0]=Tinit*np.ones(I*J)
    if conduction:
        Mci,Ce_V=calcul_Mci_Ce_V(I,J)
    else:
        Mci,Ce_V=np.zeros((I*J,I*J)),np.zeros(I*J)
    for n in range(Tprod.shape[1]-1):
        Ta=T_air[n]
        Tp=Tprod[:,n]
        for k in range(1,I*J+1):
            i,j =utils.calcul_ij(k,I,J)
            id_k= k-1
            V[id_k]= -h*Sp*Tp[id_k]
            V[id_k]-=Qyp[i,j]*Ta*(k%J==1) #sorties d'air en bas si k est une case 1,7,13 pour J=6 par ex
            V[id_k]-=Qym[i,j+1]*Ta*(k%J==0)
            V[id_k]-=Qxm[i+1,j]*Ta*(k>(I-1)*J)
        T_az[:,n]=IM.dot(V)
        Hci=Mci.dot(Tprod[:,n])
        Hce=np.multiply(Ce_V,(Ta-Tprod[:,n]))
        Tprod[:,n+1]=Tprod[:,n]+(h*Sp*(T_az[:,n]-Tprod[:,n])+Q+Hce+Hci)*(dt/mp/Cp_p)
    return Tprod,T_az

def calcul_profils(palette,produit,T_air,dt,Vfr,conduction=True):
    Qx,Qy=calcul_hydraulique(palette,produit,Vfr)
    Qxp,Qxm,Qyp,Qym=utils.init_champs_temperature(Qx,Qy,produit)
    M=calcul_M(Qxm,Qym,Qxp,Qyp,produit,palette)
    Tprod,T_az=calcul_temperatures(M,T_air,dt,Qxm,Qym,Qxp,Qyp,palette,produit,conduction)
    return Tprod,T_az