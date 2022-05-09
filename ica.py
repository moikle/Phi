# This file provides Sk-learn functionality for reducing the feature dimensionality of multi-dimsional time series data as a pre-processing step in calculating Tononi Phi.
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import sys
import csv
from sklearn import decomposition
import phi_params_27Apr22 as conf

from sklearn.decomposition import FastICA, PCA, fastica
from numpy import genfromtxt

# The compute_ica function reads in a file name. The input file should be a csv or tsv array-like file of shape (n_samples, n_features).compute_ica outputs a pair [S_, num_of_nodes] in which S_ is the best fit ICA transform and num_of_nodes is the number of nodes leading to the smallest sum of sqaure residuals (ssr). The number of nodes is currently hard-coded as being in the range [3, max_nodes].
def compute_ica(file):
    S = genfromtxt(file, delimiter = conf.delim)
    S = S[starting_value: starting_value + int_len -1]
    ica = None
    ssr = np.zeros(max_nodes + 1)
    # Determine number of nodes that minimizes sum of the squares of the errors
    for loc in range (max_nodes + 1):
        dim = loc+3
#        ica = decomposition.FastICA(n_components = dim, max_iter = 1000, tol = 1e-02)
#        S_ = ica.fit_transform(S)
#        A_ = ica.mixing_.T
        #np.allclosei(X, np.dot(S_, A_) + ica.mean_)
        [K, W, S_] = fastica(S, n_components = dim, max_iter = 1000, tol = 1e-02)
        w = np.dot(W.T, K)
        #A = w.T*(w*w.T).I
        wwt = np.dot(w, w.T)
        #print(wwt.shape)
        A = np.dot(w.T, np.linalg.inv(wwt))
        X = np.matmul(A, S_.T)
        ssr[loc] = ((X-S.T) ** 2).sum()
        #        f.write("dimension = " + str(dim) + " and ssr = " + str(ssr[loc]) + "\n")
        #    mn = np.min(ssr)
    print(ssr)
    num_of_nodes = np.argmin(ssr) + 3
    #f.write("minimum is " + str(mn) + " at dim = " + str(ind+3))
    #f.close()
    ica = decomposition.FastICA(n_components = num_of_nodes, max_iter = 1000, tol = 1e-02)
    S_ = ica.fit_transform(S)
    return([S_, num_of_nodes])


