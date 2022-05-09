from binner import *
from build_hash import *
import csv
from cal_p_current import * #its called cow pee because it was cal p for calculate probability and

#from get_all_graphs import *
from tuple_time_series import *
#import phi_params as conf
from scipy.stats import wasserstein_distance
import matplotlib.pyplot as plt
import numpy as np
from QueyranneUtils import *

def run_phi():
    #Get the data and bin it into the time series
    raw_time_series = load_data(conf.file_path, conf.no_of_cols_to_skip)
    time_series = binner(raw_time_series, conf.num_of_bins, 0, 0)
    time_series = np.array(time_series).T.tolist()
    tuple_series = tuple_time_series(time_series)

    #Calculate how many iterations are needed
    num_of_cols = len(np.array(raw_time_series).T.tolist())
    cap = num_of_cols - conf.int_len
    
    #initilize data structures
    tuple_hash = build_hash(tuple_series[:conf.int_len]) #Holds all data, build the first iteration
#    graphs = get_all_graphs() 
    phi_vals = [] #Hold phi values

    #Iterate through the sliding window and print the percent done
    for starting_value in range(0, cap ):
        print('\r', end = "")
        print("     Percent done: %2.3f" % ((float(starting_value ) * 100.00)/ (float(cap))), end =' \n')
        
        #If we need to move the wiindow, do as such
        if not starting_value == 0:
        
            #Add the next tuple
            add_index = starting_value + conf.int_len - 1 
            cur_tuple = tuple_series[ add_index ]
            prev_tuple = tuple_series[ add_index - 1 ]
            tuple_hash = add_tuple( cur_tuple, prev_tuple, add_index, tuple_hash)
#            print('tuple_hash = ', tuple_hash)
            
            #Remove the first tuple
            remove_index = starting_value - 1
            cur_tuple = tuple_series[ remove_index ]
            nex_tuple = tuple_series[ starting_value ]
            tuple_hash = remove_tuple( cur_tuple, nex_tuple, remove_index, tuple_hash)
        
        cur_X  = tuple_series[ starting_value + conf.int_len - 3]
        
        #Initilize vectors to hold D(Pe || Pe(i)) and D(Pc || Pc(i))
        e_vals = [] 
        c_vals = []
        
        e_whole = cal_p(cur_X, tuple_hash, 0)#cal Pe(Xt|Xt-1 = X) 
#        print('e_whole = ', e_whole)
        c_whole = cal_p(cur_X, tuple_hash, 1)#cal Pc(Xt-1|Xt = X) 
#        print('c_whole = ', c_whole)
        #iterate through the graphs
        
        ##QUEYRANNE'S ALGORITHM GOES HERE
        index = [i for i in range(conf.num_of_nodes)]
        e_IndexOutput = QueyranneAlgorithm(cal_p_i, index, cur_X, tuple_hash, e_whole, 0)
#        print('e_IndexOutput = ', e_IndexOutput)
        c_IndexOutput = QueyranneAlgorithm(cal_p_i, index, cur_X, tuple_hash, c_whole, 1)
#        print('c_IndexOutput = ', c_IndexOutput)
        
        e_graph = vertices2graph(e_IndexOutput, index)
#        print('e_graph =', e_graph)
        c_graph = vertices2graph(c_IndexOutput, index)
#        print('c_graph =', c_graph)
        
#        for graph in graphs:
        e_part = cal_p_i(e_graph, cur_X, tuple_hash, 0)#cal Pe(i)(Xt|Xt-1 = X) 
        c_part = cal_p_i(c_graph, cur_X, tuple_hash, 1)#cal Pc(i)(Xt-1|Xt = X)
#        print('e_part = ', e_part)
#        print('c_part = ', c_part)
        
        (e_whole_list, e_part_list, multiplier) = wasserstein_hash_2_list(e_whole, e_part)
#        print('e_whole_list = ', e_whole_list)
#        print('e_part_list = ', e_part_list)
        e_val = multiplier*wasserstein_distance(e_whole_list, e_part_list)
        
        (c_whole_list, c_part_list, multiplier) = wasserstein_hash_2_list(c_whole, c_part)
#        print('c_whole_list = ', c_whole_list)
#        print('c_part_list = ', c_part_list)
        c_val = multiplier*wasserstein_distance(c_whole_list, c_part_list)
        
            #Append the values to the lists
        e_vals.append(e_val)
        c_vals.append(c_val)
        
        #Cal MIN(i \in I) for e and c    
        e_min = min(e_vals)
        c_min = min(c_vals)
#        print('e_min = ', e_min, '\n')
        
        #Add min( PHIe, PHIc) to phi values
        phi_vals.append(min(e_min, c_min))
#        print('phi_vals = ', phi_vals, '\n')
    return phi_vals  
    
    
phi_vals = run_phi()

phi_mean = np.mean(np.array(phi_vals))
phi_sd = np.std(np.array(phi_vals))
info_string = "Phi (STD %2.6f, MEAN: %1.3f)" % (phi_sd, phi_mean) 
#Plot the phi values      
plt.plot(phi_vals, label = info_string)
plt.legend()
plt.show(block = False)
plt.savefig("image_results/window" + str(conf.int_len) + "_noOfBins" + str(conf.num_of_bins) + ".png")
plt.clf()
