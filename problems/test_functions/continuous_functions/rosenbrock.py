#! /usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
from generic import *
from continuous_function_problem import *

"""
La sous-classe de Problem pour le OneMax

"""
    
class Rosenbrock(ContinuousFunctionProblem) : 

    def __init__(self, size,  max_eval=1000):
        ContinuousFunctionProblem.__init__(self, size, max_eval)
        self._name = "Rosenbrock"

    def eval(self, sol):

        if not isinstance(sol, RealSolution):
            raise TypeError("x must be a instance of Solution")
    
        self.nb_evaluations += 1
        x = sol.solution
        val=[100.*(x[i]**2-x[i+1])**2 +(1.-x[i])**2 for i in xrange(len(x)-1)]
        sol._value = sum(val)
        return sol._value
"""
Factory pour generer des instances de OneMax

"""
        
def generate_rosenbrock_instance(prob_type, max_eval):
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
        
    problem = Rosenbrock(size=size, max_eval=max_eval)
    return problem
