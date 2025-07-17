# Robotic Arm Setup

Repository gathering infos and scripts to reproduce TPG training for the robotic arm.

# Build image on slurm

`sbatch build-container.sh`

# Run training

## Generate configurations files

`python3 path/to/experiment --action generate`

## Run training on slurm

`python3 path/to/experiment --action submit`

## Parse results and gather them in csv

`python3 path/to/experiment --action parse`

