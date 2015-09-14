# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 14:08:57 2015

@author: Magnus Dahl
"""

class production_simulation(object):
    """ This class is made for simulating the need for production of 
        district heating (production) in a given weather situation
        (weather_data_point). Also the price per MWh and total price
        of the given prodution and stored in fields in the object,
        when the method run_simulation() is run.
        
        """
    
    def __init__(self, weather_data_point, production_model, price_model):
        """ Args:
              weather_data_point: 1d array, must match
                                  the get_production(...)-method from
                                  production_model
              production_model: object, must have method get_production(...)
                                that takes a weather_data_point and returns
                                a value for the production (float)
              price_model: object, must have method get_price(...) that takes
                           a production (float) and returns a price per MWh
                           (float)
                
            Returns:
                production_simulation object
              """
              
        self.weather_data_point = weather_data_point
        self.production_model = production_model
        self.price_model = price_model
        self.production = None
        self.price_per_MWh = None
        self.total_price = None
        
    def run_simulation(self):
        """ Running this calculates the values for the fields:
            production, price_per_MWh and total_price
            
            """
            
        self.production = self.production_model.get_production(\
                                                      self.weather_data_point)
        self.price_per_MWh = self.price_model.get_price(self.production)
        self.total_price = self.price_per_MWh*self.production
        