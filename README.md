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

`python3 path/to/experiment --action generate`

## Run training on slurm

`python3 path/to/experiment --action submit`

## Parse results and gather them in csv

`python3 path/to/experiment --action parse`

Authors: Mickaël Dardaillon, Paul Allaire

**forked** from https://gitlab.insa-rennes.fr/mdardail/robot-arm-setup/
