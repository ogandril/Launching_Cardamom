# Launch CARDAMOM in one command line
# create a new directory for each parameter combination
# Still requires specific R script at that stage 

import os
import numpy as np
import matplotlib.pyplot as plt
from harissa.utils import build_pos, plot_network

# Hyperparameters
D=3449 # project name
P=3 # Experiment within project
SFT=15 # time scale factor
CC=12 # cell cycle time:
T=2 #threshold for interactions 

cwd = os.getcwd()

Infer=1# to infer the GRN
Simulate=1 # to simulate the GRN
Visualize=1 # to visualize some output
Kanto=1 # to compute Kantorovich distances
Draw=1 #to draw the GRN

# Create a working directory
os.system("mkdir "+str(cwd)+"/OG"+str(D))
os.chdir(str(cwd)+"/OG"+str(D))

# Copy needed files
os.system("cp  "+str(cwd)+"/cardamom/infer_network.py infer_network.py")
os.system("cp  "+str(cwd)+"/cardamom/simulate_data.py simulate_data.py")
os.system("cp  "+str(cwd)+"/cardamom/visualize_data.py visualize_data.py")
os.system("cp  "+str(cwd)+"/cardamom/Kanto_2D.py Kanto_2D.py")
os.system("cp  "+str(cwd)+"/cardamom/Draw_GRN.py Draw_GRN.py")
os.system("mkdir " +str(P))
os.chdir(str(P))
os.system("mkdir Data")
os.system("mkdir Results")
os.system("mkdir Rates")
os.system("mkdir cardamom")

# Launch R script to generate entry files
os.system("Rscript --vanilla  "+str(cwd)+"/res_carda/OG3449_3.R "+str(SFT)+" "+str(CC)+" "+str(P)+" "+str(D))

# Infer GRN
os.chdir(str(cwd)+"/OG"+str(D))
if Infer:
	os.system( "python infer_network.py -i " +str(P))

#In order to provide a more comprehensive representation of the network's dynamics, amplify the scaling factor applied to the network's edges.
os.chdir(str(cwd)+"/OG"+str(D)+"/"+str(P)+"/cardamom")
fi=np.load('inter.npy')
fi=fi*10
# Cut off low intensity edges
fi[abs(fi) < T] = 0
# Save the resulting matrix
np.save('inter.npy', fi)
np.savetxt("inter_matrix.csv", fi, delimiter=",")

# Simulate
os.chdir(str(cwd)+"/OG"+str(D))
if Simulate:
	os.system( "python simulate_data.py -i " +str(P))

# Visualize
if Visualize:
	os.system( "python visualize_data.py -i " +str(P))

# Compute Kanto distances
if Kanto:
	os.system("python Kanto_2D.py " +str(D)+" "+ str(P)+" "+str(cwd))

# Draw the GRN
if Draw:
	p="python Draw_GRN.py " +str(D)+" "+ str(P)+" "+ str(T) +" " + str(cwd)
	os.system("python Draw_GRN.py " +str(D)+" "+ str(P)+" "+ str(T)+" " + str(cwd))

# Write parameter values
os.chdir(str(cwd)+"/OG"+str(D)+"/"+str(P)+"/Results")
text = ['time scale factor: '+(str(SFT)), "cell cycle time: " + str(CC)]
with open('parameters', 'w') as f:
	for line in text:
        	f.write(line)
        	f.write('\n')


print('My work here is done')

