# Launching_Cardamom
Contains the files needed to excecute CARDAMOM on a distant Computing Centre

The launch_carda.sh script can be executed with sbatch launch_carda.sh command.

The carda.py script has to be carefully reviewed before use. It will execute the specified CARDAMOM scripts, with the specified parameters.

Both script should be copied out of the Launching_Cardamom directory, since the carda.py script will create dedicated folders in which to execute the specified CARDAMOM scripts and store their results. 

