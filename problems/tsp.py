#! /usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
from random import shuffle
from generic import *


"""
La sous-classe de Problem pour le TSP

Une solution est un ordre des villes (ordre du parcours).  

"""
    
class TSP(Problem) : 

    def __init__(self, cities,  dist_matrix, max_eval=1000):
        Problem.__init__(self, max_eval)
        self._cities = cities
        self._dist_matrix = dist_matrix
        self._name = "TSP"
        self._minimize = True

    def feasable(self, sol) :   
        return True
        
    def eval(self, sol):
        self.nb_evaluations += 1
        x = sol.solution

        val = 0 
        for i in xrange(0, len(self._cities)) :
            c1 = x[i-1]
            c2 = x[i]
            val += self._dist_matrix[c1,c2]

        sol._value = val*1.0 
        return val*1.0

    def print_solution(self, sol):
        return "val:{} sol:{}".format(sol._value, str(sol))

    def generate_initial_solution(self,  sol_type='empty'):
        if sol_type not in [ 'empty', 'random' ] :
            raise ValueError("Unknown inital solution type")
        
        initial_solution = PermutationSolution(dim=len(self._cities))
        if sol_type is 'random':
            initial_solution = initial_solution.random()
        return initial_solution

    def draw_solution(self, sol, fname) :
        import matplotlib.pyplot as plt
        
        x = sol.solution
        X = self._cities[x,0]
        Y = self._cities[x,1]
        
        fig = plt.figure(num=None, figsize=(4.5,4.5), dpi=100)
        axes = fig.add_subplot(111)
        axes.scatter(X, Y, lw=1, alpha=0.5)
        axes.plot(X, Y, lw=2)
        axes.plot( [X[-1], X[0]], [Y[-1], Y[0]], lw=2)
        axes.grid( color="0.5", linestyle='--', linewidth=1)
        axes.set_aspect(1)
        axes.set_ylim([-0.02, 1.02])
        axes.set_xlim([-0.02, 1.02])
        plt.savefig(fname, bbox_inches='tight')
        plt.close(axes.get_figure())

        


"""

Factory pour generer des instances de TSP

"""
        
def generate_tsp_instance(prob_type, max_eval, size=20):
    """
    Pour générer une instance de problème TSP

    prend : 
       prob_type : type 'small', 'medium', 'large', 'random' 
       max_eval : le nombre d'evaluations maximum alloué
       size : le nombre d'items (uniquement si type est random)

    retourne : une instance de la classe TSP

    """
    
    if prob_type not in ['small', 'medium', 'large', 'random'] :
        raise ValueError("Unknown prob_type instance")
    
    size = 0
    grid_size = 0
    C = None
    if prob_type is 'small' :
        size = 16
        grid_size = int(np.sqrt(size))

    if prob_type is 'medium' :
        size = 36
        grid_size = int(np.sqrt(size))

    if prob_type is 'large' :
        size = 49
        grid_size = int(np.sqrt(size))

    if prob_type in ['small', 'medium', 'large']:
        x = np.linspace(0, 1, grid_size)
        y = np.linspace(0, 1, grid_size)
        xv, yv = np.meshgrid(x, y, indexing='ij')
        C = np.zeros( (grid_size**2, 2) )
        count = 0
        for i in xrange(len(x)):
            for j in xrange(len(y)):
                C[count,0] = xv[i,j] 
                C[count,1] = yv[i,j]
                count += 1
                
    if prob_type is 'random' :
        C = np.random.sample( (size, 2) )

        
    D = np.zeros( size * size , dtype=np.float ).reshape(size , size)
    for i in xrange(size) :
        for j in xrange(size) :
            x1 = C[i,0]
            y1 = C[i,1]
            x2 = C[j,0]
            y2 = C[j,1]
                
            dist = np.sqrt( (x1-x2)**2 + (y1-y2)**2 )
            D[i,j] = dist
            D[j,i] = dist
                


                
    problem = TSP(C, D, max_eval=max_eval)
    return problem 
