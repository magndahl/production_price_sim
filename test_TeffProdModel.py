# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 14:45:26 2015

@author: Magnus Dahl
"""
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt

from TeffProdModel import TeffProdModel
plt.close('all')

model = TeffProdModel()

varlist = ['Tout', 'vWind', 'Toutavg24', 'vWindavg24',\
        'sunRadavg24', 'Tgrnd100avg24']
    
dataarrays = []

path = '../cleaned_cropped_data/'
suffix = '_all_h0-23.npy'
for v in varlist:
    filename = v + suffix
    dataarrays.append(np.load(path+filename))
weatherdata = np.array(dataarrays)

loaded_production = np.load(path + 'prod' + suffix)

timesteps = np.load(path + 'timestep' + suffix)
allhours2014 = [dt.datetime(2014,1,1,0,0) + dt.timedelta(hours=x) for x in xrange(24*365)]
hours_in_year = [allhours2014.index(t) for t in timesteps]

modeled_prod = []

for i in range(len(hours_in_year)):
    modeled_prod.append(model.get_production(weatherdata[:,i], hours_in_year[i]))
    

plt.figure()
plt.plot(loaded_production, 'b', label='Actual production')
plt.plot(modeled_prod, 'r--', label='Modeled production')
plt.xlabel('Hour')
plt.ylabel('Production [MW]')    

abs_difference = np.abs(loaded_production - np.array(modeled_prod))
 # the maximum deviation from the model has to be below 1
assert(max(abs_difference) < 1.0), 'Model deviates from actual production!'