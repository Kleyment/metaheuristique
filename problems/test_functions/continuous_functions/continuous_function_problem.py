#! /usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
from random import shuffle
from generic import *

"""
La sous-classe de Problem pour les problemes de fonctions binnaires

OneMax, BinVal, LeadingOnes

Porblèmes de maximization, sans contraintes.

"""
class ContinuousFunctionProblem(Problem) : 

    def __init__(self, size,  max_eval=1000):
        Problem.__init__(self, max_eval)
        self._size = size
        self._name = "Generic continuous function "
        self._minimize = True
        
    def feasable(self, sol) :
        """ pas de contraintes """
        return True
        
    def eval(self, sol):
        """
        Retourne la valeur de la solution 
        
        """
        raise NotImplementedError
       
    def print_solution(self, sol):
        """ Retourne la solution sous forme de string """
        
        if not isinstance(sol, RealSolution):
            raise TypeError("x must be a instance of Solution")
        
        self.nb_evaluations -= 1 # on ne compte cette evaluation
        self.eval(sol)
        return "val:{} sol:{}".format(sol.value, str(sol))

    def generate_initial_solution(self, sol_type='empty'):
        """ 
        Genérer une solution initial vide ou aléatoire 
        Retourne une instance de BinarySolution
        
        """
        if sol_type not in [ 'empty', 'random' ] :
            raise ValueError("Unknown inital solution type")

        initial_solution = RealSolution(dim=self._size)
        if sol_type is 'random':
            initial_solution = initial_solution.random()
        return initial_solution
    

