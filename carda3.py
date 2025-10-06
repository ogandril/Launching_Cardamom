# Launch CARDAMOM in one command line
# create a new directory for each parameter combination
# Still requires specific R script at that stage 
# Start from /pbs/home/o/ogandril/CardaSC

import os
import numpy as np
import matplotlib.pyplot as plt

##################
# Hyperparameters
# Pathways and files
cwd = os.getcwd()

D=3604 # project name
P=1 #Experiment within project
seq="3598_3" # R script to be launched
# Time sensitive parameters
SFT=4 # time scale factor
CC=20 # cell cycle time:
f=10 # Stabilizing factor for mRNA (slow down the model)

# Which function should be executed
transform=1 # old to new
Infer=1# to infer the GRN
simulate=1# to infer the GRN
perturb=1# to infer the GRN

# Create a working directory
os.system(f"mkdir {cwd}/OG{D}")
path_1 = (f"{cwd}/OG{D}")

# Copy carda3.py
os.system("cp  carda3.py "+path_1)

# Create a working subdirectory
os.chdir(path_1)
os.system(f"mkdir {P}")
os.chdir(f"{P}")

# Create cardamom folders
os.system("mkdir Data")
os.system("mkdir Results")
os.system("mkdir Rates")
os.system("mkdir cardamom")

# Launch R script to generate entry files
os.system(f"Rscript --vanilla  {cwd}/res_carda/{seq}.R {SFT} {CC} {P} {D} {f}")

# Move to the Cardasc repository 
path_2 = f"{cwd}/CardaSC/utils/old_to_new"
os.chdir(path_2)

if transform:
	os.system(f"python convert_old_data_to_ad.py -i {cwd}/OG{D}/{P}")
	os.system(f"python add_degradations_to_ad.py -i {cwd}/OG{D}/{P}")

# Infer GRN
path_3 = f"{cwd}/CardaSC"
os.chdir(path_3)

if Infer:
	echo "infer_mixture"
	os.system(f"python infer_mixture.py -i {cwd}/OG{D}/{P} -s full")
	echo "infer_network"
	os.system(f"python infer_network.py -i {cwd}/OG{D}/{P} -s full")
	echo "adapt_to_unitary"
	os.system(f"python adapt_to_unitary.py -i {cwd}/OG{D}/{P} -s full")

if simulate:	
	echo "simulate_network"
	os.system(f"python simulate_network.py -i {cwd}/OG{D}/{P} -s full")
	echo "check_sim_to_data"
	os.system(f"python check_sim_to_data.py -i {cwd}/OG{D}/{P} -s full")

if perturb:
	echo "Simulate KOV"
	os.system(f"python simulate_network_KOV.py -i {cwd}/OG{D}/{P} -s full -k "('HMGB1',),('TCF4',),)" -o "('HMGB1',),('TCF4',),)"")

	python simulate_network_KOV.py -i "${file}" 
	echo "Check KOV"
	python check_KOV_to_sim.py -i "${file}" -k "('HMGB1',),('TCF4',),)" -o "('HMGB1',),('TCF4',),)"	

print('My work here is done')

