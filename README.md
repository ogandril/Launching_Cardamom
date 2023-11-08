# Launching_Cardamom

Contains the files needed to excecute CARDAMOM on a distant Computing Centre

See https://github.com/ogandril/cardamom to get the required CARDAMOM scripts 

The launch_carda.sh script can be executed with "sbatch launch_carda.sh" slurm command.

The carda.py script has to be carefully reviewed before use. It will execute the specified CARDAMOM scripts, with the specified parameters.

Both scripts should be copied out of the Launching_Cardamom directory, since the carda.py script will create dedicated folders in which to execute the specified CARDAMOM scripts and store their results. 

The carda.py script will expect a .R script located in a res_carda directory. This .R script will generate the data files required by CARDAMOM.


