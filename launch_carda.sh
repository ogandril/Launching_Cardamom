#!/bin/bash
#SBATCH --job-name=3622
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=olivier.gandrillon@ens-lyon.fr
#SBATCH --export=NONE
source carda/bin/activate
module load Programming_Languages/R/latest
export PYTHONPATH="$(dirname $(which python))/../lib/python3.9/site-packages:$PYTHONPATH"
python3 Launching_Cardamom/carda3.py  $1 $2 $3 $4 $5

