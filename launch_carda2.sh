#!/bin/bash
#SBATCH --job-name=3622
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=olivier.gandrillon@ens-lyon.fr
#SBATCH --export=NONE
module load Programming_Languages/python/3.12.2
source carda_venv_12/bin/activate
module load Programming_Languages/R/latest
export PYTHONPATH="$(dirname $(which python))/../lib/python3.9/site-packages:$PYTHONPATH"
python /pbs/home/o/ogandril/Launching_Cardamom/carda2.py

