#! /usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
from generic import *
from binary_function_problem import *

"""
La sous-classe de Problem pour le LeadingOnes

"""
    
class LeadingOnes(BinaryFunctionProblem) : 

    def __init__(self, size,  max_eval=1000):
        BinaryFunctionProblem.__init__(self, size, max_eval)
        self._name = "Leading ones"
        
    def eval(self, sol):
        """
        Retourne la valeur de la solution 

        la longeur de la suite de 1 depuis le début de la solution   
        """
        
        if not isinstance(sol, BinarySolution):
            raise TypeError("x must be a instance of Solution")
        
        self.nb_evaluations += 1
        x = sol.solution
        
        val = 0
        for i in xrange(len(x)):
            prod = int(x[i])
            for j in xrange(1, i):
                prod *= int(x[j])
            val += prod

        sol._value  = val*1.0
        return sol._value 
           
"""
Factory pour generer des instances de LeadingOnes

"""
        
def generate_leading_ones_instance(prob_type, max_eval):
    """
    prend : prob_type : type 'small', 'medium', 'large'
 
    retourne : une instance de la classe LeadingOnes

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

    problem = LeadingOnes(size=size, max_eval=max_eval)
    return problem
