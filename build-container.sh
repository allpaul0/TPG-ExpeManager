#!/bin/bash
#SBATCH --mem=10G
#SBATCH --ntasks=1
#SBATCH --job-name=build-container
#SBATCH --cpus-per-task=8
#SBTACH --time=3600
cd armlearn-wrapper/
apptainer build container/gegelati-armlearn.sif container/gegelati-armlearn.def
