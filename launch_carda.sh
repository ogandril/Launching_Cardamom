#!/bin/bash
#
#SBATCH --job-name=3507_1
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=olivier.gandrillon@ens-lyon.fr

module add python
python carda.py
