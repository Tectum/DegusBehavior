# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 15:11:13 2024

@author: User
"""
# save parameters around the time onset 

import pandas as pd 
import numpy as np 
import os
import math

# important paths
folder_tracking=r'C:\Users\juryl\Documents\degus\data'
file_stim=r'C:\Users\juryl\Documents\degus\degusTime.xlsx'

# parameters of videos 
fs=30   # frames per second
period=1/fs
cm_per_px = 0.026458333

# read all of the states used from Fonchil's file 
df = pd.ExcelFile(file_stim)
states = df.sheet_names

# matrix with aligned velocities for all trials
# for each trial include: state, trial, location stim, naiveness, velocities aligned
loc_up=['P5Up','P9Up','P9UpNaive','P15Up','P15UpNaive','P30Up','AdultUp']
naive= ['P9UpNaive', 'P9DownNaive','P15UpNaive', 'P15DownNaive','P5Up', 'P5Down','AdultUp','AdultDown']
preT=1    # seconds before stimulus onset to save in matrix
postT=2   # seconds after stimulus onset to save in matrix
win_len=(preT+postT)*fs    # window size in number of frames
par_all=np.empty((183,4+win_len), dtype=object)   # matrix to save velocities
par_all.fill(np.nan)
j=0

# across states
for i in states:
    state_i=pd.read_excel(df,sheet_name=i)
    onsets=state_i['Time_stim']
    refuges=state_i['Time_refuge']
    u=0   # counter for trials
    # print('\n'+i+'\n')
    
    # across trials
    for k in state_i['Animal']:
        # print(k)
        
        # time onset 
        onset=onsets[u]     # in seconds
        
        # time to refuge 
        refuge=refuges[u]   # in seconds
 
            
        # determine window to save from the tracking
        init = math.ceil((onset*fs) - (preT*fs))     # index of onset - pre time 
        end = math.ceil((onset*fs) + (postT*fs))     # index of onset + post window
        
        
        # load tracking data for particular state
        # read all of the states used from Fonchi's file 
        tr = pd.ExcelFile(os.path.join(folder_tracking, i+'.xlsx'))
        trials_tr = tr.sheet_names
        
        # Cristian did not track all of them, then make an exception if not found
        if k in trials_tr:
            
            # read tracking data 
            data_trial=pd.read_excel(os.path.join(folder_tracking, i+'.xlsx'),sheet_name=k)
            
            # remove trials that has not enough data to fill the desired window
            if data_trial.shape[0]<end:
                print('not enough tracking time')
                print(i,k)
                # save the state of the trial
                par_all[j,0]=i
                # save the trial name
                par_all[j,1]=k
                j=j+1
                u=u+1
                continue
            
            # get the data only for the required window
            pos_x=np.array(data_trial.iloc[init:end+1, 0])
            pos_y=np.array(data_trial.iloc[init:end+1, 1])
            
            # remove data after time-to-refuge
            if (refuge!=' ') and ~np.isnan(refuge) and (refuge<onset+postT):
                win_t=np.arange(init/fs,end/fs,1/fs)
                d=min(win_t, key=lambda s:abs(s-refuge))
                idx_tr=np.where(win_t==d)[0][0]
                pos_x[idx_tr:]=np.nan
                pos_y[idx_tr:]=np.nan

            
            # calculate the velocity
            diff_x=np.diff(pos_x)
            diff_y=np.diff(pos_y)
            speed_trial=((diff_x**2 + diff_y**2)**0.5)/period 
            speed_trial=speed_trial*cm_per_px
          
            # calculate the direction
            # angle_trial=np.arctan(diff_y/diff_x)
            
            # merge position x and y into one tuple to save in matrix
            # pos_trial=list(zip(pos_x[:-1],pos_y[:-1]))
            
            # save the state of the trial
            par_all[j,0]=i
            # save the trial name
            par_all[j,1]=k
            # save the location of the stimulus
            if i in loc_up: 
                par_all[j,2]=1  # up
            else:
                par_all[j,2]=0  # down
            # save the naiveness
            if i in naive:
                par_all[j,3]=1  # naive
            else:
                par_all[j,3]=0  # non-naive
            # save the parameter aligned to stim onset in a matrix
            par_all[j,4:4+len(speed_trial)]=speed_trial
            # par_all[j,4:4+len(angle_trial)]=angle_trial
            # par_all[j,4:4+len(pos_trial)]=pos_trial
            
            j=j+1
            u=u+1
            # if len(speed_trial)!=win_len-1:
            #     print(k)
            #     print(len(speed_trial))
        else:
            print('missing tracking file')
            print(i,k)
            # save the state of the trial
            par_all[j,0]=i
            # save the trial name
            par_all[j,1]=k
            j=j+1
            u=u+1
            continue
        
# remove those row that were missing or not enough tracking time         
h=par_all[:,2]
only=~pd.isnull(h)
par_all=par_all[only,:]


# save the matrix with all the speeds and info
np.save(r'C:\Users\juryl\Documents\degus\analysis_data\speed_all.npy',par_all)
