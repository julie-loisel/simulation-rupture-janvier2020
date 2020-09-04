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
path = "/home/loisel/simulation-rupture-janvier2020/"

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

data = pd.read_csv(path+"index_simulation3000.csv", dtype = dict_dtypes,index_col=0)
#print(data)
######## Création du dataset des métriques ###########

headers_metric = ["No","Position","precision","recall","f1_score","iou","seuil","FN","FP","TN","TP"]
data_metric = pd.DataFrame(columns=headers_metric)
data_metric.to_csv(path+"TresholdAD3000_ruptures_3000.csv", header=1)
for No in np.random.random_integers(3000,size=(30)):
    data_=data[data["No"]==No]
    datetime_series = pd.to_datetime(data_['T'])
    datetime_index = pd.DatetimeIndex(datetime_series.values)
    data_ = data_.set_index(datetime_index)
    data_ = pd.DataFrame(data_, index=datetime_index)
    data_ = validate_series(data_)
    true = data_["Rupture"]

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
            data_metric.to_csv(path+"TresholdAD3000_ruptures_3000.csv", header=None, mode="a")

#data_metric.to_csv(path+"TresholdAD3000_ruptures_3000.csv", header=1)

print(data_metric)

print("temps écoulé : {:.2f} min ".format((time.time()-t0)/60))
