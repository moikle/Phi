# Phi

# Overview

Takes as input a time series of values (importance or excitation values
for example) and returns a time series of estimated Tononi Phi values

# What is Tononi Phi?

Created by University of Wisconsin psychiatrist and neuroscientist Giulio Tononi in
2004, Integrated Information Theory (IIT) is an evolving system and calculus for
studying and quantifying consciousness. Its centerpiece is Phi, Tononi’s
mathematical quantifier [1, 2].

# How we calculate Phi

In calculating Tononi Phi values, three major issues arise

    1)  There are at least 420 choices one can make in calculating the measure [3];
    
    2)  Determination of the “Minimum Information Partition” (MIP) of the causal graph structure grows super-exponentially with the number of nodes;
    
    3)  and the size of the probability distribution vectors required to determine Phi also increases super-exponentially with the number of nodes. 
    
We have chosen to implement Phi 3.0 [4] employing Queyranne’s Algorithm [5] to
obtain a good approximation of the MIP. More specifically, we used the method of
Krohn and Ostwald [6] as it applies to time series.  We stored the (often sparse)
probability distributions using Python dictionaries instead of arrays.

Since even Queyranne's algorithm grows as the cube of the number of nodes, we
include sklearn Independent Component Analysis (ICA) implementations that can be
used as a preprocessing step to reduce the feature dimensionality.

# References

[1] Tononi, G.: Consciousness as integrated information: a provisional manifesto. The Biological Bulletin 215(3), 216–242 (December 2008)

[2] Tononi, G.: An information integration theory of consciousness. BMC
Neuroscience 5(1), 42 (2004). https://doi.org/10.1186/1471-2202-5-42,
http://www.biomedcentral.com/1471-2202/5/42

[3] Kitazono, J., Oizumi, M.: Practical PHI Toolbox
(9 2018). https://doi.org/10.6084/m9.figshare.3203326.v10,
https://figshare.com/articles/phi toolbox zip/3203326

[4] Tegmark, M.: Improved measures of integrated information. PLOS Computational
Biology 12(11), 1–34 (11 2016). https://doi.org/10.1371/journal.pcbi.1005123,
https://doi.org/10.1371/journal.pcbi.1005123

[5] https://dl.acm.org/doi/pdf/10.5555/313651.313669

[6] Krohn, S., Ostwald, D.: Computing integrated information. Neuroscience
of Consciousness 2017(1), nix017 (2017). https://doi.org/10.1093/nc/nix017,
http://dx.doi.org/10.1093/nc/nix017
