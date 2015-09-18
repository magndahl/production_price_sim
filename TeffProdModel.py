# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 14:59:21 2015

@author: Magnus Dahl
"""

import numpy as np
from scipy.special import erfc

#%% This first section just loads default values for initiation of the class

# this is the same function as Teff_sim in effective_temperature.py, except
# for the normalization of the parameters
def Teff(x, a, b, c, d, e, f):
    """ x must be a matrix with each row being a weather time series in
        this order: Tout, vWind, Toutavg24, vWindavg24, sunRadavg24, Tgrnd100avg24
        The parameters must be normalized, so they already have N multiplied
        into them (a=N). See effective_temperature.pdf
        """
    Teff = a*x[0] + b*x[1] + c*x[2] + d*x[3] + e*x[4] + f*x[5]
    
    return Teff

# This model for the production as a function of temperature or effective temperature
# assumes a superposition of piecewise linear
# functions with the position of the bend being 
# normally distributed read 'production_model.pdf' for documentation    
def P_model_erf(T, P0, B, T0, sigma):
    return B*(T-T0)*0.5*erfc((T-T0)/(np.sqrt(2)*sigma)) \
             - B*sigma/(np.sqrt(2*np.pi))*np.exp(-(T-T0)**2/(2*sigma**2))+P0

Teff_params = np.load('settings/normed_Teff_params.npy')
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
        """ Args:
                Teff_function: Function that takes a weather data point
                                and returns an effective temperature.
                prod_function: Function that takes an effective temperature
                                and returns a production i MW
                residual: Array of weather independent part of the production
            Returns:
                TeffProdModel object
                
                """
        self.Teff_function = Teff_function
        self.prod_function = prod_function
        self.residual = residual
        
    
    def get_production(self, weather_data_point, hour_in_year):
        """ Args:
                weather_data_point: 1d array of a weather data point, must
                                    match the requirements of the Teff_function
                hour_in_year: number of the hour in the year, used for
                                adding the right value of the weather
                                independent residual to the production
            Returns:
                production in MW of
                
            """
        Teff = self.Teff_function(weather_data_point)
        production = self.prod_function(Teff) + self.residual[hour_in_year]
        
        return production