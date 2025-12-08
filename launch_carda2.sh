#!/bin/bash
#SBATCH --job-name=3622
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=olivier.gandrillon@ens-lyon.fr
#SBATCH --export=NONE
source carda_venv_12/bin/activate
module load Programming_Languages/R/latest
export PYTHONPATH="$(dirname $(which python))/../lib/python3.9/site-packages:$PYTHONPATH"
/pbs/home/o/ogandril/carda_venv_12/bin/python /pbs/home/o/ogandril/Launching_Cardamom/carda2.py

