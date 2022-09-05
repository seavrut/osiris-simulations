#!/bin/bash

#SBATCH --job-name=four_triangle_osiris
#SBATCH --mail-user=avrut@umich.edu
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=5000m
#SBATCH --time=40:00
#SBATCH --account=engin1
#SBATCH --partition=standard
#SBATCH --output=/home/%u/log/%x-%j.log

module load intel openmpi hdf5

export EXEC=osiris-2D.e 
export INPUT_DECK=four_triangle.2d
export RUN_NAME=2D_four_triangle # folder we are running from

export deckdir=~/osiris-simulations/$RUN_NAME
export execdir=~/osiris/bin
export datadir=~/osiris-simulations/$RUN_NAME

rm -rf MS/ TIMINGS/ # clear previous run data
mpirun $execdir/$EXEC $deckdir/$INPUT_DECK # run osiris
sbatch --dependency=afterany:$SLURM_JOB_ID  generate_videos.sh # generate videos