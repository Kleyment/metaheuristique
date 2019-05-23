#! /usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
from random import shuffle
from generic import *

"""
La sous-classe de Problem pour les nombres de Schur

Une solution est une liste de k-vecteurs de n-booléens, ou chaque booléen
reflète si le nombre i/n du vecteur appartient à la partition (la liste) j/k

"""

class Schur(Problem) :

    def __init__(self, k, n, max_eval=1000):
        Problem.__init__(self, max_eval)
        self._name = "Schur"
        self._minimize = True
        self._k=k
        self._n=n

    def feasable(self, sol) :
        """
        On considère qu'une solution est faisable lorsque chaque nombre se trouve dans une et une seule liste.
        Les sommes seront utilisé pour la fonction de fitness.
        """
        if not isinstance(sol, VectorBinarySolution):
            raise TypeError("x must be a instance of Solution")

        for i in xrange(len(sol._sol[0])):
            # Un nombre ne doit etre présent que dans une seule liste
            # On retourne faux si il est présent dans plusieurs listes ou dans aucune
            isInColumn=False
            for li in xrange(len(sol._sol)):
                if sol._sol[li][i] == True:
                    # Faux, il est présent dans plusieurs listes
                    if isInColumn == True:
                        return False
                    else:
                        # Le nombre est présent au moins une fois dans une liste
                        isInColumn=True
            # Faux, après le parcours de la colonne, le nombre n'est dans aucune liste
            if isInColumn == False:
                return False

        # Après le parcours de la ligne, on a vérifié toutes les colonnes, donc la solution est valide
        return True

    def setForbidden(self, forbiddenTable, forbiddenNumber):
        if forbiddenNumber <= len(forbiddenTable):
            forbiddenTable[forbiddenNumber-1]=True

    def eval(self, sol):
        if not isinstance(sol, VectorBinarySolution):
            raise TypeError("x must be a instance of Solution")

        self.nb_evaluations += 1
        # On traduit la liste de booléens en liste d'entier (en fonction des valeurs à True)
        liste_globale = []
        for i in xrange(len(sol._sol)):
            liste_locale = []
            for j in xrange(len(sol._sol[i])):
                if (sol._sol[i][j]):
                    liste_locale.append(j+1)
            liste_globale.append(liste_locale)

        #On crée un tableau à double entrée pour noter les nombres interdits (de meme taille avec booléen)
        forbidden_global = np.zeros((self._k,self._n), dtype=np.bool_)

        for i in xrange(len(liste_globale)):
            for j in xrange(len(liste_globale[i])):
                for k in xrange(j+1, len(liste_globale[i])):
                    #print(forbidden_global[i])
                    self.setForbidden(forbidden_global[i],liste_globale[i][j]*2)
                    self.setForbidden(forbidden_global[i],liste_globale[i][k]*2)
                    self.setForbidden(forbidden_global[i],liste_globale[i][j]+liste_globale[i][k])
        #print(forbidden_global)

        fitness=0
        # On refait un parcours de toute la solution et on ajoute 1 à chaque somme interdite
        for i in xrange(len(sol._sol)):
            for j in xrange(len(sol._sol[i])):
                if (sol._sol[i][j] == True and forbidden_global[i][j] == True):
                    fitness+=1
        sol._value=fitness
        return fitness

    def print_solution(self, sol):
        if not isinstance(sol, VectorBinarySolution):
            raise TypeError("x must be a instance of Solution")
        return "val:{} sol:\n{}".format(sol._value,str(sol))


    def generate_initial_solution(self, sol_type='empty'):

        if sol_type not in [ 'empty', 'random' ] :
            raise ValueError("Unknown inital solution type")

        initial_solution = VectorBinarySolution(dim=self._k)
        initial_solution._sol = np.zeros((self._k,self._n), dtype=np.bool_)
        for i in xrange(self._n):
            randomInt=np.random.randint(self._k)
            initial_solution._sol[randomInt][i]=True
        self.print_solution(initial_solution)
        return initial_solution



"""

Factory pour generer des problèmes de schur

"""

def generate_schur_instance(prob_type, max_eval, k=-1, n=-1):
    """
    Pour générer une instance du problème des nombres de Schur

    prend :
       prob_type : type 'small', 'medium', 'large', 'random'
       max_eval : le nombre d'evaluations maximum alloué
       k : le nombre de listes (optionnel uniquement si type est random)
       n : le nombre à tester (optionnel uniquement si type est random)

    retourne : une instance de la classe Schur

    """

    if prob_type not in ['small', 'medium', 'large', 'random'] :
        raise ValueError("Unknown prob_type instance")

    volume = 0
    items = []

    if prob_type is 'small' :
        #Pour tester  fitness:0 (solution acceptable), k:3, n:13
        #[1,0,0,1,0,0,0,0,0,1,0,0,1]
        #[0,1,1,0,0,0,0,0,0,0,1,1,0]
        #[0,0,0,0,1,1,1,1,1,0,0,0,0]
        k=3
        n=13


    elif prob_type is 'medium' :
        #Pour tester  fitness:0 (solution acceptable), k:5, n:160
        k=5
        n=160

    elif prob_type is 'large' :
        k=6
        n=400

    elif prob_type is 'random' :
        if k == -1:
            k=np.random.randint(5, high=101)
        if n == -1:
            k=np.random.randint(160, high=1000)


    problem = Schur(k, n, max_eval=max_eval)

    return problem
