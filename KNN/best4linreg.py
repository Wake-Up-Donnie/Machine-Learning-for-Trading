import os
import matplotlib.pyplot as plt
import pandas as pd
import csv
import numpy as np


random_sampleX1 = np.random.uniform(0, 1, 1000)
x1column = pd.DataFrame(random_sampleX1, columns = ['X1'])
#noise
x1column['X1'] += np.random.random_sample(1000)

random_sampleX2 = np.random.uniform(0, 1, 1000)
x2column = pd.DataFrame(random_sampleX2 , columns = ['X2'])
#noise
x2column['X2'] += np.random.random_sample(1000)

y_data = random_sampleX1 * 500 + random_sampleX2 * 500
y_df = pd.DataFrame(y_data, columns = ['Y'])
df = x1column.join(x2column)
df = df.join(y_df)
df.to_csv('best4Linreg.csv', sep=',', header=False, index=False)

