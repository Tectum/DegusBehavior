# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 15:06:47 2024

@author: juryl
"""

# plot raw data without normalization just the raster plot 
import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib.colors import LinearSegmentedColormap
# import scipy
# from matplotlib.pyplot import cm

# load data already aligned to stimulus onset
file_data=r'C:\Users\juryl\Documents\degus\analysis_data\speed_all.npy'
data=np.load(file_data, allow_pickle=True)

# load data from the baseline, all time before onset
# file_data='E:\degus\\base_speed_all.npy'
# base=np.load(file_data, allow_pickle=True)

# get rid of naive differences 
age={'P5Up':1, 'P5Down':1,'P9Up':2,"P9Down":2,'P9UpNaive':2, 'P9DownNaive':2,
     'P15Up':3, 'P15UpNaive':3,'P15Down':3,'P15DownNaive':3, 'P30Up':4,
     'P30Down':4,'AdultUp':5, 'AdultDown':5}
cor_age=[]
for i in range(len(data)):
    cor_age.append(age[data[i,0]])
    
# sorter data within groups
sorter_age=np.array([])
for group in range(1,6):
    print(group)
    idx_group=np.where(np.array(cor_age)==group)[0]
    # np.random.shuffle(idx_group)
    speed_state=data[idx_group,4+30:]
    idx_max=np.argmax(speed_state,1)
    sorter_idx=np.argsort(idx_max)
    sorter_group=idx_group[sorter_idx]
    sorter_age=np.concatenate([sorter_age,sorter_group])
sorter_age=sorter_age.tolist()    
sorter_age=[int(i) for i in sorter_age]
data=data[sorter_age,:]

# parameters to plot 
location = 1  # 1:up    0:down
naive = 0     # 1:naive 0:non-naive  

loc_=data[:,2]==location
nai_=data[:,3]==naive
part=loc_#*nai_
speed_part=data[part,4:]

# to plot naive versus nonnaive
# part2=[f=='P15Up'  for f in data[:,0]]   #or f=='P15Up'
# part3=[f=='P15UpNaive' for f in data[:,0]]    # or f=='P15UpNaive' 
# part=np.array(part2)+np.array(part3)
# speed_part=data[part,4:]
# new_order=list(range(0,11))+list(range(28,34))+list(range(11,28))+list(range(34,50))
# new_order=list(range(0,12))+list(range(24,30))+list(range(12,24))+list(range(30,39))
# speed_part=speed_part[new_order,0:30]
#

id_part=data[part,0]
# id_part=id_part[new_order]
# if location==1:
#     id_part=[i[0:-2] for i in id_part]
# elif location==0:
#     id_part=[i[0:-4] for i in id_part]
id_part=[age[i] for i in id_part]


# normalization of the parameter value based on the baseline
speed_part=np.array(speed_part, dtype=float)
n=len(speed_part)

# cmap = LinearSegmentedColormap.from_list('mycmap', ['black', 'white','orange']) # cyan, up 
cmap = LinearSegmentedColormap.from_list('mycmap', ['black','white','cyan']) # orange, down 
cmap.set_bad(color='k') 

fig = plt.figure(figsize=(4,6))
ax = fig.add_subplot(111)
cax = ax.imshow(speed_part,origin='lower',interpolation='nearest',aspect='auto',extent=[-1,2,0,n],cmap=cmap,vmax=20,vmin=0) # ,norm=colors.LogNorm()
ax.set_xlabel("Time (seg)")
ax.set_yticks(np.arange(0,n,1))
ax.set_yticklabels(id_part, fontsize=8)

ax.xaxis.set_ticks_position('none') 
cbar = fig.colorbar(cax) 
cbar.set_label("Speed (cm/s)")
ax.axvline(0,0,2,linestyle='dashed',color='white',lw=2)
plt.locator_params(axis='x',nbins=2)


# plot horizontal lines between states
pre_state=''
k=0
for i in id_part:
    if i!=pre_state:
        ax.axhline(k,linestyle='dashed',color='white',lw=1) 
        k=k+1
        pre_state=i
    else:
        k=k+1

plt.tight_layout()







