#!/usr/bin/env zsh

#SBATCH -p wacc
#SBATCH -t 0-00:25
#SBATCH -c 8
#SBATCH -o slurm.%j.out
#SBATCH -e slurm.%j.err

singularity pull me468_a10.sif docker://gitlab.wacc.wisc.edu/me468/dockerimage:hw10
