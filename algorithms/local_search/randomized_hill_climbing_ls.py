#! /usr/bin/env python
# -*- coding: utf-8 -*-
import random
from generic import *

class RandomizedHillClimbingLS(LocalSearchAlgorithm):

    def __init__(self, prob, options):
        """ Constructeur de la super classe
        """
        LocalSearchAlgorithm.__init__(self, prob, options)

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

        # On parcourt toute les solutions
        for candidat in candidates[1:]:
            # On évalue les solutions parcourues
            current_solution = self._problem.eval(candidat)
            # Si la solution est meilleure que la solution courante, on sauvegarde la solution (le candidat) et sa valeur (best_solution)
            if self.better(current_solution,best_solution):
                best_solution = current_solution
                best_candidat = candidat
        return best_candidat

    def accept(self, new_solution) :
        """ HillClimbingLS accepte seulement les solutions qui sont meilleures que la solution courante"""

        cur_val = self._solution.value
        new_val = new_solution.value
        # On prend la meilleure solution (better tient compte du fait que le problème soit minimisation ou maximisation)
        return self.better(new_val,cur_val)
