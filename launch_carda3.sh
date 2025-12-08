#!/bin/bash
#SBATCH --job-name=3635
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=olivier.gandrillon@ens-lyon.fr
#SBATCH --export=NONE
module load Programming_Languages/python/3.12.2
source carda_venv_12/bin/activate
module load Programming_Languages/R/latest
python3 Launching_Cardamom/carda3.py 
