# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 15:46:11 2015

@author: Magnus Dahl
"""
import numpy as np
import datetime as dt

from ProductionSimulation import ProductionSimulation
from TeffProdModel import TeffProdModel
from PriceModel import PriceModel

production_model = TeffProdModel()
price_model = PriceModel()


#% load weatherdata
varlist = ['Tout', 'vWind', 'Toutavg24', 'vWindavg24',\
        'sunRadavg24', 'Tgrnd100avg24'] 
dataarrays = []
path = '../cleaned_cropped_data/'
suffix = '_all_h0-23.npy'
for v in varlist:
    filename = v + suffix
    dataarrays.append(np.load(path+filename))
weatherdata = np.array(dataarrays)

timesteps = np.load(path + 'timestep' + suffix)
allhours2014 = [dt.datetime(2014,1,1,0,0) + dt.timedelta(hours=x) for x in xrange(24*365)]
hours_in_year = [allhours2014.index(t) for t in timesteps]


mysim = ProductionSimulation(weather_data_point=weatherdata[:,0],
                             hour_in_year=0, 
                             production_model=production_model,
                             price_model=price_model)
                             
            
            
for i in range(10):
    mysim.weather_data_point = weatherdata[:,i]
    mysim.hour_in_year = i
    mysim.run_simulation()
    print mysim.production, mysim.price_per_MWh, mysim.total_price