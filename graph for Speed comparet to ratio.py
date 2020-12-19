import plotly.express as px
import numpy as np
import pandas as pd

pi = 3.1415926535897932384626433832

rpm  = float(input('Rpm: '))
size = float(input('Radius (cm): '))

lines = []
for i in range(int(size)):
    lines.append(str(i+1)+','+str((2*pi*((i+1)/100))*(rpm/60))+','+str((rpm**2)*1.118*(10**(0-5))*i))
lines.append(str(size)+','+str((2*pi*((size)/100))*(rpm/60))+','+str((rpm**2)*1.118*(10**(0-5))*size))
xs = list()
ys = list()
zs = list()
for line in lines:
    x, y, z = line.split(',')
    xs.append(float(x))
    ys.append(float(y))
    zs.append(float(z))
    
df = pd.DataFrame({'cm ':xs, 'Speed in m/s ':ys, 'Zentrifugal force (RCF) or g force ':zs})
fig = px.line(df, x='cm ', y=['Speed in m/s ', 'Zentrifugal force (RCF) or g force '], title='Comparison of ratio and speed ({0} rpm and {1} cm)'.format(rpm, size))
fig.write_html('Ratio and speed.html', auto_open=True)

