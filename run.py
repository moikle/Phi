import os
import numpy as np
import pickle
import matplotlib.pyplot as plt
import phi_params_27Apr22.py as conf

num_iterations = 100
phi_series = [[] for _ in range(num_iterations)]
phi_mean = np.zeros(num_iterations)
phi_sd = np.zeros(num_iterations)
for i in range(num_iterations):
    os.system("python ica2.py")
    f = open("/Users/moikle_admin/Research/SingularityNET/Python/Phi Pipeline/phi_params.py" , "a")
    f.write("file_path = '/Users/moikle_admin/Research/SingularityNET/Phi+Reputation/equilDefault9conserv1/S_")
    #        f.write(str(num_iterations))
    f.write(".csv' \n")
    f.close
    os.system("python main.py")
    with open("/Users/moikle_admin/Research/SingularityNET/Python/Phi Pipeline/phi_vals.py", "rb") as f:
        phi_vals = pickle.load(f)
    with open("/Users/moikle_admin/Research/SingularityNET/Python/Phi Pipeline/num_of_nodes.py", "rb") as f:
        num_of_nodes = pickle.load(f)
    phi_series[i] = phi_vals
    phi_mean[i] = np.mean(np.array(phi_vals))
    phi_sd[i] = np.std(np.array(phi_vals))
    info_string = "Phi (STD %2.6f, MEAN: %1.3f)" % (phi_sd[i], phi_mean[i])
    plt.plot(phi_series[i], label = info_string)
    plt.legend()
    plt.show(block = False)
    plt.savefig("image_results9-1-20b/window" + str(conf.int_len) + "_noOfBins" + str(conf.num_of_bins) + "_noOfNodes" + str(num_of_nodes) + "iteration" + str(i) + ".png")
    plt.clf()
phi_mean_mean = np.mean(np.array(phi_mean))
print("phi_mean_mean = ", phi_mean_mean)
phi_mean_sd = np.sqrt(sum(i*i for i in phi_sd))
print("phi_mean_sd = ", phi_mean_sd)
info_string = "Phi (STD %2.6f, MEAN: %1.3f)" % (phi_mean_sd, phi_mean_mean)
#Plot the phi values
#phi = ([0] * 180 for i in range(num_iterations))
#for i in range(num_iterations):
#    phi[i] = phi_series[i]
#phi = np.array(phi_series[i] for i in range(num_iterations))
#print(phi)
phi_avg = np.average(phi_series, axis = 0)
plt.plot(phi_avg, label = info_string)
plt.legend()
plt.show(block = False)
plt.savefig("image_summary9-1-100/window" + str(conf.int_len) + "_noOfBins" + str(conf.num_of_bins) + "summary.png")
plt.clf()
