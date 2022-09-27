#!/bin/bash

#SBATCH --job-name=raman1D_osiris
#SBATCH --mail-user=avrut@umich.edu
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=4
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=5000m
#SBATCH --time=180:00
#SBATCH --account=engin1
#SBATCH --partition=standard
#SBATCH --output=/home/%u/log/%j-%x.log

export EXEC=osiris-1D.e 
export INPUT_DECK=raman.1d
export RUN_NAME=1D_raman # folder we are running from

export deckdir=~/osiris-simulations/$RUN_NAME
export execdir=~/osiris/bin
export datadir=~/osiris-simulations/$RUN_NAME

module load intel openmpi hdf5

rm -rf MS/ TIMINGS/ # clear previous run data
mpirun $execdir/$EXEC $deckdir/$INPUT_DECK # run osiris
sbatch --dependency=afterany:$SLURM_JOB_ID  generate_videos.sh # generate videos