#! /usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np

import random 

from generic import *


class RandomPS(PopulationSearchAlgorithm):

    def __init__ (self, prob, options) :
        """
        Entrées : 

        * Un problème donnée instance de la classe Problem.
        Seules les problèmes dont les solution sont des tableaus booléens sont 
        acceptée. 
        
        * Un dictionnaire des paramètres des algorithmes 

        """
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
        

    def bit_flip_mutation(self, x) :
        """ 
        Mutation d'un individu. On modifie un bit aléatoire de la solution.
        
        Entrée : une instance de la classe Solution.

        Sortie : la solution modifiée
        """
        if not isinstance(x, BinarySolution) :
            raise TypeError("Algorithm only works on binary solution problems")
      
        i = random.randint(0, len(x.solution)-1 )
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
            p = self.select_random ( parents )

            # on la modifie 
            p = self.bit_flip_mutation( p )
         
            # on a rajoute a la liste
            offspring.append(p)

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
