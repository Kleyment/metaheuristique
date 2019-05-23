#! /usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import random

from problem import Problem
from solution import Solution
from population_search_algorithm import PopulationSearchAlgorithm

class EvolutionStrategy(object):

    def __init__(self, prob, options):
        """
        Algorithm de stratégie d'evolution générique

        Entrées :

        * Un problème donnée instance de la classe Problem.
        * Un dictionnaire des paramètres des algorithmes

        """
        if not isinstance(prob, Problem):
            raise TypeError("prob must be a instance of Problem")

        self._problem = prob
        self._mu = options.get('mu', 5 )
        self._lambda = options.get('lambda', 10 )
        self._sigma = options.get('sigma', 1.0 )

        # Création de la solution intiale initiale
        self._m = self._problem.generate_initial_solution(sol_type='random')
        self._problem.eval(self._m )

        self._best_solution = self._m.clone()
        self.min_value = self._m.value
        self.max_value = self._m.value
        self._max_ever = self._m.value
        self._min_ever = self._m.value

        # un critère d'arrête dépandant de l'algorithme
        self._stop = False

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

    def eval_pop(self, pop):
        """
        Evaluation d'une population de solution candidates

        Entrée : une liste d'instances de la classe Solution
        Sortie : la liste des valeurs des solution

        Note : les valeurs de fitness sont aussi stockés dans les solutions.

        Note : les solutions infeasable ont une fitness infini
        """
        vals = [ self._problem.eval(x) for x in pop]
        feasable = [ self._problem.feasable(x) for x in pop ]

        for i in xrange(len(feasable)) :
            if not feasable[i] :
                vals[i] = float("inf")
                if self._problem.maximize :
                    vals[i] = float("-inf")
                pop[i]._value = vals[i]

        # retourne le tableau des fitness
        return vals

    def update_stats(self, pop):
        """
        Mise à jours des statistique de la population. La meilleure solution
        est mise à jour ainsi que les valeurs de fitness maximun, minimum,
        et moyenne.

        Entrée : une population de solution

        Note : cette population a déjà été évaluée
        """
        vals = [ x.value for x in pop ]

        self.min_value = min(vals)
        self.max_value = max(vals)
        self.ave_value = np.average(vals)

        # on enregistre la meilleure solution trouvée
        if self._problem.maximize :
            self._best_solution = pop[np.argmax(vals)].clone()
        if self._problem.minimize :
            self._best_solution = pop[np.argmin(vals)].clone()

    def sort_pop(self, pop) :
        """
        Trie la population par ordre de fitness pop[0] est la meilleure
        solution

        Entrée : une liste de solution evaluée.

        Note : le tri est fait en place

        """
        if self._problem.maximize :
            pop.sort(key=lambda x: x.value, reverse=True)
        else:
            pop.sort(key=lambda x: x.value)


    def print_dist(self):
        """
        Pour afficher graphiqument les stats

        """

        l = 20

        dist=list('.'*(l+2))

        if self.max_value > self._max_ever:
            self._max_ever = self.max_value
        if self.min_value < self._min_ever:
            self._min_ever = self.min_value

        if _is_finite( [
                self._max_ever,
                self._min_ever,
                self.max_value, 
                self.min_value,
                self.ave_value ] ):

            a = l/(self._max_ever-self._min_ever)
            b = - (l*self._min_ever)/(self._max_ever-self._min_ever)

            idx_max = int(a*self.max_value + b)
            idx_ave = int(a*self.ave_value + b)
            idx_min = int(a*self.min_value + b)
            dist[idx_max] ='|'
            dist[idx_min] ='|'
            dist[idx_ave] ='|'

        return "".join(dist)

    def print_step(self):
        """ retourne des infos sur l'itération  """
        return "eval:{} val:{} max:{} min:{} sig:{} [{}]".format(
            self._problem.nb_evaluations,
            self.ave_value, self.max_value, self.min_value,
            self._sigma,
            self.print_dist())

    def print_final(self):
        """ retourne des infos finale  """
        sol_str = self._problem.print_solution(self._best_solution)
        return "Final solution: eval:{} {}".format(
            self._problem.nb_evaluations, sol_str )



    def normal(self, n):
        """
        Echantillonne selon une loi normale (0,1) un vecteur de dimension n

        Entrée : un entier la dimension
        Sortie : une liste de de n flotants
        """
        return [ random.gauss(0.0, 1.0) for i in xrange(n) ]


    def sample_solutions(self):
        """
        Echantillonage de lambda solutions selon la distribution courrente

        Sortie : une liste de lambda solutions
        """
        raise NotImplementedError

    def update_sigma(self, sample):

        """
        Mise à jour de pas de mutation sigma selon une règle donnée
        """
        raise NotImplementedError

    def update_m(self, sample):
        """
        Mise à jour de la moyenne de la distribution
        """
        raise NotImplementedError



    def step(self):

        # Echantillonage de solutions
        O = self.sample_solutions()

        # évaluation et tri des solutions
        fit = self.eval_pop( O )
        self.sort_pop(O)

        # Mis a jour des parammetre de ls distribution
        self.update_m(O)
        self.update_sigma(O)

        # mise a jour des statistiques
        self.update_stats( O )

        return self.stop()


    def stop(self) :
        """
        Un critère d'arrêt atteint  max eval ou plus a définir
        retourne un boolean vrai si on s'arrête
        """
        return self._problem.no_more_evals() or self._stop



def _is_finite(numbers):
    """
    Prend un liste de nombres, pour verifié s'il ne sont pas infinit

    """

    for n in numbers :
        if n == float('Inf') or n == float('-Inf'):
            return False
    return True
