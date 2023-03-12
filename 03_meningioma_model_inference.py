# -*- coding: utf-8 -*-

from google.colab import drive
drive.mount('/content/drive')

!pip install nnunet

import os
os.environ['nnUNet_raw_data_base'] = "/content/drive/MyDrive/nnUNet/nnUNet_raw_data_base/"
os.environ['nnUNet_preprocessed'] =  "/content/drive/MyDrive/nnUNet/nnUNet_preprocessed"
os.environ['RESULTS_FOLDER'] = "/content/drive/MyDrive/nnUNet/nnUNet_trained_models"
!nnUNet_find_best_configuration -m 3d_fullres -t 510

!nnUNet_predict -i $nnUNet_raw_data_base/nnUNet_raw_data/Task510_Meningioma/imagesTs/ -o $nnUNet_raw_data_base/inference -t 510 -m 3d_fullres --save_npz

import SimpleITK as sitk

image = sitk.ReadImage('volume.nii.gz', sitk.sitkFloat32)
label = sitk.ReadImage('label.nii.gz', sitk.sitkInt8)

image = sitk.Cast(sitk.RescaleIntensity(image, 0, 255), sitk.sitkUInt8)

overlay = sitk.LabelOverlay(image=image, labelImage=label, opacity=0.3)
sitk.WriteImage(overlay, 'overlay.nii.gz')