#!/usr/bin/env python3

## This script computes the degree using Chung's construction
import math
import warnings
## needed to suppress warning when computing chung's degree with non reasonable
## parameters - needed during table_chung
warnings.filterwarnings("ignore")
import numpy as np
import sys

##
def table_chung(target_degree):
    deg = target_degree
    alphas = [0.01]
    alphas = alphas + list(np.arange(0.1,0.81,0.05))
    betas = np.arange(0.01,1,0.01)
    table = []
    for alpha in alphas:
        for beta in betas:
            try:
                d = chung_degree(alpha,beta)
                # print("alpha %f, beta %f degree %d (target %d), table length %d" % (alpha,beta,d,deg,len(table)))
                if math.isnan(d) or int(d) != deg:
                    continue
                
                # print("\talpha %f, beta %f degree %d (target %d), table length %d" % (alpha,beta,d,deg,len(table)))
                
                table += [[alpha,beta]]
                # print("\talpha %f, beta %f degree %d, table length %d" % (alpha,beta,d,len(table)))
            except Exception as e:
                print("aie: " + str(e))
                continue

    return table


## Compute the binary entropy function 
def bin_entropy(x):
    ##
    return -x * np.log2(x) - (1 - x) * np.log2(1-x)

## Compute chung's degree inequality
def chung_degree(alpha,beta):
    hb = bin_entropy
    
    return (hb(alpha) + hb(beta)) /  (hb(alpha) - beta * hb(alpha / beta))

def print_degrees():
    alphas = [0.5,0.5,1/3,1/4]
    betas = [0.8,0.7,2/3,2/4]
    ## for DRG alpha 0.8, 
    if len(alphas) != len(betas):
        print("invalid parameter arrays")
        sys.exit(1)

    for i in range(0,len(alphas)):
        alpha = alphas[i]
        beta = betas[i]
        degree = chung_degree(alpha,beta) + 1 # because >=
        print("alpha %f - beta %f - degree d >= %d" % (alpha,beta,degree))

def print_table():
    target_degree = 8
    table = table_chung(target_degree)
    print("chung's table has length %d" % len(table))
    for pair in table:
        print("degree %d, alpha %f, beta %f, exp. factor %f" %
                (target_degree,pair[0],pair[1],pair[1]/pair[0]))

print_table()
