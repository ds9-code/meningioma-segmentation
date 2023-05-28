#!/bin/bash
# DS9 - 11/29/2022
export nnUNet_raw_data_base=/cbica/home/ds9/comp_space/nnUNet_raw_data_base
export nnUNet_preprocessed=/cbica/home/ds9/comp_space/nnUNet_preprocessed
export RESULTS_FOLDER=/cbica/home/ds9/comp_space/nnUNet_trained_models
module load python/nnUNet/aa53b3b
module load cuda/11.2

# Verify dataset integrity has to be executed only the first time you are pre-processing the data
# After successful plan and preprocessing
# 510 is the Task ID
nnUNet_plan_and_preprocess -t 510 --verify_dataset_integrity