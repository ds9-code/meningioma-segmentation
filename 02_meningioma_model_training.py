# -*- coding: utf-8 -*-
from google.colab import drive
drive.mount('/content/drive')

!pip install nnunet

import os
os.environ['nnUNet_raw_data_base'] = "/content/drive/MyDrive/nnUNet/nnUNet_raw_data_base/"
os.environ['nnUNet_preprocessed'] =  "/content/drive/MyDrive/nnUNet/nnUNet_preprocessed"
os.environ['RESULTS_FOLDER'] = "/content/drive/MyDrive/nnUNet/nnUNet_trained_models"

# update the fold # and rerun. Here fold 0 is shown
!nnUNet_train 3d_fullres nnUNetTrainerV2 Task510_Meningioma 0 --npz