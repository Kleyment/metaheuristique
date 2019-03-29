#! /usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib
matplotlib.use('agg')

from matplotlib.patches import Circle, Wedge, Polygon, Ellipse, Arc
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import *

def start_figure():
    """
    Prepare a figure object and return an axes fot its 
    
    """

    #matplotlib.rc('font',family='serif',size=8)
    #matplotlib.rcParams['ps.useafm'] = True
    #matplotlib.rcParams['pdf.use14corefonts'] = True
    #matplotlib.rcParams['text.usetex'] = True
    fig = plt.figure(num=None, figsize=(8,4.5), dpi=100)
    ax = fig.add_subplot(111)
    return ax

def finish_figure(axes, fname, xlabel, ylabel ):
  
    # handle ticks 
    axes.get_xaxis().tick_bottom()
    axes.get_yaxis().tick_left()
    axes.set_axisbelow(True)
       
    # handle labels
    axes.set_xlabel(xlabel)
    axes.set_ylabel(ylabel)
 
        
    # draw & save image
    plt.savefig(fname, bbox_inches='tight')
    plt.close(axes.get_figure())

def stat_test(x, y, ks=False):
    """
    Perform a tow sample statistical test returns a p value 
    """
    if ks:
        return ks_2samp(x,y)
    else :
        return mannwhitneyu(x,y)
    
def stars(p):
    """
    Return statistical significance marker 
    a sting of starts depending on the p-value

    """
    
    if p < 0.0001:
        return "****"
    elif (p < 0.001):
        return "***"
    elif (p < 0.01):
        return "**"
    elif (p < 0.05):
        return "*"
    else:
        return "n. s."


def draw_stars(d1, d2, ax, i, j,
               yerr=None, dh=.05, barh=.04):
    """ 
    Annotate barplot with p-values.

    :param num1: number of left bar to put bracket over
    :param num2: number of right bar to put bracket over
    :param yerr: yerrs of all bars (like plt.bar() input)
    :param dh: height offset over bar / bar + yerr in axes coordinates (0 to 1)
    :param barh: bar height in axes coordinates (0 to 1)
 

    """

    try : 
        z,p = stat_test(d1, d2)
    except ValueError: # when we feed the test all smae values 
        p = 1.0

        
        
    lx, ly = i+1+0.02, max(d1)
    rx, ry = j+1-0.02, max(d2)

    ax_y0, ax_y1 = ax.get_ylim()
    
    dh *= abs(ax_y1 - ax_y0)
    barh *= abs(ax_y1 - ax_y0)

    y = max(ly, ry) + dh

    barx = [lx, lx, rx, rx]
    bary = [y, y+barh, y+barh, y]
    mid = ((lx+rx)/2., y+barh)

    ax.plot(barx, bary, c='black')

    kwargs = dict(ha='center', va='bottom')
    
    ax.text(mid[0], mid[1], stars(p*2.0), **kwargs)   

    

    
def plot_boxplot(axes, data_stuff, labels=[]):
    """

    Plot boxplot for set of data_stuff
    where data_stuff is a list of lists of values 
    
    data_stuff = [ [ ... ] ... [ ... ] ] 
    
    """
        
    # manage padding
    y_max = max(data_stuff[0])
    y_min = min(data_stuff[0])
    for s in data_stuff :
        if y_max < max(s) : y_max = max(s)
        if y_min > min(s) : y_min = min(s)
        
    if abs(y_max-y_min) == 0:
        y_max += y_max * 1e-6 
        y_min -= y_min * 1e-6
        
    pad=abs(y_max-y_min)*0.6
    axes.set_ylim([y_min-pad, y_max+pad])
      
    bp = axes.boxplot(data_stuff, showmeans=True, labels=labels)

    # manage the colors list is given (when box order is changed)
    color_list = \
        plt.rcParams['axes.prop_cycle'].by_key()['color'][:len(data_stuff)]

    # draw the boxes 
    for i in range(0, len(bp['boxes'])) :

        # set the color 
        this_box_color = color_list[i]
        bp['boxes'][i].set_color(this_box_color)
        
        # we have two whiskers!
        bp['whiskers'][i*2].set_color(this_box_color)
        bp['whiskers'][i*2 + 1].set_color(this_box_color)
        bp['whiskers'][i*2].set_linewidth(2)
        bp['whiskers'][i*2 + 1].set_linewidth(2)
        # top and bottom fliers
        # (set allows us to set many parameters at once)

        
        #if len(bp['fliers']) > 2*i+1 : # hack for when flatbox
        #    bp['fliers'][i*2].set(markerfacecolor=params['color'],
        #                          marker='o', alpha=params['alpha'],
        #                          markersize=6,
        #                          markeredgecolor='none')
        #    bp['fliers'][i*2 + 1].set(markerfacecolor=params['color'],
        #                              marker='o', alpha=params['alpha'],
        #                              markersize=6,
        #                              markeredgecolor='none')
        
        bp['medians'][i].set_color('black')
        bp['medians'][i].set_linewidth(3)
        # and 4 caps to remove
        for c in bp['caps']:
            c.set_linewidth(1)
    
    # fill the boxes 
    for i in range(len(bp['boxes'])):
        this_box_color = color_list[i]
        box = bp['boxes'][i]
        box.set_linewidth(0)
        boxX = []
        boxY = []
        for j in range(5) :
            boxX.append(box.get_xdata()[j])
            boxY.append(box.get_ydata()[j])
            boxCoords = zip(boxX,boxY)
            boxPolygon = Polygon(boxCoords, facecolor=this_box_color,
                                 linewidth=0, alpha=0.5)
            axes.add_patch(boxPolygon)
             

    # stat test 
    dh = 0.02
    for d in xrange(1, len(data_stuff)) :
        L =  [(k,k+d) for k in xrange(len(data_stuff))]
        for ij in L:
            i,j = ij
            if j < len(data_stuff) :
                draw_stars(data_stuff[i], data_stuff[j], axes, i, j, dh=dh)
                dh += 0.02
        dh += 0.04
               

