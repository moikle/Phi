import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import sys
import csv
from sklearn import decomposition

from sklearn.decomposition import FastICA, PCA, fastica
from numpy import genfromtxt

def compute_ica(file):
    S = genfromtxt(file, delimiter=',')
    ica = None
    num_of_nodes =  3
    #f.write("minimum is " + str(mn) + " at dim = " + str(ind+3))
    #f.close()
    ica = decomposition.FastICA(n_components = num_of_nodes, max_iter = 1000, tol = 1e-02)
    S_ = ica.fit_transform(S)
    return(S_)

filename = "/Users/moikle_admin/Research/SingularityNET/Noisy Smokes/smokes-pln.csv"
num_iterations = 1000
S_ = np.zeros((895, 3))
for i in range(num_iterations):
    Snew_ = compute_ica(filename)
    S_ = np.add(S_, Snew_)
S_ = np.true_divide(S_, num_iterations)
with open('/Users/moikle_admin/Research/SingularityNET/Noisy Smokes/S_.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(S_)


