#! /usr/bin/env python
# -*- coding: utf-8 -*-

from solution  import Solution

class Problem(object):

    def __init__(self, max_eval):
        self._max_eval = max_eval
        self.nb_evaluations = 0
        self._name = 'Generic problem'
        self._minimize = False

    @property
    def minimize(self) :
        return self._minimize

    @property
    def maximize(self) :
        return not self._minimize


    @property
    def name(self):
        """ Retourne le petit nom du problème """
        return self._name
    
    def reset(self):
        """ remets le compteur a zero """
        self.nb_evaluations = 0
    
    def no_more_evals(self):
        """ Retourne vrai ou faux """
        return self.nb_evaluations > self._max_eval
        
    def eval(self, sol):
        """
        Méthode qui retourne la valeur de la solution sol
        
        pramètres sol une instance de Solution
        retourne un Float sa valeur
        
        """
        raise NotImplementedError

    def feasable(self, sol) :
        """
        Méthode qui retourne si la solution est feasable
        
        pramètres sol une instance de Solution
        retourne un booléen
        
        """
        raise NotImplementedError

    def print_solution(self, sol):
        """
        Méthode qui retourne la solution sous forme de string
        
        pramètres sol une instance de Solution
        retourne un string 
        
        """
        raise NotImplementedError

    def draw_solution(self, sol, fname) :
    
        """
        Méthode dessine la solution quand c'est possible
        
        Note : le dessin est possible que pour certain problème. 
        comme le TSP par example. 

        pramètres : 
            sol une instance de Solution
            fname : le nom du fichier image de sortie  
        
        """
        raise NotImplementedError
