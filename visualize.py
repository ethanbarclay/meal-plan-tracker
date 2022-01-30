import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
import pandas as pd

#8.98188034188
df = pd.read_csv('data.csv', header=0, names=["Time", "Balance"])

z = np.polyfit(df['Time'], df['Balance'], 1)
p = np.poly1d(z)
plt.plot(df['Time'],p(df['Time']),"r--")


df['Time'] = pd.to_datetime(df['Time'],unit='s')
plot = df.plot(x="Time", y="Balance")
plot.plot_date(df['Time'],df['Balance'])

plt.plot([datetime.fromtimestamp(1641765631),datetime.fromtimestamp(1651895999)], [1050.88, 0], 'k--', lw=2)

# plot.xaxis.set_major_locator(mdates.DayLocator())
plot.set_xlabel("Date")
plot.set_ylim(600, 1100)
plot.set_xlim(pd.datetime.fromtimestamp(1641765631), datetime.fromtimestamp(1643477880))


plt.show()