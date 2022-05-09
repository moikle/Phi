from binner import *
from build_hash import *
import csv
#likeABoss
from cal_p_current import * #its called cow pee because it was cal p for calculate probability and 
#cal p sounds like cow pee and cow pee is alot cooler and we really cant miss that opertunity.
#from get_all_graphs import *
from tuple_time_series import *
#import phi_params as conf
from scipy.stats import wasserstein_distance
import matplotlib.pyplot as plt
import numpy as np

# Function that takes two lists as inputs and returns a list of the set union of the two lists
def Union(lst1, lst2):
    if (type(lst1) == list and type(lst2) == list):
        final_lst = list(set(lst1)|set(lst2))
    elif type(lst1) == list:
        final_lst = list(set(lst1)|set([lst2]))
    elif type(lst2) == list:
        final_lst = list(set([lst1])|set(lst2))
    else:
        final_lst = list(set([lst1])|set([lst2]))
    return final_lst 

# Function that takes two lists as inputs and returns a list of the set difference A-B of the two lists
def indexdiff(A, B):
    if len(A) == 0:
        mx = 1 + np.amax(B)
    elif len(B) == 0:
        mx = 1 + np.amax(A)
    else:    
        mx = 1 + max(np.amax(A), np.amax(B))  
    vals = np.zeros(mx)
    for index in A:
        vals[index] = 1
    for index in B:
        vals[index] = 0
    C = np.where(vals == 1)
    return C

# The function vertices2graph takes as inputs a list of vertice and an index list and returns a
# graph bipartition in the correct format for use in calculsting the resulting Phi probability distributions
#
# The output format is of the form given by this example for an effect repetoire: 
# graph = [[(0,1),(1,2)],[(2,),(0,)]] means nodes 0 and 1 affect nodes 1 and 2, while node 2 affect node 0. Cause
# repetoire follows mutatis mutandis.
# The cause-effect repetoires for time-series data follow the system model and decomposition for IIT as described
# in Stephan Krohn and Dirk Ostwald, "Computing Integrated Information," Neuroscience of Consciousness, 
# Volume 2017, Issue 1, 1 January 2017, nix017, https://doi.org/10.1093/nc/nix017

def vertices2graph(vertices, index):
#    print('vertices = ', vertices, '\n')
    graph1 = [[], []]
    graph1[0] = []
    graph1[1] = []
    graph2 = [[], []]
    graph2[0] = []
    graph2[1] = []   
    for vertex in vertices:
#        print('vertex = ', vertex, '\n')
        if vertex < conf.num_of_nodes/2:
            graph1[0].append(vertex)
        else:
            graph1[1].append(vertex)
    graph2[0] = indexdiff(np.arange(len(index)), graph1[0])
    graph2[1] = indexdiff(np.arange(len(index)), graph1[1])
    graph = [[], []]
    graph[0] = graph1
    graph[1] = [graph2[0][0].tolist(), graph2[1][0].tolist()]
    return graph

# The function QueyranneAlgorithm implments Queyranne's algorithm for approximating the Minimum Information
# Partition (MIP). According to Jun Kitazono, Ryota Kanai, Masafumi Oizumi, "Efficient Algorithms for 
# Searching the Minimum Information Partition in Integrated Information Theory," Entropy 2018, 20(3), 173; 
# https://doi.org/10.3390/e20030173, Queyranne's Algorithm finds an approximation to the MIP, at least for
# Phi *. We use Phi 3.0 in place of Phi *, but initial experiments look promising. The code for implementing
# Queyranne's Algorithm follows the implementation from the Araya group's Practical Phi Toolbox 
# (https://figshare.com/articles/phi_toolbox_zip/3203326/10), though all probability distribution arrays have 
# been replaced with hash-tables for efficiency.
def QueyranneAlgorithm(F, index, cur_X, tuple_hash, dist_whole, args):
    if not(isinstance(index[0], list)):
#        index = np.array(index)
#        print(index)
        index = [[x] for x in index]
    indexlen = len(index)
    M = [(np.size(a)) for a in index]
    M = np.sum(M)
    indexrec = [[] for i in range(indexlen-1)]
    f = np.zeros(indexlen-2)
    for i in range(0,indexlen-2):
        pp = pendent_pair(F, index, [0], cur_X, tuple_hash, args)
        last = pp[-1]
        indexrec[i] = index[last]
        index = [index[x] for x in pp]
        graph = vertices2graph(indexrec[i], index)
#        print('Qgraph = ', graph)
        dist_part = F(graph, cur_X, tuple_hash, args)
#        print(i)
        (dist_whole_list, dist_part_list, multiplier) = wasserstein_hash_2_list(dist_whole, dist_part)
#        print('dist_whole_list = ', dist_whole_list)
#        print('dist_part_list = ', dist_part_list)
        f[i] = multiplier*wasserstein_distance(dist_part_list, dist_whole_list)
#        print('i = ', i, 'and f[i] = ', f[i])
        index[-2] = Union(index[-2], index[-1])
        index.pop()
    min_f = np.min(f)
    argmin_f = np.argmin(f)
#    print('f = ', f)
#    print('indexrec =', indexrec)
#    print('argmin_f = ', argmin_f)
    if len(indexrec[argmin_f]) > M/2:
        if isinstance(index[0], list):
            index = index[0]
        IndexOutput = indexdiff(index, indexrec[argmin_f])
        IndexOutput = IndexOutput[0]
#        print('IndexOutput in Q = ', IndexOutput, '\n')
    else:
        IndexOutput = np.sort(indexrec[argmin_f])
    return IndexOutput

# This function is the core function of the QueyranneAlgorithm
def pendent_pair(F, index, ind, cur_X, tuple_hash, args):
    ind_ind = [index[k] for k in ind]
#    print('ind_ind = ', ind_ind, '\n')
#    print('index = ', index, '\n')
#    orig_index = index
#    index = [[x] for x in index]
    for i in range(len(index) - 1):
#        index_set = set(index)
#        ind_set = set(ind)
#        indc = index_set.difference(ind_set)
        indc = indexdiff(np.arange(len(index)), ind)
        indc = indc[0]
#        print('indc = ', indc, '\n')
        candidates = [index[i] for i in indc]
#        reduced_candidates = [x for [x] in candidates]
#        reduced_ind = [x for [x] in ind_ind]
        keys = np.zeros(len(candidates))
        for j in range(len(candidates)):
#            print('index = ', index, '\n')
#            print('candidates[j] = ', candidates[j], '\n')
#           reduced_ind = [x for [x] in ind_ind]
#            print('ind = ', ind, '\n')
#            vertices_plus = Union(ind, reduced_candidates[j])
            vertices_plus = Union(ind, candidates[j])
            graph_plus = vertices2graph(vertices_plus, index)
            graph = vertices2graph(candidates[j], index)
#            print('cal_pi = ', cal_p_i(graph_plus, cur_X, tuple_hash, args))
            p_i_hash_plus = cal_p_i(graph_plus, cur_X, tuple_hash, args)
            p_i_hash = cal_p_i(graph, cur_X, tuple_hash, args)
            (p_i_list_plus, p_i_list, multiplier) = wasserstein_hash_2_list(p_i_hash_plus, p_i_hash)
            keys[j] = multiplier*wasserstein_distance(p_i_list_plus, p_i_list)
        minkey = min(keys)
#        print('minkey = ', minkey, '\n')
        minkey_ind = np.argmin(keys)
#        print('minkey_ind = ', minkey_ind, '\n')
#        print('ind = ', ind, '\n')
#        print('indc[minkey_ind] =', indc[minkey_ind], '\n')
        ind.append(indc[minkey_ind])
#        print('ind =', ind, '\n')
    return ind

# This function processes the hash-table outputs from cal_p and cal_pi core IIT functions and outputs two
# lists of reduced size (compared to full probability distributions) along with a multiplier to compensate
# for the reduction in list size. The two lists can then be inputs into the scipy stats.py wasserstein_distance
# function. In order to obtain the correct Wassrestein distance, the output from the wasserstein_distance simply
# needs to be multiplied by the multiplier
def wasserstein_hash_2_list(hash1, hash2):
    hash1_keys = list(hash1.keys())
    hash2_keys = list(hash2.keys())
    total_keys = Union(hash1_keys, hash2_keys)
    min_key = np.min(total_keys)
    max_key = np.max(total_keys)
    
    for key in total_keys:
        if key not in hash1.keys():
            hash1[key] = 0
        if key not in hash2.keys():
            hash2[key] = 0

    hash1_list = list(hash1.values())
#    print('hash1_list = ', hash1_list)
    hash2_list = list(hash2.values())
#    print('hash2_list = ', hash2_list)
    multiplier = len(hash1_list)/(max_key-min_key+1)
    return (hash1_list, hash2_list, multiplier)
