#!/bin/bash
#SBATCH --job-name=3634
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=olivier.gandrillon@ens-lyon.fr
#SBATCH --export=NONE
module load Programming_Languages/python/3.9
source carda_V1_venv/bin/activate
module load Programming_Languages/R/latest
python3 Launching_Cardamom/carda2.py 
