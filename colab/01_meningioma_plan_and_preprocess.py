# DS9 - 11/29/2022
"""01.Meningioma Plan and Preprocess.ipynb
"""

from google.colab import drive
drive.mount('/content/drive')

!pip install nnunet

import os
os.environ['nnUNet_raw_data_base'] = "/content/drive/MyDrive/nnUNet/nnUNet_raw_data_base/"
os.environ['nnUNet_preprocessed'] =  "/content/drive/MyDrive/nnUNet/nnUNet_preprocessed"
os.environ['RESULTS_FOLDER'] = "/content/drive/MyDrive/nnUNet/nnUNet_trained_models"

# Verify dataset integrity has to be executed only the first time you are pre-processing the data
# After successful plan and preprocessing
# 510 is the Task ID
!nnUNet_plan_and_preprocess -t 510 --verify_dataset_integrity