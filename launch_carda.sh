#!/bin/bash
#
#SBATCH --job-name=3519_1
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=olivier.gandrillon@ens-lyon.fr
module add python
module load Programming_Languages/R/latest
python carda2.py