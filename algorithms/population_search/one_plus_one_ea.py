#! /usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np

import random

from generic import *

# Structure temporaire à améliorer
alpha=0.1

class OnePlusOneEA(PopulationSearchAlgorithm):

    def __init__ (self, prob, options) :
        """
        Entrées :

        * Un problème donnée instance de la classe Problem.
        Seules les problèmes dont les solution sont des tableaus booléens sont
        acceptée.

        * Un dictionnaire des paramètres des algorithmes

        """

        # La taille de la popilation est toujours 1 pour cet algorithme
        options['mu']=1
        options['lambda']=1

        PopulationSearchAlgorithm.__init__(self, prob, options)


    def make_parent_pop(self):
        """
        Permet de selectionner selon une strategie donnée, qui parmi la
        population courrante (self._pop) va pouvoir se reproduire.

        retourne une liste de solution de self._pop de taille self._mu

        """
        # Population de mu parents choisie aléatoirement de self._pop
        parents = []
        for _ in xrange( len(self._pop) ):
            parents.append( random.choice(self._pop) )
        return parents


    def select_random(self, pop):
        """
        On selectionnne une solution aleatoire de la population donnée

        Entrée : une liste de solutions
        Sortie : une solution (aléatoire)

        """

        return random.choice( pop ).clone()


    def bit_uniform_mutation(self, x) :
        """
        Mutation d'un individu. On modifie uniformément chaque bit avec une probabilité alpha.

        Entrée : une instance de la classe Solution.

        Sortie : la solution modifiée
        """
        if not isinstance(x, BinarySolution) :
            raise TypeError("Algorithm only works on binary solution problems")

        for i in xrange(len(x.solution)):
            if (alpha > random.uniform(0, 1)) :
                x.solution[i] = not x.solution[i]

        return x


    def evolve_pop(self, parents):
        """
        Créer des nouvelles solution par evolution des parents. Les opérateur
        génétique son appliqué ici.

        Entrée : une liste de parents (cf.  make_parent_pop)
        Sortie : une liste de solution enfants de taille self._lambda

        """
        offspring = []
        done = False
        while not done :

            # on prend une solution
            x = self.select_random ( parents )
            self._problem.eval(x)

            # on la modifie avec une mutation uniforme et on la garde seulement si elle est meilleure
            y = x.clone()
            y = self.bit_uniform_mutation( y )
            self._problem.eval(y)

            # on a rajoute a la liste la meilleure solution si elle est faisable
            if self.better(y.value,x.value) and self._problem.feasable(y):
                offspring.append(y)
            else:
                offspring.append(x)


            # on arrête si la population est remplie
            done = len(offspring) == self._lambda

        return offspring

    def make_new_pop(self, offspring):
        """
        Constituer la nouvelle population selon une stratégie de selection
        donnée depuis les enfants et self._pop.

        Entrée : une liste de solutions enfants
        Sortie : une liste de solutions de taille self._mu

        """

        # On tri les enfants
        self.sort_pop(offspring)

        # on garde les mu meilleurs
        survivors = []
        for i in xrange( self._mu ):
            survivors.append( offspring[i] )
        return survivors
