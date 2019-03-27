#! /usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
from generic import *
from binary_function_problem import *

"""
La sous-classe de Problem pour le BinVal

"""
    
class BinVal(BinaryFunctionProblem) : 

    def __init__(self, size,  max_eval=1000):
        BinaryFunctionProblem.__init__(self, size, max_eval)
        self._name = "Binval"
        
    def eval(self, sol):
        """ 
        Retourne la valeur de la solution  

        La valeur en décimal
        """

        if not isinstance(sol, BinarySolution):
            raise TypeError("x must be a instance of Solution")
        
        self.nb_evaluations += 1
        x = np.array(sol.solution, dtype=np.int)
        
        val = 0
        for i in xrange(len(x)):
            val +=  x[i] << i

        return val
       
"""
Factory pour generer des instances de BinVal

"""
        
def generate_binval_instance(prob_type, max_eval):
    """
    prend : prob_type : type 'small', 'medium', 'large'
 
    retourne : une instance de la classe BinVal

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

    problem = BinVal(size=size, max_eval=max_eval)
    return problem
