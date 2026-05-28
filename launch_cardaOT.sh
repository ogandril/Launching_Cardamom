#!/bin/bash
#SBATCH --job-name=3731
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=olivier.gandrillon@ens-lyon.fr
#SBATCH --export=NONE
module load Programming_Languages/python/3.12.2
source cardamom_env/bin/activate
python3 Launching_Cardamom/CardaOT.py $1 $2 $3 $4 $5 $6 $7 $8 $9
