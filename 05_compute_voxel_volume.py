# -*- coding: utf-8 -*-

!pip install nibabel

# Mount Google Drive
from google.colab import drive
drive.mount('/content/drive')

import nibabel as nib
import numpy as np
import os
import pathlib
import matplotlib.pyplot as plt

inf_base_img_path = f'/content/drive/MyDrive/nnUNet/ClusterFiles/Inference'
patients = os.listdir(inf_base_img_path)
patients.sort()
# print(patients)
print(len(patients))
#print(patients)

# Compute voxel volumes for Inference labels

wt_vox = []
et_vox = []
ed_vox = []
patient_list = []

for patient in patients:

  # new_img_dir = f'{out_dirpath}/{patient}'

  # If patient sub-folder does not exist, create it
  # if not os.path.exists(new_img_dir):
  #   os.makedirs(new_img_dir)

  img_path = f'/content/drive/MyDrive/nnUNet/ClusterFiles/Inference/{patient}'  
  
  # Load image
  img = nib.load(img_path)
  #print("-"*100)
  pid_temp = patient.split('_')
  pid_temp1 = pid_temp[1].split('.')
  pid = pid_temp1[0]
  print ("Patient: ", pid)

  # Store image as a numpy array
  #img_data = img.get_fdata()
  patient_list.append(pid)
  wt_vox += [np.sum(img.get_fdata() == 0)]
  et_vox += [np.sum(img.get_fdata() == 1)]
  ed_vox += [np.sum(img.get_fdata() == 2)]
  
for x in range(0,72):
  print(patient_list[x], ",", wt_vox[x], ",", et_vox[x], ",", ed_vox[x])

gt_base_img_path = f'/content/drive/MyDrive/nnUNet/ClusterFiles/GT'
gt_patients = os.listdir(gt_base_img_path)
gt_patients.sort()
# print(patients)
print(len(gt_patients))
#print(patients)

# Compute voxel volumes for GT labels

wt_vox = []
et_vox = []
ed_vox = []
patient_list = []

for patient in gt_patients:

  # new_img_dir = f'{out_dirpath}/{patient}'

  # If patient sub-folder does not exist, create it
  # if not os.path.exists(new_img_dir):
  #   os.makedirs(new_img_dir)

  img_path = f'/content/drive/MyDrive/nnUNet/ClusterFiles/GT/{patient}'  
  
  # Load image
  img = nib.load(img_path)
  #print("-"*100)
  pid_temp = patient.split('_')
  pid = pid_temp[0]
  print ("Patient: ", pid)

  # Store image as a numpy array
  #img_data = img.get_fdata()
  patient_list.append(pid)
  wt_vox += [np.sum(img.get_fdata() == 0)]
  et_vox += [np.sum(img.get_fdata() == 1)]
  ed_vox += [np.sum(img.get_fdata() == 3)]
  
for x in range(0,72):
  print(patient_list[x], ",", wt_vox[x], ",", et_vox[x], ",", ed_vox[x])

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr
import statsmodels.api as sm

df_et = pd.read_csv('/content/drive/MyDrive/nnUNet/ClusterFiles/Stats/et-wt.csv')

_ = sns.lmplot(x='GT ET/WT', y='Predicted ET/WT', data=df_et, ci=None)
et_corr, _ = pearsonr(df_et['GT ET/WT'], df_et['Predicted ET/WT'])
print('Pearsons correlation: %.3f' % et_corr)

#create Bland-Altman plot for ET
f, ax = plt.subplots(1, figsize = (8,5))
sm.graphics.mean_diff_plot(df_et['GT ET/WT'], df_et['Predicted ET/WT'], ax = ax)

#display Bland-Altman plot
plt.show()

df_ed = pd.read_csv('/content/drive/MyDrive/nnUNet/ClusterFiles/Stats/ed-wt.csv')

_ = sns.lmplot(x='GT ED/WT', y='Predicted ED/WT', data=df_ed, ci=None)
ed_corr, _ = pearsonr(df_ed['GT ED/WT'], df_ed['Predicted ED/WT'])
print('Pearsons correlation: %.3f' % ed_corr)

#create Bland-Altman plot for ED
f, ax = plt.subplots(1, figsize = (8,5))
sm.graphics.mean_diff_plot(df_ed['GT ED/WT'], df_ed['Predicted ED/WT'], ax = ax)

#display Bland-Altman plot
plt.show()