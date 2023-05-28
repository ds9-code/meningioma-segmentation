#!/bin/bash

export nnUNet_raw_data_base=/cbica/home/sreedhad/comp_space/nnUNet_raw_data_base
export nnUNet_preprocessed=/cbica/home/sreedhad/comp_space/nnUNet_preprocessed
export RESULTS_FOLDER=/cbica/home/sreedhad/comp_space/nnUNet_trained_models
module load python/nnUNet/aa53b3b
module load cuda/11.2

#nnUNet_predict -i $nnUNet_raw_data_base/nnUNet_raw_data/Task501_Meningioma/imagesTs/ -o $nnUNet_raw_data_base/t501_inference -t 501 -m 3d_fullres --save_npz
nnUNet_predict -i $nnUNet_raw_data_base/nnUNet_raw_data/Task501_Meningioma/imagesTs1/ -o $nnUNet_raw_data_base/t501_inference -t 501 -m 3d_fullres --save_npz
