# Launch CARDAMOM.V2 in one command line
# create a new directory for each parameter combination
# Still requires specific R script at that stage 
# Start from /pbs/home/o/ogandril/

import os
import numpy as np
import matplotlib.pyplot as plt

##################
# Hyperparameters
# Pathways and files
cwd = os.getcwd()

D=3614 # project name
P=1 #Experiment within project
seq="3591_1" # R script to be launched
# Time sensitive parameters
SFT=10 # time scale factor
CC=20 # cell cycle time:
f=10 # Stabilizing factor for mRNA (slows down the model)

# Which function should be executed
transform=1 # old to new
Infer=1# to infer the GRN
simulate=1# to simulate the GRN
perturb=1# to perturb the GRN (KO/OV)

# Create a working directory
os.system(f"mkdir {cwd}/OG{D}")
path_1 = (f"{cwd}/OG{D}")

# Create a working subdirectory
os.chdir(path_1)
os.system(f"mkdir {P}")
os.chdir(f"{cwd}/")

# Copy carda3.py and the R script
path_2 = (f"{cwd}/OG{D}/{P}")
os.system("cp  Launching_Cardamom/carda3.py "+path_2)
os.system(f"cp  res_carda/{seq}.R "+path_2)

# Create cardamom folders
os.chdir(path_2)
os.system("mkdir Data")
os.system("mkdir Rates")
os.system("mkdir cardamom")

# Launch R script to generate entry files
os.system(f"Rscript --vanilla  {cwd}/res_carda/{seq}.R {SFT} {CC} {P} {D} {f}")

# Move to the Cardasc repository 
path_3 = f"{cwd}/CardaSC/utils/old_to_new"
os.chdir(path_3)

if transform:
	os.system("echo 'old_to_new'")
	os.system(f"python convert_old_data_to_ad.py -i {cwd}/OG{D}/{P}")
	os.system(f"python add_degradations_to_ad.py -i {cwd}/OG{D}/{P}")

# Launch V2 scripts
path_4 = f"{cwd}/CardaSC"
os.chdir(path_4)

if Infer:
	os.system("echo 'infer_mixture'")
	os.system(f"python infer_mixture.py -i {cwd}/OG{D}/{P} -s full")
	os.system("echo 'infer_network'")
	os.system(f"python infer_network.py -i {cwd}/OG{D}/{P} -s full")
	os.system("echo 'adapt_to_unitary'")
	os.system(f"python adapt_to_unitary.py -i {cwd}/OG{D}/{P} -s full")

if simulate:	
	os.system("echo 'simulate_network'")
	os.system(f"python simulate_network.py -i {cwd}/OG{D}/{P} -s full")
	os.system("echo 'check_sim_to_data'")
	os.system(f"python check_sim_to_data.py -i {cwd}/OG{D}/{P} -s full")

if perturb:
	# Write the genes to perturb. POur le moment en dur
	path_5 = (f"{cwd}/OG{D}/{P}/Data")
	os.chdir(path_5)
	fichier = open('list_KO.txt', 'w')
	fichier.write("PCNA\n")
	fichier.close()
	fichier = open('list_OV.txt', 'w')
	fichier.write("PCNA\n")
	fichier.close()
	# Excecute the perturbation
	os.chdir(path_4)
	os.system("echo 'simulate_network_KOV'")
	os.system(f"python simulate_network_KOV.py -i {cwd}/OG{D}/{P} -s full -k \"{Genes}\" -o \"{Genes}\"")
	os.system("echo 'check_KOV_to_sim'")
	os.system(f"python check_KOV_to_sim.py -i {cwd}/OG{D}/{P} -s full -k \"{Genes}\" -o \"{Genes}\"")

print('My work here is done')

