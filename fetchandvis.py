import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats


df = pd.read_csv('woocommerce.csv')


mean = np.mean(df['order_price'])
median = np.median(df['order_price'])
mode = stats.mode(df['order_price'])

# Visualize the data
sns.histplot(df['order_price'])
plt.show()
