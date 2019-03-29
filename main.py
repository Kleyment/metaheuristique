#! /usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np

from generic import *
from algorithms import *
from problems import *
from misc import *


def plot_by_evaluation(data, fname):
    """
    Dessine des courbes de valeurs de la solution courante vs.
    nombre évaluations. Il y a une courbe par exécution.

    Abcisse :le nombre d'évaluations
    Ordonnée : la valeur de la solution courante
    """

    ax = start_figure()
    for d in data:
        ax.plot(d[1], d[2], lw=0.3, color="0.5")
    finish_figure(ax, fname, 'Evaluations', 'Value')


def plot_by_final_solution(data, names, fname):
    """
    Dessine les distributions des valeurs des solutions finales de chaque
    exécution. Autant de boites à moustaches que d'algorithmes testés.

    Ordonnée : la valeur de la solution finale
    """

    ax = start_figure()
    plot_boxplot(ax, data, names)
    finish_figure(ax, fname, '', 'Value')


def split_stat_line(line):
    """
    Découpe une ligne de statistique et retourne les valeur
    itération, évaluations, valeur, sous forme de tuple,

    Ex. si la ligne contient :  "... iter:3 eval:420 val:79.0 ... "
    le valeur retournées sont : 3, 420, 79.0

    Prend un string
    Retourne un tuple
    """

    data = line.split()
    i, e, v = 0, 0, 0
    for d in data :
        if d.startswith('eval') :
            e = float(d.split(':')[1])
        if d.startswith('val') :
            v = float(d.split(':')[1])
        if d.startswith('iter') :
            i = float(d.split(':')[1])
    return i,e,v


def run_algorithm(algo, max_iter, screen=True) :
    """
    Lance une instance d'un algorithme de recherche et retourne
    ses resultas.

    prend :
       algo : une instance de la classe Algorithme
       max_iter : entier le nombre d'itération maximum
       screen : booléen pour afficher ou non une ligne de stat par itération

    retourne :
       un entier : le nombre d'itérations consomé
       un tableau : chaque case contient un tuple
          (itération, évaluation, valeur) cf. split_stat_line plus haut. Il y
          a autant de case que d'itération
    """

    stats = []
    done = False
    it = 0

    # sauter une ligne
    if screen :
        print

    # tan que pas fini
    while not done:
        it += 1

        # exécuter une itération de l'algorithme
        finished = algo.step()

        # récupérer les statistiques sur la solution courante
        stat_line = "iter:{} {}".format(it, algo.print_step())
        stats.append( split_stat_line(stat_line) )
        if screen :
            print "\r\t"+stat_line+"\r",


        # a-t-on fini ? Finished est modifiée par l'algorythme
        done = it > max_iter or finished

    # sauter une ligne
    if screen :
        print
        print

    # retournons le nombre d'iteration consomés et les stats complète
    return it, np.array(stats).T


def multiple_runs(problem, algo_class_name,  max_iter, nb_runs, alg_options):
    """
    Exécute plusieurs fois un algorithme de recherche local sur un problème
    donné.

    Note : Un fichier de courbe avec les valeur des solutions courante est
           créer a la fin de l'éxécution . Il a le nom de la classe de
           l'algorithme et l'extension .png

    prend :
       problem : une instance de la classe problem
       algo_class_name : le NOM DE LA CLASSE d'un algorithme
       max_iter : entier le nombre d'itération maximum
       nb_runs : entier le nombre nombre d'exécutions

    retourne :
       Un tuple
            un tableau : avec toute les valeur des solution finale, autant que
                         nb_runs
            le nom de l'algorithme : string, pour affichage
    """


    # Pour stocker les stat de sortie
    iter_data = []   # les stats par iteration
    final_data = []  # les stats finales, la meilleurs solution

    print "Algorithm : {}".format(algo_class_name)

    for r in xrange(nb_runs) :

        # instancier un algorithme avec le problem et la solution initial
        algorithm = algo_class_name( problem, alg_options )
        problem.reset()

        # exécuter l'algorithme jusqua la fin et récupérer ses stats
        it , iter_stats = run_algorithm(algorithm, max_iter, screen=True)
        iter_data.append( iter_stats )

        # recuperons et affichons les stats de fin
        final_stat = algorithm.print_final()
        final_data.append (split_stat_line(final_stat)[2] ) # juste la valeur
        print "Run {}, iter:{} {}".format(r, it, final_stat)

        # Si le probleme s'y prete, on dessine la solution
        try :
            s = algorithm.best_solution
            problem.draw_solution(s, "{}-{}-{}.png".format(problem.name,
                                                           algorithm.name,r))
        except NotImplementedError :
            pass # la solution ne se dessine pas, alors on fait pas


    # afficher une line pour séparer les affichages.
    print "-"*80

    # Réaliser les courbes pour chaque exécution
    plot_by_evaluation(iter_data, algorithm.name+'-iter.png')

    # retourner les valeur des solution final et le nom de l'algorithme
    return np.array(final_data), algorithm.name


if __name__ == '__main__':

    # paramètre globaus, a modifier selon taille des problèmes
    #small - medium - large
    probleme_size   = 'small'

    max_evaluations = 3000 # Les critère d'arrêt
    max_iterations  = 3000

    nb_runs         = 30   # le nombre d'exécution de chaque algorithme

    # paramètre pour les algorithmes
    algo_options = {
        'mu' : 10,
        'lambda' : 20,
        'Pc' : .8,
        'Pm' : .4,
    }

    # la liste des algorithmes (le nom des classes)
    algo_list = [
        RandomLS,
        HillClimbingLS,
        FirstImprovementHillClimbingLS
    ]

    # Générer un problème
    prob = generate_knapsac_instance( probleme_size, max_evaluations)
    #prob = generate_set_covering_instance( probleme_size, max_evaluations)
    #prob = generate_tsp_instance( probleme_size, max_evaluations, size=20)

    #prob = generate_onemax_instance( probleme_size, max_evaluations)
    #prob = generate_leading_ones_instance( probleme_size, max_evaluations)
    #prob = generate_binval_instance( probleme_size, max_evaluations)

    # pour stocker les stats
    algo_stats = []
    algo_names = []

    # exécute tous les algorithme
    for algo_class in  algo_list :
        stats, name = multiple_runs(prob,
                                    algo_class,
                                    max_iterations,
                                    nb_runs,
                                    algo_options)
        algo_stats.append( stats )
        algo_names.append( name )

    # Dessine les boites a moustaches avec tous les algorithmes
    plot_by_final_solution(algo_stats, algo_names, 'boxplots.png' )
