import pandas as pd 
import matplotlib.pyplot as plt 

'''
Neutral gas velocity Vn in [m/s] with its three components
Vn_Lat (meridional, positive northward)
Vn_Lon (zonal, positive eastward)
Vn_IP (vertical, radial, calculated from Omega)
'''

infile = 'models/TIEGCM/300_winds.txt'

f = open(infile).readlines()

out = []
for line in f:
    
    if '#' in line:
        pass
    else:
        out.append(line.split())
        
df = pd.DataFrame(out) 

dict = {0:'year',1:'month',2:'day', 3:'hour',4:'minute'}

df['time'] = pd.to_datetime(df[[0,1,2,3,4]].rename(
    columns=dict
))

# Coloca essa coluna como índice
df = df.set_index('time')

df = df.iloc[:, 9:].astype(float)

# df.plot()
df.columns = ['zon', 'mer', 'vn']

df 