#!/bin/bash
#SBATCH --mem=10G
#SBATCH --ntasks=1
#SBATCH --job-name=build-container
#SBATCH --cpus-per-task=8
#SBTACH --time=3600
apptainer build gegelati-arm.sif gegelati-arm.def
