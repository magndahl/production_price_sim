# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 14:59:21 2015

@author: Magnus Dahl
"""

import numpy as np
from scipy.special import erfc

#%% This first section just loads default values for initiation of the class

# this is the same function as Teff_sim in effective_temperature.py
def Teff(x, c, e, f, h, i):
    """ x must be a matrix with each row being a weather time series in
        this order: Tout, vWind, Toutavg24, vWindavg24, sunRadavg24, Tgrnd100avg24
        
        """
    Teff = x[0,:] + c*x[1,:] + e*x[2,:] + f*x[3,:] + h*x[4,:] + i*x[5,:]
    Teff *= np.mean(x[0,:])/np.mean(Teff)
    return Teff

# This model for the production as a function of temperature or effective temperature
# assumes a superposition of piecewise linear
# functions with the position of the bend being 
# normally distributed read 'production_model.pdf' for documentation    
def P_model_erf(T, P0, B, T0, sigma):
    return B*(T-T0)*0.5*erfc((T-T0)/(np.sqrt(2)*sigma)) \
             - B*sigma/(np.sqrt(2*np.pi))*np.exp(-(T-T0)**2/(2*sigma**2))+P0

Teff_params = np.load('settings/Teff_params_allhours.npy')
def default_Teff(x):
    return Teff(x, *Teff_params)    

P_model_params = np.load('settings/fit_params_all_h0-23.npy')
def default_prod_model(T):
    return P_model_erf(T, *P_model_params)    
    
default_residual = np.load('settings/weather_indep_residuals.npy')


#%%  Here comes the class definition
    
class TeffProdModel(object):
    
    def __init__(self, Teff_function=default_Teff,\
                       prod_function=default_prod_model,\
                       residual=default_residual):
        self.Teff_function = Teff_function
        self.prod_function = prod_function
        self.residual = residual
        
    
    def get_production(self, weather_data_point, hour_in_year):
        Teff = self.Teff_function(weather_data_point)
        production = self.prod_function(Teff) + self.residual[hour_in_year]
        
        return production