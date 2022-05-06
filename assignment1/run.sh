#!/usr/bin/env bash
#SBATCH --partition=csedu
#SBATCH --output=output/std_%A_%a.txt
#SBATCH --error=output/%A_%a.err
#SBATCH --mem=100M
#SBATCH --time=4-0:00:00
#SBATCH --array=0-8%1

matrix_sizes=($(seq 1 1 8))
repetitions=($(seq 1 1 3))
cores=($(seq 1 1 10))
m_size=${matrix_sizes[$SLURM_ARRAY_TASK_ID]}
rep=${repetitions[$SLURM_ARRAY_TASK_ID]}
num_cores=${cores[$SLURM_ARRAY_TASK_ID]}
cd ~/Parallel_computing
mpicc -fopenmp -DMPI -o relax relax_omp.c
time salloc -p csedu --cpus-per-task=${num_cores} -n 1 mpirun ./relax $[10**${m_size}] 500 4