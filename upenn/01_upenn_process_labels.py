# Process meningioma labels to remove unwanted labels
# DS9 - 11/29/2022

import nibabel as nib
import numpy as np
import os
import pathlib

base_img_path = '/cbica/home/sreedhad/comp_space/nnUNet_raw_data_base/nnUNet_raw_data/Task501_Meningioma/labelsTr'

patients = os.listdir(base_img_path)
patients.sort()


# Create a list of labels we dont want
bad_labels = [2,4,5,6]

# Loop through each patient in patients list, read the labels, change them and save the new file
for patient in patients:

  # new_img_dir = f'{out_dirpath}/{patient}'

  # If patient sub-folder does not exist, create it
  # if not os.path.exists(new_img_dir):
  #   os.makedirs(new_img_dir)

  img_path = base_img_path + '/' + patient

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
  img_data[(img_data == 3)] = int(2)

  int_img_data = img_data.astype(np.int)

  # Check min, max and unique values again
  print("After label conversion ")
  print(np.amin(int_img_data),np.amax(int_img_data))
  print(np.unique(int_img_data))

# Convert array back to Nii image
  new_img = nib.Nifti1Image(int_img_data, img.affine, img.header)
  #new_img_path = base_img_path + '/' + patient.split('_')[0] + '.nii.gz'
  new_img_path = base_img_path + '/' + patient

  # Save image to out_dir_path
  nib.save(new_img, new_img_path)
  print("Saved as: " + new_img_path)
