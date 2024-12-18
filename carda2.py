# Launch CARDAMOM in one command line
# create a new directory for each parameter combination
# Still requires specific R script at that stage 

import os
import numpy as np
import matplotlib.pyplot as plt
from harissa.utils import build_pos, plot_network

# Hyperparameters
D=3526 # project name
P=5# Experiment within project
SFT=4 # time scale factor
CC=2 # cell cycle time:
T=4 #threshold for interactions 
sf=10 # scaling factor: in order to provide a more comprehensive representation of the network's dynamics# amplify the scaling factor applied to the network's edges.
seq="3519_5" # R script to be launched
cwd = os.getcwd()
rval=2.5
percent_valid=0.6 # percentage of KD values to be considered as valid
KO=0
Gene_to_KO='PENK'

Infer=1# to infer the GRN
Simulate=1# to simulate the GRN
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
os.system("cp  "+str(cwd)+"/cardamom/Kanto_1D_OG.py Kanto_1D_OG.py")
os.system("cp  "+str(cwd)+"/cardamom/Draw_GRN_2.py Draw_GRN_2.py")
os.system("mkdir " +str(P))
os.chdir(str(P))
os.system("mkdir Data")
os.system("mkdir Results")
os.system("mkdir Rates")
os.system("mkdir cardamom")

# Launch R script to generate entry files
os.system("Rscript --vanilla  "+str(cwd)+"/res_carda/"+str(seq)+".R "+str(SFT)+" "+str(CC)+" "+str(P)+" "+str(D))

# Move to the central cardamom directory (cwd)
os.chdir("../")

# Infer GRN
if Infer:
	os.system( "python infer_network.py -i " + str(cwd)+"/OG"+str(D)+"/"+str(P))

# Modify the resulting matrix	
	os.chdir(str(cwd)+"/OG"+str(D)+"/"+str(P)+"/cardamom")

# Open files
    basal = np.load('basal.npy')
    inter = np.load('inter.npy')
	kmin = np.load('kmin.npy')

# Modify interactions values
	fi=sf*inter
	basal = sf*basal

	# Cut off low intensity edges
	fi[abs(fi) < T] = 0
	fi_t[abs(fi_t) < T] = 0
	# Save the resulting matrix
	np.save('inter.npy', fi)
	np.savetxt('inter.csv', fi, delimiter=",")

	np.save('basal.npy', basal)

	# Same for time-dependent matrix
	for i in range(0, len(fi_t)):	
			fi = np.load('inter_{}.npy'.format(i))	
			fi=fi*sf
			fi[abs(fi) < T] = 0
			np.save('inter_{}.npy'.format(i), fi)
			np.savetxt('inter_{}.csv'.format(i), fi, delimiter=",")

# Add transfert 
	os.chdir(str(cwd)+"/OG"+str(D)+"/"+str(P)+"/Data")
	data_real = np.loadtxt('panel_real.txt', dtype=float, delimiter='\t')[1:, 1:].T
    C, G = data_real.shape

    inter[:, :] = inter_t[-1][:, :] + (1 - rval/G) * np.diag(basal_t[-1])
	inter[1:, 1:] /= (1 - .6 * rval/G)
	inter -= np.diag(np.diag(inter)) * .6 * rval/G
	basal[:] = rval/G * basal_t[-1]
	np.save('basal.npy', basal)
	np.save('inter.npy', inter)

# KO
	if KO:
# Find the index of the gene 
		os.chdir("/pbs/home/o/ogandril/OG"+str(D)+"/"+str(P)+"/Data")

		with open('../Data/Genenames.txt') as f:
			Genenames = f.read().splitlines()

		i=Genenames.index(Gene_to_KO)

		os.chdir("/pbs/home/o/ogandril/OG"+str(D)+"/"+str(P)+"/cardamom")
		basal= np.load('basal.npy')
		basal[i]=  -1000

# Valeur minimale de k_on
		kmin = np.load('kmin.npy')
		kmin[i] =  0 # Devrait déjà être proche de 0

# Save the modified files
		np.save('basal.npy', basal) # Récupérer ce fichier et le renommer 'basal_t.npy'
		np.save('kmin.npy', kmin) # Récupérer ce fichier et le renommer 'kmin.npy'



# Simulate
os.chdir(str(cwd)+"/OG"+str(D))
if Simulate:
    os.system( "python simulate_data.py -i " +str(P)+" -r " +str(rval))

# Visualize
if Visualize:
	os.system( "python visualize_data.py -i " +str(P)+ " " +str(percent_valid))

# Compute Kanto distances
if Kanto:
	os.system("python Kanto_1D_OG.py " +str(D)+ " " + str(P)+ " " + str(cwd) + " " +  str(percent_valid))

# Draw the GRN
if Draw:
	os.system("python Draw_GRN_2.py " +str(D)+" "+ str(P)+" "+ str(T)+" " + str(cwd))

# Write parameter values
os.chdir(str(cwd)+"/OG"+str(D)+"/"+str(P)+"/Results")
text = ['time scale factor: '+str(SFT), 
"cell cycle time: " + str(CC), 
"sequence modelized: " +str(seq),
"Transfert: "+str(transfert),
"rval: "+str(rval),
"Threshold: "+str(T),
"Scaling factor: "+str(sf),
"Percentage of correct values: "+str(percent_valid)],
"KO: "+str(KO),
"Knocked_out gene: "+str(Gene_to_KO)

with open('parameters', 'w') as f:
	for line in text:
        	f.write(line)
        	f.write('\n')


print('My work here is done')
