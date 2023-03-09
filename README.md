# Automated segmentation of Meningioma MRI scans using nnU-Net

## Table of Contents
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



## Model Training


## Model Performance Metrics