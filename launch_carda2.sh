#!/bin/bash
#SBATCH --job-name=3622
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=olivier.gandrillon@ens-lyon.fr
#SBATCH --export=NONE
source carda_venv_12/bin/activate
module load Programming_Languages/R/latest
python /pbs/home/o/ogandril/Launching_Cardamom/carda2.py

