#! /usr/bin/env python
# -*- coding: utf-8 -*-
import random
from generic import *

class HillClimbingLS(Algorithm):

    def __init__(self, prob, x0, options):
        """ Constructeur de la super classe 
        """
        Algorithm.__init__(self, prob, x0)
   
    def get_neighbors(self):
        """ retourner les voisins de la solution courante 
        """ 
        return self._solution.neighbors()

    def filter_neighbors(self, neighbors):
        """ filtrer toutes les solutions violant les contraintes 
        """
        return [ n for n in neighbors if self._problem.feasable(n) ]
    
    def select_next_solution(self, candidates):
        """ Si il y des solutions (après filtrage), retourner la meilleure
        """
        best_candidat = candidates[0]
        best_solution = self._problem.eval(best_candidat)

        for candidat in candidates[1:]:
            current_solution = self._problem.eval(candidat)
            if self.better(current_solution,best_solution):
                best_solution = current_solution
                best_candidat = candidat
        return best_candidat

    def accept(self, new_solution) :
        """ RandomLS accepte toutes les solutions, retourner True
        """

        # ces deux lignes de servent à rien. Mais si dans un autre algorithme
        # il  faut faire un choix, les valeurs des solutions son obtenues
        # comme suit. 
        cur_val = self._solution.value
        new_val = new_solution.value
        
	return self.better(new_val,cur_val)
        #return True
    
  

