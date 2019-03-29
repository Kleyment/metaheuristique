#! /usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
from random import shuffle, sample, randrange
from generic import *

"""
La sous-classe de Problem pour la couverture d'ensemble.

Une solution est un vecteur de booléens, ou chaque element reflète si le 
sous ensemble au même indice est present ou pas dans l'union .

"""

class SetCovering(Problem) : 

    def __init__(self, universe, subsets,  max_eval=1000):
        Problem.__init__(self, max_eval)
        self._universe = universe
        self._subsets = subsets
        self._name = "Set Covering"
        self._minimize = True

        # test if the union of all subset is the universe
        U = set()
        for s in subsets:
            U = U.union(s)

        if not U == set(universe) :
            raise ValueError("the union of subsets must be the universe") 
            
    def feasable(self, sol) :
        if not isinstance(sol, BinarySolution):
            raise TypeError("x must be an instance of Solution")
        
        x = sol.solution

        U = set()
        for i in xrange( len(self._subsets) ) :
            if x[i] :
                U = U.union(self._subsets[i] )
        return  U == set(self._universe)


    def eval(self, sol):
        if not isinstance(sol, BinarySolution):
            raise TypeError("x must be an instance of Solution")
        
        self.nb_evaluations += 1
        x = sol.solution
        val = len(np.where(x)[0])

        sol._value = val*1.0
        
        return val*1.0
            

    def print_solution(self, sol):
        if not isinstance(sol, BinarySolution):
            raise TypeError("x must be a instance of Solution")
        x = sol.solution
        val = sol._value 
        str_subsets = ""
        for i in np.where(x)[0] :
             str_subsets +="{"+ ",".join(str(e) for e in self._subsets[i]) +"}"
        
        return "val:{} sol:{}".format(val, str(sol)) 


    def generate_initial_solution(self, sol_type='empty'):
        
        if sol_type not in [ 'empty', 'random' ] :
            raise ValueError("Unknown inital solution type")

        initial_solution = BinarySolution(dim=len(self._subsets))
        initial_solution = BinarySolution(x=np.ones(len(self._subsets),
                                                  dtype=np.bool_))
        
        if sol_type is 'random':
            initial_solution = initial_solution.random()
            while not self.feasable(initial_solution) : 
                initial_solution = initial_solution.random()
        return initial_solution





"""

Factory pour generer des instances de problem de couverture 

"""
        
def generate_set_covering_instance(prob_type, max_eval, size=50, nb_sub=40):
    """
    Pour générer une instance de problème sac a dos 

    prend : 
       prob_type : type 'small', 'medium', 'large', 'random' 
       max_eval : le nombre d'evaluations maximum alloué
       size : la taille de l'univers (uniquement si type est random)
       nb_sub : le nombre de sous-ensembles  (uniquement si type est random)

    retourne : une instance de la classe SetCovering

    """
    if prob_type not in ['small', 'medium', 'large', 'random'] :
        raise ValueError("Unknown prob_type instance")

    universe = [0,1,2,3,4,5,6]
    subsets = []
    
    if prob_type is 'small' :

        universe = range(7)
        subsets =  [[0,1,5,6],
                    [0,1,6],
                    [0,1,2],
                    [4,5,6],
                    [5,6],
                    [3,5],
                    [3]]
        
    if prob_type is 'medium' :
    
        universe = range(30)
        subsets = [[0, 2, 3, 4, 8, 9, 10, 16, 17, 23, 26, 28],
                   [1, 19, 13, 22, 15],
                   [0, 6, 8, 10, 13, 19, 22, 25, 27],
                   [4, 8, 9, 11, 15, 19, 23, 26],
                   [11],
                   [3, 7, 8, 11, 12, 16, 19, 20],
                   [4, 5, 7, 9, 10, 14, 18, 20, 28],
                   [10, 13, 17, 20, 21, 22],
                   [0, 9, 19],
                   [2, 3, 4, 12, 17, 18],
                   [25, 2, 4, 29, 23],
                   [3, 10, 12, 22, 23, 25],
                   [16],
                   [0, 3, 5, 6, 7, 8, 13, 20, 22, 24, 26, 29]]

    if prob_type is 'large' :
        
        universe = range(50)
        subsets = [[40, 42, 3, 20, 31],
                   [34, 4, 40, 14, 48, 46, 36, 29, 30],
                   [49, 7],
                   [32, 38, 39, 42,  20, 24, 29],
                   [27, 9, 43, 46, 14],
                   [0],
                   [16, 35, 37, 6, 43, 46,  26, 30, 31],
                   [0, 2, 35, 49, 43, 26, 30, 31],
                   [32, 33, 35, 4, 5, 11, 46, 48, 29],
                   [16, 45, 23],
                   [3, 46],
                   [32, 27, 7],
                   [6, 7, 41, 45, 17, 18, 21, 23],
                   [32],
                   [17, 15, 9],
                   [32, 35, 4, 8, 41, 11, 44, 13, 22, 28],
                   [18, 45, 46],
                   [16, 3, 39, 10, 11,5, 27, 30],
                   [24, 17, 31],
                   [9],
                   [34, 5, 6, 42, 13, 48, 26, 38],
                   [40, 23],
                   [8, 48, 35, 30, 15],
                   [8, 7, 39],
                   [6, 44, 13, 49, 18, 22, 24],
                   [45],
                   [41, 42, 3, 21, 38],
                   [4, 44],
                   [43, 40, 11, 13, 14, 25],
                   [32, 3, 39, 8, 28, 30],
                   [1, 37, 39, 10, 7, 13, 23, 25, 29, 30],
                   [40, 43, 47],
                   [34, 36, 5, 42, 11, 2, 48],
                   [1, 34, 4],
                   [32, 36, 5, 9, 44, 45, 46, 48, 14, 26],
                   [33, 2, 35, 7, 13, 15, 34, 22, 27, 28],
                   [17, 44, 21, 7],
                   [19, 12]]
    

        
        
    if prob_type is 'random' :
        universe = range(size)
        
        subsets = []
        control = set()
        for i in range( nb_sub - 1):
            sub_size = randrange(size/4)
            sub = set(sample(universe, sub_size))
            subsets.append(list(sub))
            control |= sub
        rest = set(universe) - control     
        if rest:
            subsets.append(list(rest))
            
        
    problem = SetCovering(universe, subsets, max_eval=max_eval)
    return problem 
