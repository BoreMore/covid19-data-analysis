import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# reads csv file and drops N/A values
data = pd.read_csv("2019_nCoV_data.csv").dropna()

# subsets dataset to only have data for China
china = data[data['Country'].str.contains('China')]

# makes date format uniform unlike the UNORGANIZED, BADLY ENTERED DATA
china['Last Update'] = np.where(china['Last Update'].str.contains('T'), 
        china['Last Update'].str.split('T').str[0], 
        china['Last Update'].str.replace('/', '-').str.split(' ').str[0])

# gets only the most recent report for the day
china = china.drop_duplicates(subset=['Province/State', 'Last Update'], keep='last')

# adds everything up for the day
chinaSum = china.groupby('Last Update', as_index=False).sum()

# removes data in which the confirmed cases decreased compared to the previous day since it is likely an error
chinaSumTemp = chinaSum[chinaSum['Confirmed'] > chinaSum['Confirmed'].shift()]
chinaSumTemp.loc[0] = chinaSum.iloc[0]
chinaSumTemp = chinaSumTemp.sort_index()
chinaSum = chinaSumTemp

# creates a new column that contains all the active cases
chinaSum['Active Cases'] = chinaSum['Confirmed'] - chinaSum['Deaths'] - chinaSum['Recovered']
#print(chinaSum)

# creates a stacked bar graph of the data
ax = chinaSum.plot(kind='bar', x='Last Update', y=['Active Cases', 'Recovered', 'Deaths'], stacked=True, color=['red', 'green', 'black'], rot=70)

# sets z-index of gridlines to be lower so the data can be seen on top of them
ax.set_axisbelow(True)
# creates grid and sets color and line style
ax.grid(color='gray', linestyle='dashed')

# sets labels and titles
ax.set_xlabel('Date')
ax.set_ylabel('People')
ax.set_title('Coronavirus in China')

# moves chart up on the window
plt.subplots_adjust(bottom=0.2)

# shows chart
plt.show()

# alternative but more complex way to plot the data
"""
p1 = plt.bar(ind, chinaSum['Confirmed'], color='red')
p2 = plt.bar(ind, chinaSum['Recovered'], bottom=chinaSum['Confirmed'], color='green')
p3 = plt.bar(ind, chinaSum['Deaths'], bottom=chinaSum['Confirmed'] + chinaSum['Recovered'], color='black')
plt.xlabel('Date')
plt.ylabel('People')
plt.title('Coronavirus in China')
plt.xticks(ind, chinaSum.iloc[ind, 0], rotation=70)
plt.yticks(np.arange(0, 90000 + 1, 5000))
plt.grid(True)
plt.legend((p1[0], p2[0], p3[0]), ('Confirmed', 'Recovered', 'Deaths'))
plt.show()
"""
