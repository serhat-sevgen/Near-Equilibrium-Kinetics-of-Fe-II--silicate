"""
Generated by B.M. Tutolo and edited by S. Sevgen, 2024.

"""
import os, sys, numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.close('all')
plt.rcParams.update({'font.size': 20,
                     'axes.labelsize': 20,
                     'xtick.labelsize' : 16,
                     'xtick.direction' : 'in',
                     'ytick.direction' : 'in',
                     'ytick.labelsize' : 16,
                     'lines.linewidth': 1.0,
                     'lines.markersize': 8,
                     'axes.linewidth': 2})

plt.rcParams['axes.unicode_minus'] = False
#this is to get the text to output as text 
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42

E_ICP= #insert your analytical uncertanity

dat= pd.read_csv('file location')

dat['Time elapsed (s)']=dat['Time elapsed']*60

m = dat['Fluid in reactor (kg)'] # (kg) solution mass
v_dis= # insert stoichometric coefficient of element of interest
v_ppt= # insert stoichometric coefficient of element of interest

S =  # instert surfacea area value
d28Si_dt = dat['28Si (mol/kg)'].diff() / dat['Time elapsed (s)'].diff()
d29Si_dt = dat['29Si (mol/kg)'].diff() / dat['Time elapsed (s)'].diff()
dSi_dt=dat['Total Si (mol/kg)'].diff()/ dat['Time elapsed (s)'].diff()

f28Si_29Si = dat['28Si (mol/kg)'] / dat['29Si (mol/kg)']
f28Si_29Si_tbar = f28Si_29Si.rolling(window=2).mean()

f29Si_28Si = dat['29Si (mol/kg)'] / dat['28Si (mol/kg)']
f29Si_28Si_tbar = f29Si_28Si.rolling(window=2).mean()

f29Si_totSi=dat['29Si (mol/kg)']/dat['Total Si (mol/kg)']
f29Si_totSi_tbar=f29Si_totSi.rolling(window=2).mean()

f28Si_totSi=dat['28Si (mol/kg)']/dat['Total Si (mol/kg)']
f28Si_totSi_tbar=f28Si_totSi.rolling(window=2).mean()

f28Si_totSi_dis=0.9223
f29Si_totSi_dis=0.0468
f28Si_29Si_dis=f28Si_totSi_dis/f29Si_totSi_dis
f29Si_28Si_dis=f29Si_totSi_dis/f28Si_totSi_dis

Rdis=(m/(v_dis*S))*(d28Si_dt-d29Si_dt*f28Si_29Si_tbar)/(f28Si_totSi_dis-f29Si_totSi_dis*f28Si_29Si_tbar)

error_Rdis_SS= Rdis * np.sqrt(((E_ICP*d28Si_dt)**2+(d29Si_dt)**2*(f28Si_29Si_tbar)**2*((E_ICP)**2+(E_ICP)**2)+(f28Si_29Si_tbar)**2*(E_ICP*d29Si_dt)**2)/((d28Si_dt-d29Si_dt*f28Si_29Si_tbar)**2)
                              +(f29Si_totSi_dis)**2*((f28Si_29Si_tbar)**2*((E_ICP)**2+(E_ICP)**2))/((f28Si_totSi_dis-f29Si_totSi_dis*f28Si_29Si_tbar))**2)

Rppt_BT= (m/(v_ppt*S))*(d29Si_dt-d28Si_dt*(1/f28Si_29Si_dis))/(f28Si_totSi_tbar*(1/f28Si_29Si_dis)-f29Si_totSi_tbar)
Rppt=Rppt_BT

Rppt[(Rppt<0)]=np.nan

error_Rppt_SS= Rppt * np.sqrt((((E_ICP*d29Si_dt)**2+(f29Si_28Si_dis)**2*(E_ICP*d28Si_dt)**2)/((d29Si_dt-d28Si_dt*f29Si_28Si_dis)**2))
                              +(((f28Si_totSi_tbar)**2*(f29Si_28Si_dis)**2*((E_ICP)**2+(E_ICP)**2))+((f29Si_totSi_tbar)**2*((E_ICP)**2+(E_ICP)**2)))/((f29Si_28Si_dis*f28Si_totSi_tbar-f29Si_totSi_tbar))**2)

frac28_error = np.sqrt((E_ICP*dat['28Si (mol/kg)']/dat['28Si (mol/kg)'])**2+(E_ICP*dat['Total Si (mol/kg)']/dat['Total Si (mol/kg)'])**2)*f28Si_totSi
frac29_error = np.sqrt((E_ICP*dat['29Si (mol/kg)']/dat['29Si (mol/kg)'])**2+(E_ICP*dat['Total Si (mol/kg)']/dat['Total Si (mol/kg)'])**2)*f29Si_totSi

plt.figure()
plt.errorbar(dat['Time elapsed'], f28Si_totSi, yerr=frac28_error, xerr=None,capsize=3,fmt='-o',mfc='darkblue',ecolor='k',color='darkblue', label='f28')
plt.errorbar(dat['Time elapsed'], f29Si_totSi, yerr=frac29_error,xerr=None,capsize=3,fmt='-o',mfc='darkred',ecolor='k',color='darkred', label='f29')
plt.ylabel('fSi')
plt.xlabel('Time (min)')
plt.legend()
plt.show()

time_elapsed = dat['Time elapsed'][1:]  # Exclude the first value

dissprecipratefig, ax1 = plt.subplots() 
ax1.errorbar(time_elapsed, np.log10(Rdis[1:]), yerr=0.434*error_Rdis_SS[1:]/Rdis[1:], xerr=None, capsize=3, fmt='ko', mfc='w', label='Dissolution') 
ax1.errorbar(time_elapsed, np.log10(Rppt[1:]), yerr=0.434*error_Rppt_SS[1:]/Rppt[1:], xerr=None, capsize=3, fmt='ko', mfc='k', label='Precipitation')
ax1.set_ylabel('log rate (mol Si /m$^2$/s)')
ax1.set_xlabel('Time (min)')  

Rdis_subset = Rdis[1:]
Rppt_subset = Rppt[1:]
E_diss_subset = error_Rdis_SS[1:]
E_ppt_subset = error_Rppt_SS[1:]

time_elapsed_subset = dat['Time elapsed'][1:]
bar_width = 0.35
index = np.arange(len(time_elapsed_subset))

ratefig = plt.figure()
plt.bar(index + bar_width/2, Rdis_subset, yerr=E_diss_subset, width=bar_width, color='#E8772E', label='Rdis')
plt.bar(index - bar_width/2, Rppt_subset, yerr=E_ppt_subset, width=bar_width, color='#AEE950', label='Rppt')

plt.errorbar(index + bar_width/2, Rdis_subset, yerr=E_diss_subset, fmt='+', capsize=1, capthick=1, color='black', label='Rdis_er')
plt.errorbar(index - bar_width/2, Rppt_subset, yerr=E_ppt_subset, fmt='+', capsize=1, capthick=1, color='black', label='Rppt_er')

plt.ylabel('Reaction rate (mol/m$^2$/s)')
plt.xlabel('Time (min)')

custom_labels = ['0-14','14-26', '26-64', '64-134', '134-190']  # Update this list as per your specific labels
plt.xticks(index, custom_labels)

plt.legend()

plt.show()

AllSifig=plt.figure()

plt.errorbar(dat['Time elapsed'],dat['Total Si (mol/kg)'],yerr=E_ICP*dat['Total Si (mol/kg)'],xerr=None,capsize=3,fmt='-d',mfc='darkblue',ecolor='k',color='darkblue', label='Total Si')
plt.errorbar(dat['Time elapsed'],dat['29Si (mol/kg)'],yerr=E_ICP*dat['29Si (mol/kg)'],xerr=None,capsize=3,fmt='-o',ecolor='k',color='darkgreen', label='29Si')
plt.errorbar(dat['Time elapsed'],dat['28Si (mol/kg)'],yerr=E_ICP*dat['28Si (mol/kg)'],xerr=None,capsize=3,fmt='-s',ecolor='k',color='darkred', label='28Si')
plt.ylabel('Concentration (mol/kg)')
plt.xlabel('Time (min)')
plt.legend()
