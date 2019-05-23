#! /usr/bin/env python
# -*- coding: utf-8 -*-
import random
from generic import *

class OnePlusOneES(LocalSearchAlgorithm):

    def __init__(self, prob, options):
        """ Constructeur de la super classe
        """

        EvolutionStrategy.__init__(self, prob, options)

    def sample_solutions(self):
        """
        Echantillonage de lambda solutions selon la distribution courrente

        Sortie : une liste de lambda solutions
        """
        x=[]
        x.append(self._m.clone())



        #Un vecteur de 1 double tiré aléatoirement avec une distribution gaussienne
        z=self.normal(1)
        for i in xrange(z):
            x[i]=z[i]*self._sigma

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
#self._problem._size
#normal pour avoir z

#sample solution première indentation
#O tableau 1 sol

# sigma * z coordonnées par coordonnées
#clone solution

# rien dans update_m et tous dans sigma
