#!/bin/bash
#SBATCH --mem=10G
#SBATCH --ntasks=1
#SBATCH --job-name=testArmGegelati1
#SBATCH --cpus-per-task=128
#SBATCH --time=7200
# X coeurs, 100 gens, pas de limite de temps (juste scheduler)
EXPERIMENT_FOLDER=$1
BIN_FOLDER=/armlearn-wrapper/build
apptainer exec --bind $EXPERIMENT_FOLDER/params:/params/ --bind $EXPERIMENT_FOLDER/outLogs:/outLogs/ ./armlearn-wrapper/container/gegelati-armlearn.sif /bin/bash -c "cd / && .$BIN_FOLDER/armGegelati"