#! /usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import copy
import random

from mu_coma_lambda_ga import MuComaLambdaGA
from generic import *

# Structure temporaire à améliorer
alpha=0.1

# Probabilité de croisement
pc=0.2

# Probabilité de mutation
pm=0.2
class MuPlusComaLambdaGA(MuComaLambdaGA):

    def __init__ (self, prob, options) :
        """
        Entrées :

        * Un problème donnée instance de la classe Problem.
        Seules les problèmes dont les solution sont des tableaus booléens sont
        acceptée.

        * Un dictionnaire des paramètres des algorithmes

        """
        MuComaLambdaGA.__init__(self, prob, options)

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

            # On sélectionne les géniteurs
            y,z = self.tournament_selection(parents,2,5)

            y1 = y
            z1 = z
            # On a une certaine probabilité de croisement
            if (pc > random.uniform(0, 1)):
                feasable=False
                # On cherche a obtenir des solutions enfants qui sont valides
                while (not feasable):
                    childs=self.bit_point_crossing(y,z)
                    y1=childs[0]
                    z1=childs[1]
                    feasable=self._problem.feasable(y1) and self._problem.feasable(z1)
                self._problem.eval(y1)
                self._problem.eval(z1)

            # On a une certaine probabilité de mutation
            # On cherche a obtenir des mutations qui sont valides
            if (pm > random.uniform(0, 1)):
                feasable=False
                while (not feasable):
                    y1=self.bit_uniform_mutation(y1)
                    feasable=self._problem.feasable(y1)
                feasable=False
                while ( not feasable):
                    z1=self.bit_uniform_mutation(z1)
                    feasable=self._problem.feasable(z1)
                self._problem.eval(y1)
                self._problem.eval(z1)

            # on a rajoute a la liste
            # les parents
            offspring.append(y)
            offspring.append(z)
            # et les enfants
            offspring.append(y1)
            offspring.append(z1)

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
