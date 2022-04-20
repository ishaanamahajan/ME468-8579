#!/usr/bin/env zsh

#SBATCH -p wacc
#SBATCH -t 0-00:25
#SBATCH -c 2
#SBATCH --gpus=1
#SBATCH -o slurm.%j.out
#SBATCH -e slurm.%j.err

singularity run --nv -e me468_a10.sif /bin/bash a10_script.sh
