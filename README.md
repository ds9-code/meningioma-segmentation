# meningioma-segmentation
 Automated segmentation of Meningioma MRI scans using nnU-Net
 
## Introduction

Medical image segmentation involves the extraction of regions of interest from 3D image data, such as from MRI or CT scans. Segmentation helps physicians conduct a more precise analysis of anatomical data by isolating only the important, tumor related areas of a scan.

Manual tumor segmentation imposes a high burden on the radiologists and lacks intra- and inter-observer repeatability. Furthermore, many of the current methods for tumor assessment in neuro-oncology practice is based on 2D tumor measurements which cannot provide accurate information about the tumor sub-regions and its response to treatments. Automatic tumor segmentation of 3D MRI scans can facilitate tumor assessments and improve prediction of patient prognosis by providing reproducible volumetric measurements.

nnU-Net is a deep learning framework that automates several aspects of the automated segmentation pipeline, and provides a standardized baseline for biomedical segmentation.

In this project, we use nnU-Net to train a deep learning segmentation model to automatically segment multi-parametric 3D meningioma tumor scans. The scans were manually segmented by expert radiologists, which are used as the ground truth to compare and assess the model generated segmentation. 

## Setup and Configuration



## Training the models


## Model Performance Metrics