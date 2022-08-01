#!/bin/bash

#SBATCH --job-name=osiris_run
#SBATCH --mail-user=avrut@umich.edu
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=5000m
#SBATCH --time=250:00
#SBATCH --account=engin1
#SBATCH --partition=standard
#SBATCH --output=/home/%u/osiris/log/%x-%j.log

export EXEC=osiris-2D.e 
export INPUT_DECK=four_triangle.2d
export RUN_NAME=2d\ 4\ triangle # folder we are running from

export deckdir=~/osiris-simulations/$RUN_NAME
export execdir=~/osiris/bin
export datadir=~/osiris-simulations/$RUN_NAME

cd datadir
rm -rf MS/ TIMINGS/ # clear previous run data
mpirun $execdir/$EXEC $deckdir/$INPUT_DECK # run osiris
python3 generate_videos.py