#!/bin/bash

#SBATCH --job-name=single_triangle
#SBATCH --mail-user=avrut@umich.edu
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=5000m
#SBATCH --time=40:00
#SBATCH --account=engin1
#SBATCH --partition=standard
#SBATCH --output=/home/%u/osiris/log/%x-%j.log

export EXEC=osiris-2D.e 
export INPUT_DECK=single_triangle.2d
export RUN_NAME=2D_single_triangle # folder we are running from

export deckdir=~/simulations/$RUN_NAME
export execdir=~/osiris/bin
export datadir=~/simulations/$RUN_NAME

rm -rf MS/ TIMINGS/ # clear previous run data
mpirun $execdir/$EXEC $deckdir/$INPUT_DECK # run osiris