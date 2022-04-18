import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import sys
import csv
from datetime import datetime, timedelta
from itertools import islice

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

def str2ms(s):
    hr, mm, sec, ms = map(float, s.split(':'))
    inMs = ((hr * 60 + mm) * 60 + sec) * 1000 + ms
    return int(inMs)

nlines = 2000

with open('Sophia/MeditationSession004.csv', 'r') as csvfile:
    csvReader = csv.reader(csvfile)
    csvReader.__next__()
    csvReader.__next__()
    header = csvReader.__next__()
    AtomIndex = header.index("Atom(uuid)")
    t1Index = header.index(" t1(H:m:s:ms)")
    t2Index = header.index(" t2(H:m:s:ms)")
    sti1Index = header.index(" STI_1")
    sti2Index = header.index(" STI_2")
    durationIndex = header.index(" duration")
    times = []
    atoms = []
#    for row in csvReader:
    for row in islice(csvReader, nlines):
        t1_raw = row[t1Index]
        t2_raw = row[t2Index]
        atom = row[AtomIndex]
        times = Union(times, [t1_raw, t2_raw]) 
        atoms = Union(atoms, [atom])
    del times[0]
    time_ms = []
    for time in times:
        time = str2ms(time)
        time_ms.append(time)
    time_ms = np.sort(time_ms)
            

output = np.zeros((len(atoms), len(time_ms)))               
with open('Sophia/MeditationSession004.csv', 'r') as csvfile:
    csvReader = csv.reader(csvfile)
    csvReader.__next__()
    csvReader.__next__()
    csvReader.__next__()
#    for row in csvReader:
    for row in islice(csvReader, nlines):
#        print('row = ', row)
        for i in range(len(atoms)):
            atom = atoms[i]
#            print('atom = ', atom)
            for j in range(len(time_ms)):
                time = time_ms[j]
#                print('j = ', j)
                t1 = str2ms(row[t1Index])
                t2 = str2ms(row[t2Index])
                if ((t1 <= time <= t2) and (row[AtomIndex] == atom)):
                    if (t2 - t1) == 0:
                        output[i][j] = row[sti1Index]
                    else:
                        output[i][j] = float(row[sti1Index]) + (time - t1)/(t2 -t1) * (float(row[sti2Index]) - float(row[sti1Index]))
#                else:
#                    print("no")

with open('output_2000.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(output)
