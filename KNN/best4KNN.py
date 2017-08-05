import os
import matplotlib.pyplot as plt
import pandas as pd
import csv
import numpy as np
import matplotlib.pyplot as plt


random_sampleX1 = np.random.random_sample(3000) * 15
x1column = pd.DataFrame(random_sampleX1, columns = ['X1'])
#noise
random_sampleX2 = np.random.random_sample(3000) * 15
x2column = pd.DataFrame(random_sampleX2 , columns = ['X2'])

ycolumn = pd.DataFrame(np.random.random_sample(3000), columns = ['y'])
ycolumn['y'] += x1column['X1']**2 + x2column['X2'] **2
df = x1column.join(x2column)
df = df.join(ycolumn)
df.to_csv('best4KNN.csv', sep=',', header=False, index=False)

