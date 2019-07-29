#!/usr/bin/env python3

## This scripts computes the number of challenges offline / onlines using the
## conditions and formulas imposed by the theorem 4, i.e. the ZigZag theorem.
## It includes a "hypothetic" calculator for tapering ZigZag as well. Hypothetic
## since we don't have the analysis yet.
## The acutal numbers plugged in are from the parameters written down in the
## google doc named "PoRep Parameters & VC"

import numpy as np

## class zigzag, without tapering
class ZZParams:
    def __init__(self,lambd, delta,epsilon):
        self.lambd = lambd
        self.delta = delta
        self.eps = epsilon
        self.check()

    def levels(self):
        return 2.0 * np.log2(1/(3 * (self.eps - 3.0*self.delta))) + 18

    def offline_level(self,lvl = 0):
        if lvl == 0:
            return self.lambd / self.delta 
            
    def offline_total(self):
        return self.levels() * self.offline_level()

    def online(self):
        return 2 * self.lambd / self.eps

    def check(self):
        if self.delta > np.minimum(0.01,self.eps/3):
            raise Exception("delta value too high")

        if self.eps + 2 * self.delta > 0.24:
            raise Exception("epsilon + 2delta > 0.24")

## ZigZag graph with tapering
class ZZTapering(ZZParams):
    def check(self):
        if self.delta > np.minimum(0.01,self.eps/2):
            raise Exception("delta value too high")

        if self.eps >= 0.24:
            raise Exception("epsilon superior to 0.24")
        
        if self.eps + self.delta > 0.24:
            raise Exception("eps + delta > 0.24")

    def offline_total(self):
        delta = self.delta
        acc = self.lambd / delta
        mini = 0.05
        for i in range(int(self.levels()-1)):
            if i % 2 == 0:
                delta = np.maximum(mini,2/3 * delta)
            acc += self.lambd / delta
        return acc



def regularZZ():
    lambd = 8
    delta = 0.009
    epsilon = 0.07
    p1 = ZZParams(lambd,delta,epsilon)
    print("regular ZZ:")
    print("\tnumber of levels %d" % p1.levels())
    print("\toffline total %d" % p1.offline_total())

def taperingZZ():
    eps = 0.01
    delta = 0.003
    lambd = 8
    p1 = ZZTapering(lambd,delta,eps)
    print("Tapering ZZ:")
    print("\tnumber of levels %d" % p1.levels())
    print("\toffline total %d" % p1.offline_total())

regularZZ()
taperingZZ()
