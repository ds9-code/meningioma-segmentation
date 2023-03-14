# Automated segmentation of Meningioma MRI scans using nnU-Net

## Table of Contents
- [Introduction](#introduction)
- [Setup and Configuration](#setup-and-configuration)
- [Model Training](#model-training)

## Introduction

Medical image segmentation involves the extraction of regions of interest from 3D image data, such as from MRI or CT scans. Segmentation helps physicians conduct a more precise analysis of anatomical data by isolating only the important, tumor related areas of a scan.

Manual tumor segmentation imposes a high burden on the radiologists and lacks intra- and inter-observer repeatability. Furthermore, many of the current methods for tumor assessment in neuro-oncology practice is based on 2D tumor measurements which cannot provide accurate information about the tumor sub-regions and its response to treatments. Automatic tumor segmentation of 3D MRI scans can facilitate tumor assessments and improve prediction of patient prognosis by providing reproducible volumetric measurements.

This study uses a self-adapting, deep learning, biomedical image segmentation framework called [nnU-Net (Isensee et al, 2019)](https://github.com/MIC-DKFZ/nnUNet) to segment meningioma tumors on 3D MRI scans across 4 MRI modalities (T1, T1-CE, T2, T2-FLAIR), and evaluates the deep learning model’s performance using spatial overlap metrics. The model’s segmentation results are also compared with ground truth segmentation images created by radiologists using volumetrics to assess its clinical applicability.

For more information on nnU-Net, please read the following paper:

	Isensee, F., Jaeger, P. F., Kohl, S. A., Petersen, J., & Maier-Hein, K. H. (2020). nnU-Net: a self-configuring method 
	for deep learning-based biomedical image segmentation. Nature Methods, 1-9.

## Setup and Configuration

### High level configuration notes

- nnU-Net requires the MRI data to be structured in a specific format so the pipeline can process it
- All images (including labels) must be 3D nifti files (.nii.gz)
- Base directory (entry point) should always be nnUNet_raw_data_base
- Each segmentation project is stored and processed as a "Task"
- Each Task is associated with a unique 3 digit task ID (nnU-Net authors recommend starting from 500 so it does not conflict with pretrained models' task IDs)
- Maximum task ID is 999
- The label files must contain segmentation maps that contain consecutive integers, starting with 0: 0, 1, 2, 3, ... n. Each class has its own unique label value.
- Imaging modalities (T1, T1-CE, T2, FLAIR) are identified by a four-digit integer at the end of the filename.

### My configuration settings

File name setup - nn-UNET expects patient identifier followed by the modality as it is searching for this pattern in the data processing step. Bulk renames were performed on Windows, but can be automated in Python as well. Files were renamed as shown below - 
- Bulk rename all the T1 modality files to 0001. So 2_t1_ss.nii.gz will be renamed to 2_0001.nii.gz
- Follow same pattern for T1CE (0001) and T2 (0002) and FLAIR (0003)
- Rename all segmentation files to have just the patient ID. So 2_segmentation.nii.gz is renamed to 2.nii.gz

## Model Training


## Model Performance Metrics
