#!/bin/bash

#SBATCH --job-name=test_brewster_30
#SBATCH --mail-user=avrut@umich.edu
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=4000m
#SBATCH --time=12:00
#SBATCH --account=engin1
#SBATCH --partition=standard
#SBATCH --output=/home/%u/log/%x-%j.log

module load intel openmpi hdf5 ffmpeg
source ~/.venv/plasma/bin/activate

export EXEC=osiris-2D.e 
export INPUT_DECK=test_brewster.2d
export RUN_NAME=2D_brewster # folder we are running from

export deckdir=~/osiris-simulations/$RUN_NAME
export execdir=~/osiris/bin
export datadir=~/osiris-simulations/$RUN_NAME

rm -rf MS/ TIMINGS/ # clear previous run data
mpirun $execdir/$EXEC $deckdir/$INPUT_DECK # run osiris
python3 generate_videos.py