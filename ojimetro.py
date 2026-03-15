# -*- coding: utf-8 -*-
"""
Created on Sat Oct 26 10:29:09 2024

@author: juryl
"""

# read excel with ojimetro results 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
from scipy.optimize import curve_fit
import matplotlib.patches as patches
from scipy.stats import chi2_contingency, fisher_exact

# important paths
file_stim=r'C:\Users\juryl\Downloads\degusTimev2.xlsx'

# binocular fields 
bino=[25.5, 34.2,40.4, 54.2, 59.5]
bino=[5,9,15,30,40]

# read all of the states used from Fonchil's file 
df = pd.ExcelFile(file_stim)
states = df.sheet_names 
loc_tableY={'LoomUp': 0, 'LoomDown':1}
loc_tableX={'P4-5':0, 'P8-9':1,'P14-15':2, 'P30-31':3, 'Adult':4}
scape=np.zeros((2,5))
freeze=np.zeros((2,5))

tableS=np.zeros((2,5))
tableF=np.zeros((2,5))
tablenoS=np.zeros((2,5))
tablenoF=np.zeros((2,5))
for i in states:
    location=i.split()[0]
    age=i.split()[1]
    print(location, age)
   
    state_i=pd.read_excel(df,sheet_name=i)
    column_names = state_i.columns
    
    ojimetro=state_i[column_names[3]]
    
    trials_i=int(np.sum(ojimetro.notna()))
    print(ojimetro.unique())
    
    scape[loc_tableY[location],loc_tableX[age]]=sum(ojimetro=='e')/trials_i

    freeze[loc_tableY[location],loc_tableX[age]]=sum(ojimetro=='f')/trials_i
    freeze[loc_tableY[location],loc_tableX[age]]=freeze[loc_tableY[location],loc_tableX[age]]+sum(ojimetro=='o')/trials_i 
    freeze[loc_tableY[location],loc_tableX[age]]=freeze[loc_tableY[location],loc_tableX[age]]+sum(ojimetro=='t')/trials_i

    # tables contigency
    tableS[loc_tableY[location],loc_tableX[age]]=sum(ojimetro=='e')
    tablenoS[loc_tableY[location],loc_tableX[age]]=trials_i-tableS[loc_tableY[location],loc_tableX[age]]
    
    tableF[loc_tableY[location],loc_tableX[age]]=sum(ojimetro=='f')
    tableF[loc_tableY[location],loc_tableX[age]]=tableF[loc_tableY[location],loc_tableX[age]]+sum(ojimetro=='o')
    tableF[loc_tableY[location],loc_tableX[age]]=tableF[loc_tableY[location],loc_tableX[age]]+sum(ojimetro=='t')
    tablenoF[loc_tableY[location],loc_tableX[age]]=trials_i-tableF[loc_tableY[location],loc_tableX[age]]


    
# scatter plots with fitting curve 

# plot scape probability overhead looming
toplot=scape[0,:]

fig = plt.figure(1,figsize=(3,3)) 
ax = fig.add_subplot(111)
colors = plt.cm.Blues(np.linspace(0, 1, 9))
for i in range(len(bino)):
    print(i)
    ax.scatter(bino[i], toplot[i], color=colors[i+4])    

ax.plot(bino,toplot,'-o')
# ax.set_xlabel("Binocularity")
ax.set_xlabel("Stage (days)")
ax.set_ylabel("Escape probability")
# ax.set_ylabel("Freeze probability")
ax.set_ylim(0,1)
ax.set_xlim(0,45)

ax.spines[['right', 'top']].set_visible(False)
plt.tight_layout()
    
# Define the sigmoid function
def sigmoid(x, L, x0, k, b):
    return L / (1 + np.exp(+k * (x - x0))) + b   # change +k for inverse


# Generate synthetic data
x_data = bino[:-1] #np.arange(0,5,1)
y_data = toplot[:-1]

# Fit the sigmoid curve
p0 = [max(y_data), np.median(x_data), 1, min(y_data)]  # Initial guess
popt, popv = curve_fit(sigmoid, x_data, y_data, p0)

# Generate fitted values
x_fit = np.linspace(min(x_data), max(x_data), 100)
y_fit = sigmoid(x_fit, *popt)

# plot the fitting
# ax.plot(x_fit, y_fit,color=colors[i+4],lw=1,zorder=0)

rect = patches.Rectangle((bino[-1]-2, 0), 4, 1, linewidth=2, edgecolor='none', facecolor=colors[-1], alpha=0.1, zorder=0)
ax.add_patch(rect)
ax.set_xticks(bino)
values=[str(i) for i in bino[:-1]]
values.append('adult')
ax.set_xticklabels(values)


# plot scape probability frontal looming
toplot=scape[1,:]

# fig = plt.figure(2,figsize=(2,3)) 
# ax = fig.add_subplot(111)
colors = plt.cm.Oranges(np.linspace(0, 1, 9))
for i in range(len(bino)):
    print(i)
    ax.scatter(bino[i], toplot[i], color=colors[i+4])    
ax.plot(bino,toplot,'o-')
# ax.set_xlabel("Binocularity")
ax.set_xlabel("Stage (days)")
ax.set_ylabel("Escape probability")
# ax.set_ylabel("Freeze probability")
ax.set_ylim(0,1)
ax.set_xlim(0,45)

ax.spines[['right', 'top']].set_visible(False)
plt.tight_layout()
    
# Define the sigmoid function
def sigmoid(x, L, x0, k, b):
    return L / (1 + np.exp(-k * (x - x0))) + b   # change +k for inverse


# Generate synthetic data
x_data = bino[:-1] #np.arange(0,5,1)
y_data = toplot[:-1]

# Fit the sigmoid curve
p0 = [max(y_data), np.median(x_data), 1, min(y_data)]  # Initial guess
popt, popv = curve_fit(sigmoid, x_data, y_data, p0)

# Generate fitted values
x_fit = np.linspace(min(x_data), max(x_data), 100)
y_fit = sigmoid(x_fit, *popt)

# plot the fitting
# ax.plot(x_fit, y_fit,color=colors[i+4],lw=1,zorder=0)

rect = patches.Rectangle((bino[-1]-2, 0), 4, 1, linewidth=2, edgecolor='none', facecolor=colors[-1], alpha=0.3, zorder=0)
# ax.add_patch(rect)
ax.set_xticks(bino)
values=[str(i) for i in bino[:-1]]
values.append('adult')
ax.set_xticklabels(values)
# fig.savefig('C:/Users/juryl/Documents/degus/figures/escape_down.pdf')    
fig.savefig('C:/Users/juryl/Documents/degus/figures/escape_both.pdf')   

# plot freeze probability frontal looming
toplot=freeze[0,:]

fig = plt.figure(3,figsize=(3,3)) 
ax = fig.add_subplot(111)
colors = plt.cm.Blues(np.linspace(0, 1, 9))
for i in range(len(bino)):
    print(i)
    ax.scatter(bino[i], toplot[i], color=colors[i+4])    

ax.plot(bino,toplot,'o-')
# ax.set_xlabel("Binocularity")
ax.set_xlabel("Stage (days)")
# ax.set_ylabel("Escape probability")
ax.set_ylabel("Freeze probability")
ax.set_ylim(0,1)
ax.set_xlim(0,45)

ax.spines[['right', 'top']].set_visible(False)
plt.tight_layout()
    
# Define the sigmoid function
def sigmoid(x, L, x0, k, b):
    return L / (1 + np.exp(-k * (x - x0))) + b   # change +k for inverse


# Generate synthetic data
x_data = bino[:-1] #np.arange(0,5,1)
y_data = toplot[:-1]

# Fit the sigmoid curve
p0 = [max(y_data), np.median(x_data), 1, min(y_data)]  # Initial guess
popt, popv = curve_fit(sigmoid, x_data, y_data, p0)

# Generate fitted values
x_fit = np.linspace(min(x_data), max(x_data), 100)
y_fit = sigmoid(x_fit, *popt)

# plot the fitting
# ax.plot(x_fit, y_fit,color=colors[i+4],lw=1,zorder=0)

rect = patches.Rectangle((bino[-1]-2, 0), 4, 1, linewidth=2, edgecolor='none', facecolor=colors[-1], alpha=0.1, zorder=0)
ax.add_patch(rect)
ax.set_xticks(bino)
values=[str(i) for i in bino[:-1]]
values.append('adult')
ax.set_xticklabels(values)
# fig.savefig('C:/Users/juryl/Documents/degus/figures/freeze_up.pdf')    


# plot freeze probability overhead looming
toplot=freeze[1,:]

# fig = plt.figure(4,figsize=(2,3)) 
# ax = fig.add_subplot(111)
colors = plt.cm.Oranges(np.linspace(0, 1, 9))
for i in range(len(bino)):
    print(i)
    ax.scatter(bino[i], toplot[i], color=colors[i+4])    

ax.plot(bino,toplot,'o-')
# ax.set_xlabel("Binocularity")
ax.set_xlabel("Stage (days)")
# ax.set_ylabel("Escape probability")
ax.set_ylabel("Freeze probability")
ax.set_ylim(0,1)
ax.set_xlim(0,45)

ax.spines[['right', 'top']].set_visible(False)
plt.tight_layout()
    
# Define the sigmoid function
def sigmoid(x, L, x0, k, b):
    return L / (1 + np.exp(-k * (x - x0))) + b   # change +k for inverse


# Generate synthetic data
x_data = bino[:-1] #np.arange(0,5,1)
y_data = toplot[:-1]

# Fit the sigmoid curve
p0 = [max(y_data), np.median(x_data), 1, min(y_data)]  # Initial guess
popt, popv = curve_fit(sigmoid, x_data, y_data, p0)

# Generate fitted values
x_fit = np.linspace(min(x_data), max(x_data), 100)
y_fit = sigmoid(x_fit, *popt)

# plot the fitting
# ax.plot(x_fit, y_fit,color=colors[i+4],lw=1,zorder=0)

rect = patches.Rectangle((bino[-1]-2, 0), 4, 1, linewidth=2, edgecolor='none', facecolor=colors[-1], alpha=0.3, zorder=0)
# ax.add_patch(rect)
ax.set_xticks(bino)
values=[str(i) for i in bino[:-1]]
values.append('adult')
ax.set_xticklabels(values)


#%% statistics

yes_counts = np.array(tableF)

no_counts = np.array(tablenoF)

# Loop over the 5 days
for day in range(yes_counts.shape[1]):
    table = np.array([
        [yes_counts[0, day], no_counts[0, day]],  # Condition A
        [yes_counts[1, day], no_counts[1, day]]   # Condition B
    ])
    
    chi2, p_chi2, dof, exp = chi2_contingency(table)
    _, p_fisher = fisher_exact(table, alternative='two-sided')
    
    print(f"Day {day+1}: Chi² p={p_chi2:.4f}, Fisher p={p_fisher:.4f}")





    
