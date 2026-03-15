# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 15:07:47 2024

@author: juryl
"""

# plot individual trials parameter across time 


import numpy as np 
import matplotlib.pyplot as plt 
# import scipy
from matplotlib import colormaps
from func_help import idx_ojimetro

# load data already aligned to stimulus onset and normalized
file_data=r'C:\Users\juryl\Documents\degus\analysis_data\speed_all.npy'
data=np.load(file_data, allow_pickle=True)
data=np.delete(data, (168,169), axis=0)

# get rid of naive differences 
age={'P5Up':1, 'P5Down':1,'P9Up':2,"P9Down":2,'P9UpNaive':2, 'P9DownNaive':2,
     'P15Up':3, 'P15UpNaive':3,'P15Down':3,'P15DownNaive':3, 'P30Up':4,
     'P30Down':4,'AdultUp':5, 'AdultDown':5}
cor_age=[]
for i in range(len(data)):
    cor_age.append(age[data[i,0]])
    
    
# remove one trial where speed is insane 
# data = np.delete(data,147,axis=0)

# parameters to plot 
location = 1  # 1:up    0:down
naive = 1     # 1:naive 0:non-naive  

loc_=data[:,2]==location
nai_=data[:,3]==naive
part=loc_#*nai_
# part=loc_
speed_part=data[part,4:]


# to plot naive versus non-naive
# part2=[f=='P9Up' for f in data[:,0]]
# part3=[f=='P9UpNaive' for f in data[:,0]]
# part=np.array(part2)+np.array(part3)
# speed_part=data[part,4:]
# #

id_part=data[part,0]
# if location==1:
#     id_part=[i[0:-2] for i in id_part]
# elif location==0:
#     id_part=[i[0:-4] for i in id_part]
id_part=[age[i] for i in id_part]


states=np.unique(id_part)
tot_states=len(states)


cmap=colormaps['Blues']
speed_part=np.array(speed_part, dtype=float)
k=1
# sort=[3,2,0,1]
# sort=[1,0]
# states=states[sort]

# fig = plt.figure(figsize=(3,2)) 
# ax = fig.add_subplot(111)
for i in states:
    # ax = fig.add_subplot(len(states),1,k)
    fig = plt.figure(figsize=(3,2)) 
    ax = fig.add_subplot(111)
    print(i)
    sta_=[x == i for x in id_part]
    print(sum(sta_))
    speed_state=speed_part[sta_,:]
    speed_state=np.nan_to_num(speed_state)
    
    #%% subset of the data visually determined type of response 
    ids=data[part,1]
    target_string=ids[sta_]
    i_s,i_f=idx_ojimetro(target_string)
    speed_state=speed_state[i_s,:]
    #%%
    
    # values to plotspeed_state
    speed_state_mean = np.mean(speed_state,axis=0)
    speed_state_std = np.std(speed_state,axis=0)
    speed_state_error = speed_state_std/np.sqrt(len(speed_state))
    time=np.linspace(-1,2,len(speed_state_mean))
    c = cmap(i*50)
    
    # plotting
    ax.plot(time,speed_state_mean,color=c,label=i)
    ax.fill_between(time,speed_state_mean-speed_state_error,speed_state_mean+speed_state_error,color=c,alpha=0.3)
    ax.set_xlabel("Time (sec)")
    ax.set_ylabel("Speed (cm/s)")
    ax.axvline(0,color='k', linestyle='dashed',lw=0.6)
    # ax.set_ylim(-2,35)
    ax.set_xlim(-1,1)
    ax.axhline(0,color='grey', linestyle='dashed',lw=0.6)
    ax.spines[['right', 'top']].set_visible(False)
    plt.tight_layout()
    # plt.legend()
    stat_str=str(i)
    loc_str=str(location)
    plt.savefig('C:/Users/juryl/Documents/degus/figures/avS'+loc_str+'_'+stat_str+'.pdf')
    k=k+1
    

# # plot only one state to show the outlayer 
# plt.figure()
# only_=data[:,0]=='AdultUp'
# speed_part=data[only_,:]
# for i in range(len(speed_part)):
#     plt.plot(speed_part[i,4:])








