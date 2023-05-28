# Setup the meningioma dataset for use by the nnUNet package
# DS9 - 11/29/2022

# Import pacakges
import shutil
import os, glob
import random
import numpy as np

# Set up folder paths
base_dir_path = '/cbica/home/ds9/comp_space/meningioma_data/Organized_Data'

# Target folders
train_folder = '/cbica/home/ds9/comp_space/nnUNet_raw_data_base/nnUNet_raw_data/Task501_Meningioma/imagesTr/'
test_folder = '/cbica/home/ds9/comp_space/nnUNet_raw_data_base/nnUNet_raw_data/Task501_Meningioma/imagesTs/'
labels_folder = '/cbica/home/ds9/comp_space/nnUNet_raw_data_base/nnUNet_raw_data/Task501_Meningioma/labelsTr/'

# Read all directories from source folder into a list and sort
patients = os.listdir(base_dir_path)
patients.sort()
print(len(patients))

# Train-test split. We need to split the data randomly into training set and test set
# Set percentage of patients we need in the test set, choose random patients from list up to that percentage and save it as the test list
# Put the remaining patients from original list into the training list

test_pct = int((len(patients)+1)/5) # divide length of array by 5 for 20% test data set
test_list = random.sample(list(patients), test_pct) # randomly choose 20% of patient list as test dataset
train_list = [pt for pt in patients if pt not in test_list]

# Setup the files for testing data

for tstp in test_list:
  print("Patient: "+ tstp)
  patient_img_src = os.path.join(base_dir_path, tstp)

  print("Copying patient files for patient " + tstp + " into the test directory")
  for file in glob.glob(os.path.join(patient_img_src, '*_LPS_rSRI.nii.gz')):
    #print(file)
    t1 = '_t1_'
    t1ce = '_t1ce_'
    t2 = '_t2_'
    flair = '_flair_'
    #adc = '_adc_'

    if t1 in file:
      target_name = 'meningioma_' + tstp + '_0000.nii.gz'
      target_file = os.path.join(test_folder, target_name)

    elif t1ce in file:
      target_name = 'meningioma_' + tstp + '_0001.nii.gz'
      target_file = os.path.join(test_folder, target_name)

    elif t2 in file:
      target_name = 'meningioma_' + tstp + '_0002.nii.gz'
      target_file = os.path.join(test_folder, target_name)

    elif flair in file:
      target_name = 'meningioma_' + tstp + '_0003.nii.gz'
      target_file = os.path.join(test_folder, target_name)

    else:
      print("Ignore ADC")

    shutil.copy(file, target_file)



# Setup the files for training data in the appropriate directory

for trp in train_list:
  print("Patient: "+ trp)
  patient_img_src = os.path.join(base_dir_path, trp)

  print("Copying patient files for patient " + trp + " into the training directory")
  for file in glob.glob(os.path.join(patient_img_src, '*_LPS_rSRI.nii.gz')):
    #print(file)
    t1 = '_t1_'
    t1ce = '_t1ce_'
    t2 = '_t2_'
    flair = '_flair_'
    #adc = '_adc_'

    if t1 in file:
      target_name = 'meningioma_' + trp + '_0000.nii.gz'
      target_file = os.path.join(train_folder, target_name)

    elif t1ce in file:
      target_name = 'meningioma_' + trp + '_0001.nii.gz'
      target_file = os.path.join(train_folder, target_name)

    elif t2 in file:
      target_name = 'meningioma_' + trp + '_0002.nii.gz'
      target_file = os.path.join(train_folder, target_name)

    elif flair in file:
      target_name = 'meningioma_' + trp + '_0003.nii.gz'
      target_file = os.path.join(train_folder, target_name)

    else:
      print("Ignore ADC")

    shutil.copy(file, target_file)

for ltr in train_list:
  print("Patient: "+ ltr)
  patient_img_src = os.path.join(base_dir_path, ltr)

  print("Copying label files for patient " + trp + " into the labels directory")
  for file in glob.glob(os.path.join(patient_img_src, '*_UpdatedManualSegm.nii.gz')):
    print(file)
    target_name = 'meningioma_' + ltr + '.nii.gz'
    target_file = os.path.join(labels_folder, target_name)
    shutil.copy(file, target_file)
