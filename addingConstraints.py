## Importing required libraries
import os as os
import pandas as pd
from itertools import product
import numpy as np
import scipy.stats as ss
from scipy.stats import chi2_contingency
from scipy.stats import skew
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
import statistics
from IPython.display import display

def main():
    fr = open("addingConstraints.txt", "r")
    skips = []
    for x in fr:
        if "% @hard(" in x:
            fhard = open("draco/asp/hard.lp", "r")
            for y in fhard:
                if x.strip() == y.strip():
                    skips.append(x.strip())
            fhard.close()
        if "% @soft(" in x:
            fsoft = open("draco/asp/soft.lp", "r")
            for y in fsoft:
                if x.strip() == y.strip():
                    skips.append(x.strip())
            fsoft.close()
    fr.close()
    
    
    fr = open("addingConstraints.txt", "r")
    fhard = open("draco/asp/hard.lp", "a")
    fsoft = open("draco/asp/soft.lp", "a")
    fweights = open("draco/asp/weights.lp", "a")
    kind = "None"
    copy = True
    skip = False
    for x in fr:  # Loop through each line
        if kind == "None":
            if "### Hard ###" in x:
                kind = "Hard"
                copy = True
                skip = False
        elif kind == "Hard":            
            if "### Soft ###" in x:
                kind = "Soft"
                copy = True
                skip = False
            else:
                if len(x.strip()) > 0:
                    copy = True
                    if x.strip() in skips:
                        skip = True
                if copy and not skip:
                    fhard.write(x)
                if len(x.strip()) == 0:
                    copy = False
                    skip = False
        elif kind == "Soft":
            if len(x.strip()) > 0:
                copy = True
                if x.strip() in skips:
                    skip = True
            if copy and not skip:
                fsoft.write(x)
                if "preference(" in x:
                    #print(x.strip())
                    name = x.strip()
                    name = name[11:-4]
                    fweights.write("#const " + name + " = 1.")
            if len(x.strip()) == 0:
                copy = False
                skip = False
            
    fr.close()
    fhard.close()
    fsoft.close()
            
            
            
                 # Need to check if the line starts with "% @hard" or "% @soft" for which to add to, then add all lines to the appropriate file until x is empty
                 # If soft, also need to add dummy weight to weights.lp
        

if __name__ == "__main__":
    main()
