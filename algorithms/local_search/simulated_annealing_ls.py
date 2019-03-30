#! /usr/bin/env python
# -*- coding: utf-8 -*-
import random
import math
from generic import *

# Structure temporaire à améliorer
# Température initiale
initalTemp=300
# Coefficient de baisse de température
gamma=0.99
class SimulatedAnnealingLS(LocalSearchAlgorithm):

    def __init__(self, prob, options):
        """ Constructeur de la super classe
        """
        LocalSearchAlgorithm.__init__(self, prob, options)
        self.temperature=initalTemp

    def get_neighbors(self):
        """ retourner les voisins de la solution courante
        """
        return self._solution.neighbors()

    def filter_neighbors(self, neighbors):
        """ filtrer toutes les solutions violant les contraintes
        """
        return [ n for n in neighbors if self._problem.feasable(n) ]

    def select_next_solution(self, candidates):
        """ Si il y des solutions (après filtrage), retourner une solution au hasard
        """
        # On sélectionne un voisin aléatoire si il existe (que l'on prend soin d'évaluer avant)
        if len(candidates) > 0 :
            candidate_random=random.choice(candidates)
            self._problem.eval(candidate_random)
            return candidate_random
        return None


    def accept(self, new_solution) :
        """ SimulatedAnnealingLS accepte toujours les solutions meilleures mais seulement avec une probabilité alpha les solutions moins bonnes"""

        # Soit la solution est meilleure auquel cas on l'accepte toujours
        if self.better(new_solution.value,self._solution.value) :
            # Mise à jour de la température
            self.temperature=self.temperature*gamma
            return True
        # Soit la solution est moins bonne et dans ce cas on a une probabilité de l'accepter dépendant de l'aléatoire et de la température
        else :
            alpha=math.exp(-abs(self._solution.value-new_solution.value)/self.temperature)
            # Mise à jour de la température
            self.temperature=self.temperature*gamma
            if (alpha > random.uniform(0, 1)) :
                return True
            else :
                return False
        #cur_val = self._solution.value
        #new_val = self._problem.eval(new_solution)
        return True
