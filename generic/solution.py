#! /usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
from random import shuffle

"""
Classe abstraite a concrétiser, voire plus bas.

"""

class Solution(object):

    def __init__(self, dim=None, x=None):
        """ constructeur presque vide  voire les classe concrètes plus bas """
        if dim is None and x is None :
            raise ValueError("Il faut spécifier la dimension ou une solution")

        if dim is None :
            self._dim = len(x)
        else :
            self._dim = dim
        if x is not None :
            self._sol = np.copy(x)

        self._value = None

    @property
    def solution(self):
        return self._sol

    @property
    def value(self):
        return self._value

    def random(self):
        """
        crée une solution aléatoire
        retourne un instance de Solution
        """
        raise NotImplementedError

    def neighbors(self):
        """
        permet de construire l'ensemble des solutions voisines de la solution
	    courante
        retourne ensemble solutions voisines de this
        """
        raise NotImplementedError

    def clone(self):
        """ clone la solution dans une nouvelle instance """
        raise NotImplementedError

    def __str__(self):
        """ une méthode to string """
        raise NotImplementedError

    def __eq__(self, other):
        """
        une méthode pour vérifier l'égalité de deux solutions
        Il faut la même dimention et que les tableaus soient identiques

        """
        if  self._dim != other._dim :
            return False
        if self._sol.shape != other._sol.shape :
            return False
        return (self._sol == other._sol).all()

"""
Classe abstraite pour representer une solution comme un tableau binnaire

"""

class BinarySolution(Solution):

    def __init__(self, dim=None, x=None):
        Solution.__init__(self, dim, x)
        if x is None :
            self._sol = np.zeros(dim, dtype=np.bool_)

    def random(self):
        """ Retourne une solution aléatoire """
        rnd = np.random.random(self._dim) < 0.5
        return BinarySolution(x=rnd)

    def neighbors(self):
        """ Retourne toutes les solutions voisines i.e. differentes de 1 """
        N = []
        for i in xrange(len(self._sol)):
            n = np.copy( self._sol )
            n[i] = not n[i]
            N.append(BinarySolution(x=n))

        # mélanger pour rendre le parcours non déterministe
        shuffle(N)
        return N

    def clone(self):
        """ Pour cloner la solution """
        clone_sol =  BinarySolution( x=self._sol )
        clone_sol._value = self.value
        return clone_sol

    def __str__(self):
        """ une méthode to string pour afficher la solution """
        return "".join([ '1' if i else '0' for i in  self._sol ])



"""
Classe abstraite pour representer une solution comme un tableau de permutation

"""

class PermutationSolution(Solution):

    def __init__(self, dim=None, x=None):
        Solution.__init__(self, dim, x)
        if x is None :
            self._sol = np.zeros(dim, dtype=np.int)

    def random(self):
        """ Retourne une solution aléatoire """
        rnd = np.arange(self._dim, dtype=np.int)
        np.random.shuffle(rnd)
        return PermutationSolution(x=rnd)

    def neighbors(self):
        """
        Retourne toutes les solutions voisines i.e. differentes de 1
        échanger 2 elements du tableau

        """
        N = []
        for i in xrange(len(self._sol)):
            for j in xrange(i+1,len(self._sol)):
                if i != j :
                    n = np.copy( self._sol )
                    tmp = n[i]
                    n[i] = n[j]
                    n[j] = tmp
                    N.append( PermutationSolution (x=n) )

        # mélanger pour rendre le parcour non déterministe
        shuffle(N)
        return N

    def clone(self):
        """ Pour cloner la solution """
        clone_sol = PermutationSolution( x=self._sol )
        clone_sol._value = self.value
        return clone_sol

    def __str__(self):
        """ une méthode to string pour afficher la solution """
        return ",".join([ str(i) for i in  self._sol ])




"""
Classe abstraite pour representer une solution comme un vecteur de réels

"""

class RealSolution(Solution):

    def __init__(self, dim=None, x=None):
        Solution.__init__(self, dim, x)
        if x is None :
            self._sol = np.zeros(dim, dtype=np.float_)

    def random(self):
        """ Retourne une solution aléatoire dans [-5, 5]^dim """
        rnd = np.random.random(self._dim)
        rnd *= 10
        rnd -= 5
        return RealSolution(x=rnd)

    def neighbors(self):
        raise NotImplementedError("Solution réelles n'ont pas de voisinage")

    def clone(self):
        """ Pour cloner la solution """
        clone_sol =  RealSolution( x=self._sol )
        clone_sol._value = self.value
        return clone_sol

    def __str__(self):
        """ une méthode to string pour afficher la solution """
        return ",".join([ str(i) for i in  self._sol ])

"""
Classe abstraite pour representer une solution comme plusieurs vecteurs binaire
Utilisé par le problème des nombres de Schur

"""

class VectorBinarySolution(Solution):

    def __init__(self, dim=None, x=None):
        Solution.__init__(self, dim, x)
        #self._sol=np.zeros((dim,len(x._sol[0])), dtype=np.bool_)
        if x is None :
            self._sol = np.zeros((dim,10000), dtype=np.bool_)
            for i in xrange(10000):
                randomInt=np.random.randint(dim)
                self._sol[randomInt][i]=True

    def random(self):
        """ Retourne une solution aléatoire """
        # On connait déjà les solutions pour n <= 4 donc on commence a 5
        randomInt=np.random.randint(5, high=101)
        #rnd = np.random.random(self._dim) < 0.5
        return VectorBinarySolution(dim=randomInt)

        #0,1,0,1    i: 0 < 4 j: i+1 < 4
        #                    i:0 j: 1 < 4 (1,2,3)
        #                    i:1 j: 2 < 4 (2,3)
        #                    i:2 j: 3 < 4 (3)
        #                    i:3 j: 4 < 4 X
        #1,0,0,0
        #0,0,1,0

        #i 1ère permutation j 2ème permutation
        #l1 1ère liste l2 2ème liste
        #for li < dim li++
        #    if li[i] == True:
        #        l1=li
        #    elif li[j] == True:
        #        l2=li

        #swap(permut1,permut2,l1,l2)
        #temp=l1[permut1];
        #l1[permut1]=l2[permut2]
        #l2[permut2]=temp



    def neighbors(self):
        """ Retourne toutes les solutions voisines i.e. differentes de 1 """
        N = []
        for i in xrange(len(self._sol[0])):
            for j in xrange(i+1, len(self._sol[0])):
                # On essaie de trouver l1 et l2, les listes à permuter
                l1=-1
                l2=-1
                for li in xrange(len(self._sol)):
                    if self._sol[li][i] == True:
                        l1=li
                    if self._sol[li][j] == True:
                        l2=li
                n = np.copy( self._sol )
                new_solution=VectorBinarySolution(x=n)
                new_solution.swap(i,j,l1,l2)
                N.append(new_solution)

        # mélanger pour rendre le parcours non déterministe
        shuffle(N)
        return N


    def swap(self,permut1,permut2,l1,l2):
        """ Permute deux listes aux indices l1 et l2 à la position permut1 et permut2 respectivement."""
        self._sol[l1][permut1]=False
        self._sol[l2][permut2]=False
        self._sol[l1][permut2]=True
        self._sol[l2][permut1]=True

    def clone(self):
        """ Pour cloner la solution """
        clone_sol =  VectorBinarySolution( x=self._sol )
        clone_sol._value = self.value
        return clone_sol

    def __str__(self):
        """ une méthode to string pour afficher la solution """
        string=""
        for i in xrange(len(self._sol)):
            string+="["
            vide=True
            for j in xrange(len(self._sol[i])):
                if (self._sol[i][j]):
                    string+=str(j+1)
                    string+=","
                    vide=False
            # On enlève la virgule finale si besoin
            if vide == False:
                string=string[:-1]
            string+="]\n"
        return string
