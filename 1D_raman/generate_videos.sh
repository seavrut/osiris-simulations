#!/bin/bash

#SBATCH --job-name=raman_videos
#SBATCH --mail-user=avrut@umich.edu
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=5000m
#SBATCH --time=180:00
#SBATCH --account=engin1
#SBATCH --partition=standard
#SBATCH --output=/home/%u/log/%j-%x.log

module load ffmpeg
source ~/.venv/plasma/bin/activate
python3 generate_videos.py