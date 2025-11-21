# Launch CARDAMOM.V2 in one command line
# create a new directory for each parameter combination
# Still requires specific R script at that stage 
# Start from /pbs/home/o/ogandril/

import os
import numpy as np
import matplotlib.pyplot as plt
import sys

##################
# Hyperparameters
# Pathways and files
cwd = os.getcwd()

D=3624 # project name
P=3 #Experiment within project
seq="3622_1" # R script to be launched
# Time sensitive parameters
SFT=10 # time scale factor
CC=20 # cell cycle time:
f=10 # Stabilizing factor for mRNA (slows down the model)
Th_int=1.6 #threshold for interactions 

# Which function should be executed
transform=0 # old to new
Pre_comp=1 # If a precomputed anndata is available
Infer=1# to infer the GRN
simulate=1# to simulate the GRN
perturb=1# to perturb the GRN (KO/OV)

# Create a working directory
path_1 = os.path.join(cwd, f"OG{D}")
os.makedirs(path_1, exist_ok=True)  # Using os.makedirs is safer than os.system

# Create a working subdirectory
path_2 = os.path.join(path_1, str(P))
os.makedirs(path_2, exist_ok=True)

# Define path and create folders
path_4 = os.path.join(cwd, 'CardaSC')
path_3 = os.path.join(path_4, 'utils/old_to_new')
path_5 = os.path.join(path_2, 'cardamom')
os.makedirs(path_5, exist_ok=True)  # Using os.makedirs is safer than os.system
path_6 = os.path.join(path_2, 'Data')
os.makedirs(path_6, exist_ok=True)  # Using os.makedirs is safer than os.system

# Copy various files in the new folder
# carda3; this file containing hyperparameters
os.system("cp  Launching_Cardamom/carda3.py "+path_2)
# The R script that was used for building the matrix
os.system(f"cp  res_carda/{seq}.R "+path_2)
# The CARDAMOM basic parameters
os.system(f"cp  CardaSC/cardamom_beta/model/base.py "+path_2)

if transform:
	os.chdir(path_3)
	os.system("echo 'old_to_new'")
	os.system(f"python convert_old_data_to_ad.py -i {cwd}/OG{D}/{P}")
	os.system(f"python add_degradations_to_ad.py -i {cwd}/OG{D}/{P}")
	# Launch R script to generate entry files
	os.system(f"Rscript --vanilla  {cwd}/res_carda/{seq}.R {SFT} {CC} {P} {D} {f}")

if Pre_comp:
	os.system(f"cp  {cwd}/res_carda/data.h5ad "+path_6)

if Infer:
	os.chdir(path_4)
	os.system("echo 'Select DE genes and split cells'")
	os.system(f"python select_DEgenes_and_split.py -i {cwd}/OG{D}/{P} -s full -c 0 -r 0.6")
	os.system("echo 'Get kinetic rates'")
	os.system(f"python get_kinetic_rates.py -i {cwd}/OG{D}/{P} -s full")
	os.system("echo 'infer_mixture'")
	os.system(f"python infer_mixture.py -i {cwd}/OG{D}/{P} -s full")
	os.system("echo 'Infer network structure'")
	os.system(f"python infer_network_structure.py -i {cwd}/OG{D}/{P} -s full")
	os.system("echo 'Infer network to simulate'")
	os.system(f"python infer_network_simul.py -i {cwd}/OG{D}/{P} -s full")

# Save a csv version of the interaction matrix after applying a threshold
os.chdir(path_5)
inter = np.load('inter.npy')
inter_t = np.load('inter_t.npy')
# Cut off low intensity edges
inter[abs(inter) < Th_int] = 0
inter_t[abs(inter_t) < Th_int] = 0
# Save the resulting matrix
np.save('inter.npy', inter)
np.save('inter_t.npy', inter_t)

# Save as .csv for R
inter2D=inter[:, :, 0]
np.savetxt('inter.csv', inter2D, delimiter=",")

# Same for time-dependent matrix
for i in range(0, inter_t.shape[0]): 
	inter2D_t=inter_t[i, :, :, 0]
	np.savetxt("inter_"+str(i)+".csv", inter2D_t, delimiter=",")

if simulate:	
	os.chdir(path_4)
	os.system("echo 'simulate_network'")
	os.system(f"python simulate_network.py -i {cwd}/OG{D}/{P} -s full")
	os.system("echo 'check_sim_to_data'")
	os.system(f"python check_sim_to_data.py -i {cwd}/OG{D}/{P} -s full")

if perturb:
	# Write the genes to perturb.
	os.chdir(path_6)
	fichier = open('list_KO.txt', 'w')
	for arg in sys.argv[1:]:
		fichier.write(str(arg+"\n"))
	fichier.close()
	fichier = open('list_OV.txt', 'w')
	for arg in sys.argv[1:]:
		fichier.write(str(arg+"\n"))
	fichier.close()
	# Excecute the perturbation
	os.chdir(path_4)
	os.system("echo 'simulate_network_KOV'")
	os.system(f"python simulate_network_KOV.py -i {cwd}/OG{D}/{P} -s full")
	os.system("echo 'check_KOV_to_sim'")
	os.system(f"python check_KOV_to_sim.py -i {cwd}/OG{D}/{P}")

print('My work here is done')

