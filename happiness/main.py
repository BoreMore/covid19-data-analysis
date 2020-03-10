import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# reads csv file and drops N/A values
df = pd.read_csv("happiness.csv").dropna()

# stores array of unique regions
unique = df['Region'].unique()

color_list = ['crimson', 'darkorange', 'gold', 'mediumspringgreen', 'mediumblue', 'mediumturquoise', 'darkcyan', 'darkviolet', 'hotpink', 'black']

# creates dictionary assigning unique regions to a color
color_zip = zip(unique, color_list)
color_map = dict(color_zip)

# creates bar graph
ax = df.plot.bar(x='Country', y='Happiness Score', color=df['Region'].map(color_map), figsize=(24,12))

# creates legend based on unique values and color
patches = []
for key, value in color_map.items():
    patches.append(mpatches.Patch(color=value, label=key)) 

# adds legend to graph and resizes it
ax.legend(handles=patches, prop={'size': 8})

# creates grid and sets color and line style
ax.set_axisbelow(True)
ax.grid(color='gray', linestyle='dashed')

# sets labels and titles
ax.set_xlabel('Country')
ax.set_ylabel('Happiness Score')
ax.set_title('Happiest Countries')

# adjusts graph position
plt.subplots_adjust(bottom=0.4)

# makes x labels smaller
ax.tick_params(axis='x', which='major', labelsize=8)

# saves graph as png
plt.savefig("happinessgraph.png", bbox_inches='tight')

# shows graph
plt.show()
