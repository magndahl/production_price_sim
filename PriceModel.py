# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 15:26:21 2015

@author: Magnus Dahl
"""
import numpy as np

config_dict = {'avg':[('Forbraending Lisbjerg', 130, 68.3),
                   ('Renosyd', 122, 19.7),
                   ('Skanderborg flis', 235, 19.9),
                   ('Studstrup vaerket', 297, 910),
                   ('Oliekedler', 850, 10e4)]
                   ,
        'optimistic':[('Forbraending Lisbjerg', 130, 71.1),
                   ('Renosyd', 122, 23.8),
                   ('Skanderborg flis', 235, 24.),
                   ('Studstrup vaerket', 297, 910),
                   ('Oliekedler', 850, 10e4)]
                   ,
    'pessimistic':[('Forbraending Lisbjerg', 130, 41.1),
                   ('Renosyd', 122, 11.9),
                   ('Skanderborg flis', 235, 11.),
                   ('Studstrup vaerket', 297, 910),
                   ('Oliekedler', 850, 10e4)]
                   ,
       'only_SSV':[('Forbraending Lisbjerg', 130, 0.),
                   ('Renosyd', 122, 0.),
                   ('Skanderborg flis', 235, 0.),
                   ('Studstrup vaerket', 297, 910),
                   ('Oliekedler', 850, 10e4)]
                   }
                   

class PriceModel(object):
    
    def __init__(self, plant_price_cap=config_dict['pessimistic']):
        """ Args:
                plant_price_cap: list of tupples specifying plant, price pr MWh
                                    and capacity of the plants, in the order in
                                    which they are turned on
                                    Examples can be found in the config_dict.
            Returns:
                price model object
                
            """
            
        self.plant_price_cap=plant_price_cap
        
    def get_price(self, production):
        """ Args:
                production: production in MWh
            Returns:
                price: price per MWh
                
            """
            
        prod_steps = np.cumsum(zip(*self.plant_price_cap)[-1])
        prod_steps = np.insert(prod_steps, 0, 0) # insert a 0 before the first entry 
    
        weighted_sum = 0
        for i in xrange(len(prod_steps)-1):
            if prod_steps[i] <= production <= prod_steps[i+1]:
                residual_prod = production - prod_steps[i]
                weighted_sum += residual_prod*self.plant_price_cap[i][1]
                return weighted_sum/production
            else:
                weighted_sum += (prod_steps[i+1]-prod_steps[i])*self.plant_price_cap[i][1]
                
    def easy_set_config(self, key):
        """ Simple way of setting the price model configuration using
            defaults from the config_dict.
            
            """
            
        try:
            self.plant_price_cap = config_dict[key]
        except KeyError:
            print 'Error: No such key. No changes made to object.'
            return