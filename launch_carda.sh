#!/bin/bash
#
#SBATCH --job-name=3604
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=olivier.gandrillon@ens-lyon.fr
#SBATCH --export=ALL
source carda/bin/activate
module load Programming_Languages/R/latest
python3 carda3.py
