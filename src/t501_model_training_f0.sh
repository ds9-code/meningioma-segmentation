#!/bin/bash

export nnUNet_raw_data_base=/cbica/home/sreedhad/comp_space/nnUNet_raw_data_base
export nnUNet_preprocessed=/cbica/home/sreedhad/comp_space/nnUNet_preprocessed
export RESULTS_FOLDER=/cbica/home/sreedhad/comp_space/nnUNet_trained_models
module load python/nnUNet/aa53b3b
module load cuda/11.2

nnUNet_train 3d_fullres nnUNetTrainerV2 Task501_Meningioma 0 --npz