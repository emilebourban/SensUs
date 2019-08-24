# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 09:04:43 2019

@author: Emile
"""
import os
import numpy as np
import matplotlib.pyplot as plt




#%%
in_dir = 'D:/Utilisateurs/Emile/Documents/MA2/SensUs/data/20190807plasma10ugAfter1h/int/'


data = {}
data_smoothed = {}
for filename in os.listdir(in_dir):
    if filename.endswith(".npy"):
        if 'smoothed' in filename:
            data_smoothed[filename[4:-4]] = np.load(in_dir+filename)
        else:
            data[filename[4:-4]] = np.load(in_dir+filename)
#%%  10ug

back = data['back']
spot = data['spot']

y = (back-spot) / (back+spot)

x = np.arange(0, y.shape[0]/2, 0.5)

plt.plot(x,y)
reg_lin = np.polyfit(x, y, 1)
print(reg_lin)
plt.plot(x, np.poly1d(reg_lin)(x))

#%%
in_dir = 'D:/Utilisateurs/Emile/Documents/MA2/SensUs/data/20190807plasma10ugbelushkin/int/'


data = {}
data_smoothed = {}
for filename in os.listdir(in_dir):
    if filename.endswith(".npy"):
        if 'smoothed' in filename:
            data_smoothed[filename[4:-4]] = np.load(in_dir+filename)
        else:
            data[filename[4:-4]] = np.load(in_dir+filename)
#%%  10ug

back = data_smoothed['back_smoothed']
spot = data_smoothed['spot_smoothed']

y = (back-spot) / (back+spot)

x = np.arange(0, y.shape[0]/2, 0.5)

plt.plot(x,y)
reg_lin = np.polyfit(x, y, 1)
print(reg_lin)
plt.plot(x, np.poly1d(reg_lin)(x))
#%%
in_dir = 'D:/Utilisateurs/Emile/Documents/MA2/SensUs/data/20190806 serum 10ug/ours/int/'


data = {}
data_smoothed = {}
for filename in os.listdir(in_dir):
    if filename.endswith(".npy"):
        if 'smoothed' in filename:
            data_smoothed[filename[4:-4]] = np.load(in_dir+filename)
        else:
            data[filename[4:-4]] = np.load(in_dir+filename)
#%%  10ug

back = data['back']
spot = data['spot']

y = (back-spot) / (back+spot)

x = np.arange(0, y.shape[0]/2, 0.5)

plt.plot(x,y)
reg_lin = np.polyfit(x, y, 1)
print(reg_lin)
plt.plot(x, np.poly1d(reg_lin)(x))

#%%  10ug
in_dir = 'D:/Utilisateurs/Emile/Documents/MA2/SensUs/data/20190806 serum 10ug/ours/apres35min/int/'


data = {}
data_smoothed = {}
for filename in os.listdir(in_dir):
    if filename.endswith(".npy"):
        if 'smoothed' in filename:
            data_smoothed[filename[4:-4]] = np.load(in_dir+filename)
        else:
            data[filename[4:-4]] = np.load(in_dir+filename)
#%%  10ug

back = data['back']
spot = data['spot']

y = (back-spot) / (back+spot)

x = np.arange(0, y.shape[0]/2, 0.5)

plt.plot(x,y)
reg_lin = np.polyfit(x, y, 1)
print(reg_lin)
plt.plot(x, np.poly1d(reg_lin)(x))

#%% 
in_dir = 'D:/Utilisateurs/Emile/Documents/MA2/SensUs/data/intensity/'


data = {}
data_smoothed = {}
for filename in os.listdir(in_dir):
    if filename.endswith(".npy"):
        if 'smoothed' in filename:
            data_smoothed[filename[4:-4]] = np.load(in_dir+filename)
        else:
            data[filename[4:-4]] = np.load(in_dir+filename)

#%%  10ug

#back = data['back_10ugb']
#spot = data['spot_10ugb']
#
#y = (back-spot) / (back+spot)
#x = np.arange(0, y.shape[0]/2, 0.5)
#
#plt.plot(x,y)
#reg_lin = np.polyfit(x, y, 1)
#print(reg_lin)
#plt.plot(x, np.poly1d(reg_lin)(x))

#%% 10ug GOOD MEASUREMENT
back = data['back_10ug']
spot = data['spot_10ug']

y = (back-spot)/(back+spot)
y = y - y.min()

x = np.arange(0, y.shape[0]/2, 0.5)

plt.plot(x,y)
reg_lin = np.polyfit(x, y, 1)
slope_10 = reg_lin[0]
print(reg_lin)
plt.plot(x, np.poly1d(reg_lin)(x))


#%% 5ug GOOD MEASUREMENT
back = data_smoothed['back_smoothed_8ug']
spot = data_smoothed['spot_smoothed_8ug']

y = (back-spot)/(back+spot)
#y = y - y.min()

x = np.arange(0, y.shape[0]/2, 0.5)

x = np.array(x)

plt.plot(x,y)
reg_lin = np.polyfit(x, y, 1)
slope_5 = reg_lin[0]

print(reg_lin)
plt.plot(x, np.poly1d(reg_lin)(x))

#%% 3ug

# back = data['back_3ugb']
# spot = data['spot_3ugb']

# y = (back-spot) / (back+spot)

# x = np.arange(0, y.shape[0]/2, 0.5)

# plt.plot(x,y)
# reg_lin = np.polyfit(x, y, 1)
# print(reg_lin)
# plt.plot(x, np.poly1d(reg_lin)(x))

#%% 3ug GOOD MEASUREMENT
back = data['back_3ug']
spot = data['spot_3ug']

y =(back-spot) / (back+spot)
y = y - y.min()

x = np.arange(0, y.shape[0]/2, 0.5)

plt.plot(x,y)
reg_lin = np.polyfit(x, y, 1)
slope_3 = reg_lin[0]

print(reg_lin)
plt.plot(x, np.poly1d(reg_lin)(x))


#%%  1ug

# back = data['back_1ug']
# spot = data['spot_1ug']

# y =(back-spot) / (back+spot)

# x = np.arange(0, y.shape[0]/2, 0.5)

# plt.plot(x,y)
# reg_lin = np.polyfit(x, y, 1)
# print(reg_lin)
# plt.plot(x, np.poly1d(reg_lin)(x))

#%% 300ng  GOOD MEASUREMENT

back = data['back_300ng']
spot = data['spot_300ng']

y =(back-spot) / (back+spot)
y = y - y.min()

x = np.arange(0, y.shape[0]/2, 0.5)

plt.plot(x,y)
reg_lin = np.polyfit(x, y, 1)
slope_03 = reg_lin[0]

print(reg_lin)
plt.plot(x, np.poly1d(reg_lin)(x))

# #%% 50 ng


# back = data['back_50ng']
# spot = data['spot_50ng']

# y = (back-spot) / (back+spot)

# x = np.arange(0, y.shape[0]/2, 0.5)

# plt.plot(x,y)
# reg_lin = np.polyfit(x, y, 1)
# print(reg_lin)
# plt.plot(x, np.poly1d(reg_lin)(x))

#%% control  GOOD MEASUREMENT

back = data['back_control']
spot = data['spot_control']

y =(back-spot) / (back+spot)
y = y - y.min()

x = np.arange(0, y.shape[0]/2, 0.5)

plt.plot(x,y)
reg_lin = np.polyfit(x, y, 1)
slope_0 = reg_lin[0]

print(reg_lin)
plt.plot(x, np.poly1d(reg_lin)(x))

#%% concentration vs slope plot
#plt.plot([10,5,3,0.3,0],[slope_10,slope_5,slope_3,slope_03,slope_0])

####################  SMOOTHED   ###############################################
#%%  10ug

# back = data_smoothed['back_smoothed_10ugb']
# spot = data_smoothed['spot_smoothed_10ugb']

# y = (back-spot)/(back+spot)

# x = np.arange(0, y.shape[0]/2, 0.5)

# plt.plot(x,y)
# reg_lin = np.polyfit(x, y, 1)
# print(reg_lin)
# plt.plot(x, np.poly1d(reg_lin)(x))

# back = data_smoothed['back_smoothed_10ug']
# spot = data_smoothed['spot_smoothed_10ug']

# y = (back-spot)/(back+spot)
# x = np.arange(0, y.shape[0]/2, 0.5)
# #plt.plot(x,back)

# plt.plot(x,y)
# reg_lin = np.polyfit(x, y, 1)
# print(reg_lin)
# plt.plot(x, np.poly1d(reg_lin)(x))

# #%%
# back = data_smoothed['back_smoothed_8ug']
# spot = data_smoothed['spot_smoothed_8ug']

# y = (back-spot)/(back+spot)

# x = []
# in_dir = 'D:/Utilisateurs/Emile/Documents/MA2/SensUs/data/20190605_ada_8ugml_10ulNP/'
# for filename in os.listdir(in_dir):
#     if filename.endswith(".npy"):
#         x.append(int(filename[6:].strip('.npy')))
# x.sort()

# x = np.array(x)

# plt.plot(x,y)
# reg_lin = np.polyfit(x, y, 1)
# print(reg_lin)
# plt.plot(x, np.poly1d(reg_lin)(x))


# #%% 3ug

# back = data_smoothed['back_smoothed_3ugb']
# spot = data_smoothed['spot_smoothed_3ugb']

# y = (back-spot)/(back+spot)

# x = np.arange(0, y.shape[0]/2, 0.5)

# plt.plot(x,y)
# reg_lin = np.polyfit(x, y, 1)
# print(reg_lin)
# plt.plot(x, np.poly1d(reg_lin)(x))

# #%% 3ug
# back = data_smoothed['back_smoothed_3ug']
# spot = data_smoothed['spot_smoothed_3ug']

# y = (back-spot)/(back+spot)

# x = np.arange(0, y.shape[0]/2, 0.5)

# plt.plot(x,y)
# reg_lin = np.polyfit(x, y, 1)
# print(reg_lin)
# plt.plot(x, np.poly1d(reg_lin)(x))


# #%%  1ug

# back = data_smoothed['back_smoothed_1ug']
# spot = data_smoothed['spot_smoothed_1ug']

# y = (back-spot)/(back+spot)

# x = np.arange(0, y.shape[0]/2, 0.5)
# plt.plot(x,y)
# reg_lin = np.polyfit(x, y, 1)
# print(reg_lin)
# plt.plot(x, np.poly1d(reg_lin)(x))

# #%% 300ng GOOD MEASUERMENT
# back = data_smoothed['back_smoothed_300ng']
# spot = data_smoothed['spot_smoothed_300ng']

# y =(back-spot) / (back+spot)

# x = np.arange(0, y.shape[0]/2, 0.5)

# plt.plot(x,y)
# reg_lin = np.polyfit(x, y, 1)
# print(reg_lin)
# plt.plot(x, np.poly1d(reg_lin)(x))

# #%% 50 ng


# back = data_smoothed['back_smoothed_50ng']
# spot = data_smoothed['spot_smoothed_50ng']

# y = (back-spot)/(back+spot)

# x = np.arange(0, y.shape[0]/2, 0.5)
# plt.plot(x,y)
# reg_lin = np.polyfit(x, y, 1)
# print(reg_lin)
# plt.plot(x, np.poly1d(reg_lin)(x))

# #%% control  GOOD MEASUREMENT

# back = data_smoothed['back_smoothed_control']
# spot = data_smoothed['spot_smoothed_control']

# y =(back-spot) / (back+spot)

# x = np.arange(0, y.shape[0]/2, 0.5)

# plt.plot(x,y)
# reg_lin = np.polyfit(x, y, 1)
# print(reg_lin)
# plt.plot(x, np.poly1d(reg_lin)(x))