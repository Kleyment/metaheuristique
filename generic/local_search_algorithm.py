#! /usr/bin/env python
# -*- coding: utf-8 -*-

from problem import Problem
from solution import Solution

class LocalSearchAlgorithm(object):

    def __init__(self, prob, options):
        """
        Algorithm de rechecrche local generique 
        pramètres : un probleme, et des options.
        """
        if not isinstance(prob, Problem):
            raise TypeError("prob must be a instance of Solution")
        
        self._problem = prob
        self._solution = prob.generate_initial_solution(sol_type='random')
        self._problem.eval(self._solution)
        
        # un critère d'arrête dépandant de l'algorithme
        self._stop = False

        # on enregistre la meilleur solution trouvée
        # utile pour les algorithmes qui autorise la dègradation
        self._best_solution = self._solution.clone()
        
    @property
    def curent_solution(self):
        """ retourne la solution courante """
        return self._solution
    
    @property
    def best_solution(self):
        """ retourne la meilleure solution """
        return self._best_solution
    
    @property
    def name(self):
        """
        Retourne le nom de l'algorythme (non de la classe)
        retourne un string
        """
        return self.__class__.__name__
    
    def get_neighbors(self):
        """
        Retourne la liste des solutions voisines de la solution courante
        retourne une liste de d'instances de Solution
        """
        raise NotImplementedError

        
    def filter_neighbors(self, neighbors):
        """
        Elemine les solutions voisines non valides.
        Dépend du probleme et de l'algo 
        
        prend une liste d'instances de Solution 
        retourne une liste de d'instances de Solution
        """
        raise NotImplementedError

     
    def select_next_solution(self, candidates):
        """
        Retourne une solutions, peut-être pas.
        Dépend du probleme et de l'algo 
        
        prend une liste d'instances de Solution 
        retourne une instances de Solution ou None si pas de solution
        """
        raise NotImplementedError
    
    def accept(self, new_solution) :
        """
        Accepte ou pas la nouvele solution.
        Dépend du probleme et de l'algo 
        
        prend une instance de Solution 
        retourne un booléen, acepter / refusé 
        """
        raise NotImplementedError


    def better(self, v1, v2) :
        """
        En fonction du context minimisation ou maximisation 
        retourn si la valeur de x1 est meilleur que la valeur x2

        Prend : deux valeurs de solution 
        Retourne :  un booléen
        """

        if self._problem.maximize and v1 >= v2:
            return True
        if self._problem.minimize and v1 <= v2:
            return True
        return False
        
    
    def step(self) :
        """ 
        Réalise une iteration 
        retourne booleen vrai si fin, faut sinon 
        """
        # se préparer a arreter
        self._stop = True

        # générer les voisin de la solution courante 
        N = self.get_neighbors()

        # éliminer touts les voisins non feasable (dépend du problème)
        S = self.filter_neighbors(N)

        # choir une solution parmis les voisins
        s = self.select_next_solution(S)

        # accepter ou non la solution 
        if s is not None and self.accept(s) :
            self._solution = s
            self._stop = False

        # remplacer la meilleure solution
        self.update_best_ever()
        
        return self.stop() 
    
    def stop(self) :
        """ 
        Un critère d'arrêt atteint  max eval ou plus a définir 
        retourne un boolean vrai si on s'arrête 
        """
        return self._problem.no_more_evals() or self._stop
        
    def value(self):
        """ Retourne la valeur de la solution courante  """
        return  self._solution.value

    def update_best_ever(self):
        """ Mettre a jour la meilleurs solution rencontrée """ 
        old_val = self._best_solution.value
        new_val = self._solution.value

        if self._problem.maximize and new_val >= old_val:
            self._best_solution = self._solution.clone()
        
        if self._problem.minimize and new_val <= old_val:
            self._best_solution = self._solution.clone()
                        
    def print_step(self):
        """ retourne des infos sur l'itération  """
        sol_str = self._problem.print_solution(self._solution)
        return "eval:{} {}".format(self._problem.nb_evaluations, sol_str )

    def print_final(self):
        """ retourne des infos finale  """
        sol_str = self._problem.print_solution(self._best_solution)
        return "Final solution: eval:{} {}".format(
            self._problem.nb_evaluations, sol_str )
    
