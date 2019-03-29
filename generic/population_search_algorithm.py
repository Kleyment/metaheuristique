#! /usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import math

"""
Classe Abstraite représentant un algorithme de recherche a population

A chaque itération la population interne (self._pop) de taille self._mu  
est modifée et remplacée. 

La meilleure solution trouvée est mise à jour et accessible avec l'attribut 
best_solution.

Les classe concrètes doivent implanter les méthodes suivantes :

make_parent_pop()
evolve_pop(parents)
make_new_pop(offspring)


"""

class PopulationSearchAlgorithm(object):

    def __init__ (self, prob, options) :
        """
        Crée la population initiale et l'évalue 
        
        Entrées : 

        * Un problème donnée instance de la classe Problem.
        * Un dictionnaire des paramètres des algorithmes 

        """
       
        self._problem = prob
        self._mu = options.get('mu', 5 )
        self._lambda = options.get('lambda', 10 )
        
        # Création de la population initiale
        self._pop = [ self._problem.generate_initial_solution(sol_type='random')
                      for i in xrange(self._mu) ]
        
        # Evaluation de la population initiale 
        self.eval_pop(self._pop)
        self.update_stats( self._pop )
        self._max_ever = self.max_value
        self._min_ever = self.min_value
        
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
        
    def make_parent_pop(self):
        """
        Permet de selectionner selon une strategie donnée, qui parmi la 
        population courrante (self._pop) va pouvoir se reproduire.

        retourne une liste de solution de self._pop de taille self._mu

        """
        raise NotImplementedError

    def evolve_pop(self, parents):
        """
        Créer des nouvelles solution par evolution des parents. Les opérateur 
        génétique son appliqué ici. 

        Entrée : une liste de parents (cf.  make_parent_pop)
        Sortie : une liste de solution enfants de taille self._lambda

        """
        raise NotImplementedError

    def make_new_pop(self, offspring):
        """
        Constituer la nouvelle population selon une stratégie de selection 
        donnée depuis les enfants et self._pop.  

        Entrée : une liste de solutions enfants 
        Sortie : une lisre de solutions de taille self._mu

        """
        raise NotImplementedError
     
    def step(self):

        # Selection des parents
        P = self.make_parent_pop()
       
        # évolution et création des enfants 
        O = self.evolve_pop( P )
               
        # évaluation des enfants
        fit = self.eval_pop( O )
               
        # remplacement des parents 
        self._pop = self.make_new_pop ( O )

        # mise a jour des statistiques
        self.update_stats( self._pop )
        
        return self.stop() 
        
    
    def stop(self) :
        """ 
        Un critère d'arrêt atteint  max eval ou plus a définir 
        retourne un boolean vrai si on s'arrête 
        """
        return self._problem.no_more_evals() or self._stop

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
        return "eval:{} val:{} max:{} min:{} [{}]".format(
            self._problem.nb_evaluations,
            self.ave_value, self.max_value, self.min_value,
            self.print_dist())

    def print_final(self):
        """ retourne des infos finale  """
        sol_str = self._problem.print_solution(self._best_solution)
        return "Final solution: eval:{} {}".format(
            self._problem.nb_evaluations, sol_str )
    
 
def _is_finite(numbers):
    """
    Prend un liste de nombres, pour verifié s'il ne sont pas infinit

    """

    for n in numbers :
        if n == float('Inf') or n == float('-Inf'):
            return False
    return True
