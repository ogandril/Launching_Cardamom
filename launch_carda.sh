#!/bin/bash
#
#SBATCH --job-name=3443
#SBATCH --time=0-01:00:00
#SBATCH --partition=Cascade
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=olivier.gandrillon@ens-lyon.fr

python carda.py
