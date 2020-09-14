import numpy as np
import pandas as pd
import adtk
import sklearn
import matplotlib.pyplot as plt
from adtk.detector import ThresholdAD
from adtk.data import validate_series
from adtk.metrics import recall,precision,iou,f1_score
from sklearn.metrics import confusion_matrix
from adtk.data import to_events
import time
t0 = time.time()
#path = "/home/loisel/simulation-rupture-janvier2020/"
def detection_metrics(name,N,definition,methode,path):
    ### Lecture des données #########
    headers = ["T_produit_zone"+str(i) for i in range(1,19)]\
        + ["T_air_zone"+str(i) for i in range(1,19)]\
        + ["Rupture"]\
        + ["T_air"]\
        + ["T"]\
        + ["No"]
    dtypes_list = ['float' for i in range(1,19)] \
                + ['float' for i in range(1, 19)] \
                + ['float'] \
                + ['object']\
                +['int']\
                +['int']

    dict_dtypes = {}
    for key,value in zip(headers,dtypes_list):
        dict_dtypes[key]=value
    data = pd.read_csv(path+name, dtype = dict_dtypes,index_col=0)
    #print(data)
    ######## Création du dataset des métriques ###########

    headers_metric = ["No","Position","precision","recall","f1_score","iou","seuil","FN","FP","TN","TP"]
    data_metric = pd.DataFrame(columns=headers_metric)
    name_results = path+definition+"_"+methode+"_"+name
    data_metric.to_csv(name_results , header=1)
    for No in range(N):
        data_=data[data["No"]==No]
        datetime_series = pd.to_datetime(data_['T'])
        datetime_index = pd.DatetimeIndex(datetime_series.values)
        data_ = data_.set_index(datetime_index)
        data_ = pd.DataFrame(data_, index=datetime_index)
        data_ = validate_series(data_)
        if definition == "cc_break_bool":
            true = data_["Rupture"]
        if methode == "threshold":
            for t in np.linspace(2,9,20):
                thresh = ThresholdAD(high = t)
                for i in range(1,19):
                    anomalies = thresh.detect(data_["T_air_zone"+str(i)])
                    precision_ = precision(true,anomalies)
                    recall_ = recall(true, anomalies)
                    f1_score_ = f1_score(true,anomalies)
                    iou_ = iou(true,anomalies)
                    CM = confusion_matrix(true, anomalies)
                    TN = CM[0][0]
                    FN = CM[1][0]
                    TP = CM[1][1]
                    FP = CM[0][1]
                    data_metric = pd.DataFrame(columns=headers_metric)
                    data_metric = data_metric.append({'No': No,\
                                        'Position' : i,\
                                        'precision' : precision_,\
                                        'recall' : recall_,\
                                        'f1_score' : f1_score_,\
                                        'iou' : iou_,\
                                        'seuil': t,\
                                        'FN':FN,\
                                        'FP':FP, \
                                        'TN': TN, \
                                        'TP': TP}, ignore_index=True)
                    data_metric.to_csv(name_results , header=None, mode="a")
                    del data_metric
    print("temps écoulé : {:.2f} min ".format((time.time() - t0) / 60))

