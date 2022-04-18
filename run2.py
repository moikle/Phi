import os
import numpy as np
import pickle
import matplotlib.pyplot as plt
import phi_params as conf

#os.system("python ica2.py")
#f = open("/Users/moikle_admin/Research/SingularityNET/Python/Phi Pipeline/phi_params.py" , "a")
#f.write("file_path = '/Users/moikle_admin/Research/SingularityNET/Phi+Reputation/equilDefault9conserv1/S_")
#f.write(".csv' \n")
#f.close
#os.system("python main.py")
with open("/Users/moikle_admin/Research/SingularityNET/Python/Phi Pipeline/phi_vals.py", "rb") as f:
    phi_vals = pickle.load(f)
with open("/Users/moikle_admin/Research/SingularityNET/Python/Phi Pipeline/num_of_nodes.py", "rb") as f:
    num_of_nodes = pickle.load(f)
    phi_mean = np.mean(np.array(phi_vals))
    phi_sd = np.std(np.array(phi_vals))
info_string = "Phi (STD %2.6f, MEAN: %1.3f)" % (phi_sd, phi_mean)
plt.plot(phi_vals, label = info_string)
plt.legend()
plt.show(block = False)
plt.savefig("noisy_smokes/window" + str(conf.int_len) + "_noOfBins" + str(conf.num_of_bins) + "_noOfNodes" + str(num_of_nodes) + ".png")
plt.clf()


