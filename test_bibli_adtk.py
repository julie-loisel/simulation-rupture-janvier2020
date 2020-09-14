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
path = "/home/loisel/simulation-rupture-janvier2020/Vienne/"

data_metric = pd.read_csv(path + "cc_break_bool_threshold_simulation_ANIA_100")

data_seuil = data_metric.groupby("seuil").mean()
plt.plot(data_seuil.index,data_seuil["precision"],label = 'precision')
plt.plot(data_seuil.index,data_seuil["recall"],label = 'recall')
# plt.plot(data_seuil.index,data_seuil["iou"],label = 'iou')
plt.legend()
plt.show()

plt.plot(data_seuil.index,data_seuil["iou"],label = 'iou')
plt.show()

plt.plot(data_seuil.index,data_seuil["FN"]+data_seuil["FP"],label = 'somme faux')
plt.title("Somme des faux positifs et faux négatifs en fonction du seuil")
plt.show()

plt.plot(data_seuil.index,data_seuil["FN"],label = 'faux négatifs')
plt.plot(data_seuil.index,data_seuil["FP"],label = 'faux positifs')
plt.legend()
plt.title("faux positifs et faux négatifs en fonction du seuil")
plt.show()
