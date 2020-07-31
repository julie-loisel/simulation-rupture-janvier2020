import adtk.detector
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

data = pd.read_csv("index_simulation.csv", dtype = dict_dtypes,index_col=0)
thresh = ThresholdAD(high = 4, low=-2)
data0 = data[data["No"]==0]
datetime_series = pd.to_datetime(data0['T'])
# create datetime index passing the datetime series
datetime_index = pd.DatetimeIndex(datetime_series.values)

data0=data0.set_index(datetime_index)
data0 = pd.DataFrame(data0,index=datetime_index)

data0 = validate_series(data0)
thresh = adtk.detector.ThresholdAD()
anomalies = thresh.detect(data0['T_produit_zone1'])
true = data0["Rupture"]

print(precision(true,anomalies))

for s in [s.__name__ for s in adtk.detector._NonTrainableUnivariateDetector.__subclasses__()]:

    thresh = getattr(adtk.detector, s)()
    anomalies = thresh.detect(data0['T_produit_zone1'])
    true = data0["Rupture"]
    print(precision(true,anomalies))

print([s.__name__ for s in adtk.detector._TrainableUnivariateDetector.__subclasses__()])
for s in ['QuantileAD', 'InterQuartileRangeAD', 'GeneralizedESDTestAD', 'PersistAD', 'LevelShiftAD', 'VolatilityShiftAD', 'AutoregressionAD', 'SeasonalAD']:

    thresh = getattr(adtk.detector, s)()
    anomalies = thresh.fit_detect(data0['T_produit_zone1'])
    true = data0["Rupture"]
    print(precision(true,anomalies))

