#!/bin/bash
EXPERIMENT_FOLDER=$1
BIN_FOLDER=/armlearn-wrapper/build
apptainer exec --bind $EXPERIMENT_FOLDER/params:/params/ --bind $EXPERIMENT_FOLDER/outLogs:/outLogs/ ./armlearn-wrapper/container/gegelati-armlearn.sif /bin/bash -c "cd / && .$BIN_FOLDER/Training"