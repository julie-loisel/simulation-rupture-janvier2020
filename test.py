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

data = pd.read_csv("/home/loisel/index_simulation.csv",index_col=0,low_memory=False)

# print(data)
thresh = ThresholdAD(high = 5, low=-2)
data0 = data.loc[0]
print(data0)
data0 = data0.set_index("T")
anomalies = thresh.detect(data0["T_produit_zone1"])
# true = data.loc[0].set_index("T")["Rupture"]
# print(precision(true,anomalies))