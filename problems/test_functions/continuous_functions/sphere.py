#! /usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
from generic import *
from continuous_function_problem import *

"""
La sous-classe de Problem pour le OneMax

"""
    
class Sphere(ContinuousFunctionProblem) : 

    def __init__(self, size,  max_eval=1000):
        ContinuousFunctionProblem.__init__(self, size, max_eval)
        self._name = "Sphere"

    def eval(self, sol):

        if not isinstance(sol, RealSolution):
            raise TypeError("x must be a instance of Solution")
    
        self.nb_evaluations += 1
        x = sol.solution
        val = sum((x + 0)**2)
        sol._value = val
        return sol._value
"""
Factory pour generer des instances de OneMax

"""
        
def generate_sphere_instance(prob_type, max_eval):
    """
    prend : prob_type : type 'small', 'medium', 'large'
    retourne : une instance de la classe OneMax

    """
    if prob_type not in ['small', 'medium', 'large'] :
        raise ValueError("Unknown prob_type instance")
    
    size = 0
    if prob_type is 'small' :
        size = 10
    elif prob_type is 'medium' :
        size = 30
    elif prob_type is 'large' :
        size = 100
        
    problem = Sphere(size=size, max_eval=max_eval)
    return problem
