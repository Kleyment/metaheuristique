#! /usr/bin/env python
# -*- coding: utf-8 -*-
from generic import *
from collections import deque

# Structure temporaire à améliorer
# Taille de la liste taboue
tabuSize=50
class TabuLS(LocalSearchAlgorithm):

    def __init__(self, prob, options):
        """ Constructeur de la super classe
        """
        LocalSearchAlgorithm.__init__(self, prob, options)
        self.tabuList=deque(maxlen=tabuSize)

    def get_neighbors(self):
        """ retourner les voisins de la solution courante
        """
        return self._solution.neighbors()

    def filter_neighbors(self, neighbors):
        """ filtrer toutes les solutions violant les contraintes
        """
        return [ n for n in neighbors if self._problem.feasable(n) ]

    def select_next_solution(self, candidates):
        """ Si il y des solutions (après filtrage), retourner la meilleure qui n'est pas dans la liste taboue
        """
        # Au départ aucune solution valide n'est trouvée
        best_candidat=None

        # On parcourt toute les solutions
        for candidat in candidates[1:]:
            # Si il n'est pas dans la liste taboue
            if candidat not in self.tabuList :
                # Si on a pas encore de candidat valide
                if best_candidat is None :
                    best_candidat = candidat
                    best_solution = self._problem.eval(best_candidat)
                else :
                    # On évalue les solutions parcourues
                    current_solution = self._problem.eval(candidat)
                    # Si la solution est meilleure que la solution courante, on sauvegarde la solution (le candidat) et sa valeur (best_solution)
                    if self.better(current_solution,best_solution):
                            best_solution = current_solution
                            best_candidat = candidat
        # On retourne le candidat qu'il soit nul ou non
        return best_candidat

    def accept(self, new_solution) :
        """ TabuLS accepte toujours la solution"""

        # Si la solution n'est pas nulle on l'ajoute à la liste taboue
        if new_solution is not None:

            # Si la taille de la liste taboue est la taille maximale-1 alors on supprime le premier élément (FIFO)
            if (len(self.tabuList) == self.tabuList.maxlen-1) :
                self.tabuList.popleft()

            self.tabuList.append(new_solution)

        return True
