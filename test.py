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
t0 = time.time()

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

data = pd.read_csv("index_simulation10.csv", dtype = dict_dtypes,index_col=0)

######## Création du dataset des métriques ###########

headers_metric = ["No","Position","precision","recall","f1_score","iou","seuil"]
data_metric = pd.DataFrame(columns=headers)
data_metric["No"] = range(1000)
for No in range(1000):
    data_=data[data["No"]==No]
    datetime_series = pd.to_datetime(data_['T'])
    datetime_index = pd.DatetimeIndex(datetime_series.values)
    data_ = data_.set_index(datetime_index)
    data_ = pd.DataFrame(data_, index=datetime_index)
    data_ = validate_series(data_)
    true = data_["Rupture"]

    for t in np.linspace(1,10,20):
        thresh = ThresholdAD(high = t)
        for i in range(1,19):
            anomalies = thresh.detect(data_["T_produit_zone"+str(i)])
            precision_ = precision(true,anomalies)
            recall_ = recall(true, anomalies)
            f1_score_ = f1_score(true,anomalies)
            iou_ = iou(true,anomalies)

            data_metric.append({'No': No,\
                                'Position' : i,\
                                'precision' : precision_,\
                                'recall' : recall_,\
                                'f1_score' : f1_score_,\
                                'iou' : iou_,\
                                'seuil': t}, ignore_index=True)

    print("temps écoulé : {:.2f} min ".format((time.time() - t0) / 60))

data_metric.to_csv("TresholdAD1000_ruptures.csv", header=1)

print(data_metric.groupby("seuil").mean())

print("temps écoulé : {:.2f} min ".format((time.time()-t0)/60))
