#! /usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
from random import shuffle
from generic import *

"""
Un object du sac

"""
class Item(object):
    def __init__(self, vol, val):
        self._vol = vol * 1.0
        self._val = val * 1.0
        self._density = val / vol
        
    @property
    def density(self) :
        return self._density

    @property
    def vol(self) :
        return self._vol

    @property
    def val(self) :
        return self._val
        
"""
La sous-classe de Problem pour le sac a dos

Une solution est un vecteur de booléens, ou chaque element reflète si l'élément 
au même indice est present ou pas dans le sac.

"""
    
class Knapsac(Problem) : 

    def __init__(self, capacity, items,  max_eval=1000):
        Problem.__init__(self, max_eval)
        self._capacity = capacity
        self._available_items = items
        self._name = "Knapsac"
        self._minimize = False
        
    def feasable(self, sol) :
        if not isinstance(sol, BinarySolution):
            raise TypeError("x must be a instance of Solution")
        
        vol = 0
        x = sol.solution
        for i in np.where(x)[0] :
            vol += self._available_items[i].vol
        return vol <= self._capacity

    def eval(self, sol):
        if not isinstance(sol, BinarySolution):
            raise TypeError("x must be a instance of Solution")
        
        self.nb_evaluations += 1
        x = sol.solution
        val = 0
        for i in np.where(x)[0] :
            val += self._available_items[i].val

        sol._value = val*1.0
        
        return val*1.0
            
    def print_solution(self, sol):
        if not isinstance(sol, BinarySolution):
            raise TypeError("x must be a instance of Solution")
        
        val = sol._value
        vol = 0
        x = sol.solution
        for i in np.where(x)[0] :
            vol += self._available_items[i].vol

        return "val:{} vol:{} sol:{}".format(val, vol, str(sol))


    def generate_initial_solution(self, sol_type='empty'):
        
        if sol_type not in [ 'empty', 'random' ] :
            raise ValueError("Unknown inital solution type")

        initial_solution = BinarySolution(dim=len(self._available_items))
        if sol_type is 'random':
            initial_solution = initial_solution.random()
            while not self.feasable(initial_solution) : 
                initial_solution = initial_solution.random()
        return initial_solution



"""

Factory pour generer des instances de sac a dos 

"""
        
def generate_knapsac_instance(prob_type, max_eval, size=20, vol=50):
    """
    Pour générer une instance de problème sac a dos 

    prend : 
       prob_type : type 'small', 'medium', 'large', 'random' 
       max_eval : le nombre d'evaluations maximum alloué
       size : le nombre d'items (uniquement si type est random)
       vol : le volume du sac (uniquement si type est random)

    retourne : une instance de la classe Knapsac

    """
    
    if prob_type not in ['small', 'medium', 'large', 'random'] :
        raise ValueError("Unknown prob_type instance")

    volume = 0
    items = []
    
    if prob_type is 'small' :
        #val:70.0 vol:40.0 sol:1000101111
        volume = 40
        items.append( Item(5, 4))
        items.append( Item(9, 8))
        items.append( Item(2, 3))
        items.append( Item(1, 1))
        items.append( Item(7, 12))
        items.append( Item(8, 4))
        items.append( Item(9, 13))
        items.append( Item(10, 20))
        items.append( Item(4, 7))
        items.append( Item(5, 14))

    elif prob_type is 'medium' :
        #sac  1 1 1 1 1 1 0 0 1 0 0 1 0 0 0 0 0 0 0 0(val:84 , vol:50 )
        volume = 50
        items.append( Item (5, 4))
        items.append( Item (9, 8))
        items.append( Item (2, 3))
        items.append( Item (2, 2))
        items.append( Item (7, 12))
        items.append( Item (8, 4))
        items.append( Item (9, 13))
        items.append( Item (26, 22))
        items.append( Item (4, 7))
        items.append( Item (5, 14))
        items.append( Item (3, 3))
        items.append( Item (9, 7))
        items.append( Item (12, 2))
        items.append( Item (6, 9))
        items.append( Item (5, 3))
        items.append( Item (14, 5))
        items.append( Item (7, 4))
        items.append( Item (1, 6))
        items.append( Item (6, 5))
        items.append( Item (5, 12))

    elif prob_type is 'large' :
        #sac 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 0 0 0 0 0 1 0 0(val:153,vol:103 )
        volume = 103
        items.append( Item (5, 4))
        items.append( Item (9, 8))
        items.append( Item (2, 3))
        items.append( Item (2, 1))
        items.append( Item (7, 12))
        items.append( Item (8, 4))
        items.append( Item (9, 13))
        items.append( Item (26, 20))
        items.append( Item (4, 7))
        items.append( Item (5, 14))
        items.append( Item (3, 3))
        items.append( Item (9, 7))
        items.append( Item (12, 2))
        items.append( Item (6, 9))
        items.append( Item (5, 3))
        items.append( Item (14, 5))
        items.append( Item (24, 24))
        items.append( Item (1, 6))
        items.append( Item (6, 5))
        items.append( Item (5, 12))
        items.append( Item (11, 2))
        items.append( Item (9, 4))
        items.append( Item (1, 3))
        items.append( Item (3, 9))
        items.append( Item (7, 5))
        
    elif prob_type is 'random' :
        volume = vol
        w = np.random.randint(1, 30, size)
        v = np.random.randint(1, 10, size)
        items = [ Item(w[i], v[i]) for i in xrange(size) ]

        
    problem = Knapsac(volume, items, max_eval=max_eval)

    return problem
   



