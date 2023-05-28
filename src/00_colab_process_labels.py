# DS9 - 11/29/2022
"""00_process_labels.ipynb
Process segmentation labels in the training dataset to ensure they are numbered consecutively
This is required for nnU-Net data integrity validation step
"""

import nibabel as nib
import numpy as np
import os
import pathlib
import matplotlib.pyplot as plt

from google.colab import drive
drive.mount('/content/drive')

base_img_path = f'/content/drive/MyDrive/UPennMeningioma'
out_dirpath = f'/content/drive/MyDrive/nnUNet/nnUNet_raw_data_base/nnUNet_raw_data/Task510_Meningioma/labelsTr'

patients = os.listdir(base_img_path)
patients.sort()
# print(patients)
print(len(patients))


# Create a list of labels we dont want
bad_labels = [2.0,4.0,5.0,6.0]

# Loop through each patient in patients list, read the labels, change them and save the new file
for patient in patients:

  # new_img_dir = f'{out_dirpath}/{patient}'

  # If patient sub-folder does not exist, create it
  # if not os.path.exists(new_img_dir):
  #   os.makedirs(new_img_dir)

  img_path = f'/content/drive/MyDrive/UPennMeningioma/{patient}/{patient}_segmentation.nii.gz'  
  
  # Load image
  img = nib.load(img_path)
  print("-"*100)
  print ("Patient: ", patient)

  # Store image as a numpy array
  img_data = img.get_fdata()

  # Check array min, max and unique values for image
  print("Before label check")
  print(np.amin(img_data),np.amax(img_data))
  print(np.unique(img_data))

# nnUnet requires labels to be continuous, and doesnt take 0, 1, 3 as input. It fails on the dataset integrity checks
# Here, we first remove any label that is NOT 0, 1, or 3. Then where the label is 3, we reset it to 2 to make it continuous

  # If array value is not 1 or 3, set it to zero
  # img_data[(img_data == 2.0) | (img_data == 4.0) | (img_data == 5.0) | (img_data == 6.0)] = 0
  img_data[np.isin(img_data, bad_labels)] = 0

  # Where label is 3, reset it to 2 so nnUnet doesnt complain about non-consecutive labels
  img_data[(img_data == 3.0)] = 2.0

  # Check min, max and unique values again
  print("After label conversion")
  print(np.amin(img_data),np.amax(img_data))
  print(np.unique(img_data))

  # Convert array back to Nii image
  new_img = nib.Nifti1Image(img_data, img.affine, img.header)

  # Set up new image path
  new_img_path = f'{out_dirpath}/{patient}.nii.gz'
  
  # Save image to out_dir_path
  nib.save(new_img, new_img_path)

  # for slice_number in range(img_data.shape[2]):
  #   print(np.amin(img_data[:,:,slice_number]),np.amax(img_data[:,:,slice_number]))
  #   img_data[(img_data != 1) | (img_data != 3)] = 0
  #   print ("Patient: ", patient)
  #   print(np.unique(img_data[:,:,slice_number]))