## TPG ExpeManager - TPG Experiment Manager: 

Repository gathering scripts to realize **TPG experiments** for a given **Learning Environment** (*armlearn*).
An **experiment** consist in selecting specific parameters, thus creating a **config**, launching the training of the TPG and finally plotting the results.

The scripts are used to:

1. Generate experiment folders from selected parameters. Modify JSON default parameters files dynamically, inserting the choosen parameters. - **Generate the config**

3. Submits experiments to a Slurm cluster. - **Train the TPG**

4. Parses results into a single CSV. - **Collect results**

# Build image on slurm

`sbatch build-container.sh`

# Run training

## Generate configurations files

`python3 manage-experiment.py --action generate path/to/experiment/folder`

## Run training on slurm

`python3 manage-experiment.py --action submit path/to/experiment/folder`

## Parse results and gather them in csv

`python3 manage-experiment.py --action parse path/to/experiment/folder`

Authors: Mickaël Dardaillon, Paul Allaire

**forked** from https://gitlab.insa-rennes.fr/mdardail/robot-arm-setup/

## VENV
# 1. Create a new virtual environment
python3 -m venv venv

# 2. Activate it	
source venv/bin/activate

# 3. Install packages normally
pip install pandas 
