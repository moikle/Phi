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
    ssr = np.zeros(20)
    for loc in range (20):
        dim = loc+3
        ica = decomposition.FastICA(n_components = dim, max_iter = 1000, tol = 1e-02)
        S_ = ica.fit_transform(S)
        A_ = ica.mixing_.T
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

filename = "/Users/moikle_admin/Research/SingularityNET/Phi+Reputation/equilDefault9conserv1/rankHistory_r_20_0.1_test.csv"
[S_, num_of_nodes] = compute_ica(filename)
with open('/Users/moikle_admin/Research/SingularityNET/Phi+Reputation/equilDefault9conserv1/S_.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(S_)

f = open("/Users/moikle_admin/Research/SingularityNET/Python/Phi Pipeline/phi_params.py" , "w")
f.write("int_len = 20 \n")
f.write("num_of_nodes = ")
f.write(str(num_of_nodes))
f.write("\n")
f.write("num_of_bins = 5 \n")
f.write("file_path = '/Users/moikle_admin/Research/SingularityNET/Phi+Reputation/equilDefault9conserv1/S_.csv' \n")
f.write("no_of_cols_to_skip = 0 \n")
f.close()
