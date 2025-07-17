
import argparse
import json
import os
import re
import shutil
import subprocess

def copy_files(expe_folder):
    src_folder = 'armlearn-wrapper/params/'
    params_folder = expe_folder + '/params'
    os.makedirs(params_folder, exist_ok=True)
    out_logs_folder = expe_folder + '/outLogs/dotfiles'
    os.makedirs(out_logs_folder, exist_ok=True)
    files_to_copy = ['AllTarget.csv', 'params.json', 'trainParams.json']
    for file_name in files_to_copy:
        src_file_path = os.path.join(src_folder, file_name)
        dest_file_path = os.path.join(params_folder, file_name)
        shutil.copy2(src_file_path, dest_file_path)

def modify_json(expe_folder, parameters):
    # Load the JSON file
    params_file_path = os.path.join(expe_folder, 'trainParams.json')
    with open(params_file_path, 'r') as json_file:
        json_content = json_file.read()

    # Regular expression to remove both single-line and multi-line comments
    pattern = r'//.*?\n|/\*.*?\*/'
    json_uncommented = re.sub(pattern, '', json_content, flags=re.DOTALL | re.MULTILINE)
    data = json.loads(json_uncommented)

    # Modify the JSON data
    for key, value in parameters.items():
        if key in data:
            data[key] = value
        elif key != 'instrSetName':
            print(f"Key '{key}' not found in JSON file.")

    # Save the modified JSON data back to the file
    with open(params_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def experiment_name(parameters):
    return '_'.join(f"{key}-{value}" for key, value in parameters.items() if key != 'instrSetName')

def generate_files(parameters_set, expe_path):
    for parameters in parameters_set:
        expe_name = experiment_name(parameters)
        expe_folder = os.path.join(expe_path, expe_name)
        copy_files(expe_folder)
        modify_json(expe_folder + '/params', parameters)

def submit_jobs(parameters_set, expe_path):
    for parameters in parameters_set:
        expe_name = experiment_name(parameters)
        expe_folder = os.path.join(expe_path, expe_name)
        subprocess.run(['sbatch', './script-slurm.sh', expe_folder], check=True)

def parse_results(parameters_set, expe_path):
    import pandas as pd
    results_df = pd.DataFrame()
    for parameters in parameters_set:
        expe_name = experiment_name(parameters)
        file = os.path.join(expe_path, expe_name, 'outLogs', 'garbage.ods')
        if os.path.isfile(file):
            with open(file) as f:
                lines = f.readlines()
            columns = lines[1].split()
            df = pd.read_csv(file, delim_whitespace=True, skiprows=2, names=columns)
            df['seed'] = parameters['seed']
            df['instrType'] = parameters['instrType']
            df['instrSetName'] = parameters['instrSetName']
            results_df = pd.concat([results_df, df])

    results_df.to_csv('results.csv', index=False)

instructionsSets = [
    {
        'instrSetName': 'base',
        'useInstrTrig': False,
        'useInstrLogExp': False,
        'useInstrExpensiveArithmetic': True,
        'useInstrComparison': False
    },
    {
        'instrSetName': 'comp',
        'useInstrTrig': False,
        'useInstrLogExp': False,
        'useInstrExpensiveArithmetic': True,
        'useInstrComparison': True
    },
    {
        'instrSetName': 'logexp',
        'useInstrTrig': False,
        'useInstrLogExp': True,
        'useInstrExpensiveArithmetic': True,
        'useInstrComparison': True
    },
    {
        'instrSetName': 'trigo',
        'useInstrTrig': True,
        'useInstrLogExp': False,
        'useInstrExpensiveArithmetic': True,
        'useInstrComparison': True
    },
    {
        'instrSetName': 'complete',
        'useInstrTrig': True,
        'useInstrLogExp': True,
        'useInstrExpensiveArithmetic': True,
        'useInstrComparison': True
    },
    {
        'instrSetName': 'lowcost',
        'useInstrTrig': False,
        'useInstrLogExp': True,
        'useInstrExpensiveArithmetic': False,
        'useInstrComparison': True
    }
]

parameters_set = [
    {
        'seed': seed,
        'instrType': instrType,
        **instructionSet
    }
    for seed in range(5)
    for instrType in ['int', 'float', 'double']
    for instructionSet in instructionsSets
]

parser = argparse.ArgumentParser()
parser.add_argument('path')
parser.add_argument('--action', choices=['generate', 'submit', 'parse'])

args = parser.parse_args()

if args.action == 'generate':
    generate_files(parameters_set, args.path)
elif args.action == 'submit':
    submit_jobs(parameters_set, args.path)
elif args.action == 'parse':
    parse_results(parameters_set, args.path)
