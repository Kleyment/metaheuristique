#! /usr/bin/env python
# -*- coding: utf-8 -*-
import random
from generic import *

# Structure temporaire à améliorer
alpha=0.8
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


        # On génère une probabilité entre 0 et 1 et on regarde si elle est supérieure à alpha si c'est le cas on fait du hill_climbing
        # Sinon on prend un voisin aléatoire
        if (random.uniform(0, 1) <= alpha) :
            # On parcourt toute les solutions
            for candidat in candidates[1:]:
                # On évalue les solutions parcourues
                current_solution = self._problem.eval(candidat)
                # Si la solution est meilleure que la solution courante, on sauvegarde la solution (le candidat) et sa valeur (best_solution)
                if self.better(current_solution,best_solution):
                    best_solution = current_solution
                    best_candidat = candidat
                return best_candidat
        # On sélectionne un voisin aléatoire si il existe (que l'on prend soin d'évaluer avant)
        if len(candidates) > 0 :
            candidate_random=random.choice(candidates)
            self._problem.eval(candidate_random)
            return candidate_random
        return None


    def accept(self, new_solution) :
        """ RandomizedHillClimbingLS accepte toujours la solution"""

        #cur_val = self._solution.value
        #new_val = self._problem.eval(new_solution)
        return True
