# Script calculates various statistics to be reported on a validation and a test set
# It calculates each stat for each of 5 labels and for whole tumor
# It calculates and reports each statistic as mean +/- SD
# It outputs the results into excel files, which you can view via rsync or mounting to cluster and opening in excel
# You can also add print statements to see the values as they are calculated for each patient

# Some of functions here were loosely based off of the following scripts:
# https://github.com/Issam28/Brain-tumor-segmentation/blob/master/evaluation_metrics.py
# https://github.com/sacmehta/3D-ESPNet/blob/master/ComputeDice.py
# https://github.com/deepmedic/deepmedic/blob/master/deepmedic/routines/testing.py
# https://loli.github.io/medpy/generated/medpy.metric.binary.dc.html

# Instructions to run:
# At the bare minimum, there are only 2 variables you need to update: num_train and num_test at the beginning of the main method
# (lines 172 and 175)

# Pediatric auto-segm labels:
# 0 = background
# 1 = enhancing core
# 2 = non-enhancing core
# 3 = cystic
# 4 = edema
# note: here, WT refers to whole tumor, i.e. all non-zero labels merged.
# Run this command at the terminal before running this python script - module load  python/MedPy/0.4.0

import numpy as np
import pandas as pd
import nibabel as nib
import csv
import matplotlib.pyplot as plt
from pandas import DataFrame
import medpy.metric
from medpy.metric.binary import hd95

def diceFunction(pred, ground):
    # given two segmentations for a patient, a model's inference and the ground truth, this function computes the dice score
    # For further explanation of what dice score is, see the following links:
    # https://en.wikipedia.org/wiki/S%C3%B8rensen%E2%80%93Dice_coefficient

    if pred.shape != ground.shape:
        raise ValueError("Shape mismatch: pred and ground must have the same shape.")

    # Compute Dice coefficient
    intersection = np.logical_and(pred, ground)
    # union_correct = pred * ground

    if ((pred.sum()==0) and (ground.sum()==0)):
        # label not present in either
        score = 1
    else:
        #print("Intersection: ", intersection.sum())
        #print("Prediction: ", pred.sum())
        #print("GT: ", ground.sum())
        score = (2. * intersection.sum()) / (pred.sum() + ground.sum())

    return score


def computeDiceScores(pred, ground):
    # This function computes the dice score for each of the label types

    d_wt = diceFunction(pred>0, ground>0)
    d_1 = diceFunction(pred==1, ground==1)
    d_2 = diceFunction(pred==2, ground==3)
#    d_3 = diceFunction(pred==3, ground==3)
#    d_4 = diceFunction(pred==4, ground==4)
#    d_5 = diceFunction(pred>1, ground>1)

#   return d_wt, d_1, d_2, d_3, d_4, d_5
    return d_wt, d_1, d_2

def sensitivity(pred, ground):
    # computes sensitivity between two inputs

    num=np.sum(np.multiply(ground, pred))
    denom=np.sum(ground)
    if denom==0:
        return np.nan
    else:
        return  num/denom

def computeSensitivity(pred, ground):

    im1 = np.asarray(pred)
    im2 = np.asarray(ground)

    s_wt = sensitivity(im1>0, im2>0)
    s_1 = sensitivity(im1==1, im2==1)
    s_2 = sensitivity(im1==2, im2==3)
    # s_3 = sensitivity(im1==3, im2==3)
    # s_4 = sensitivity(im1==4, im2==4)
    # s_5 = sensitivity(im1>1, im2>1)

    # return s_wt, s_1, s_2, s_3, s_4, s_5
    return s_wt, s_1, s_2

def specificity(pred, ground):

    num=np.sum(np.multiply(ground==0, pred==0))
    denom=np.sum(ground==0)
    if denom==0:
        return np.nan
    else:
        return  num/denom


def computeSpecificity(pred, ground):

    im1 = np.asarray(pred)
    im2 = np.asarray(ground)

    s_wt = specificity(im1>0, im2>0)
    s_1 = specificity(im1==1, im2==1)
    s_2 = specificity(im1==2, im2==3)
    # s_3 = specificity(im1==3, im2==3)
    # s_4 = specificity(im1==4, im2==4)
    # s_5 = specificity(im1>1, im2>1)

    # return s_wt, s_1, s_2, s_3, s_4, s_5
    return s_wt, s_1, s_2

def hausdorff95(pred, ground):
    # This computes the 95th percentile of the Huasdorff distance between the prediction and ground truth
    # For more information on what Hausdorff distance is, see the following links:
    # https://en.wikipedia.org/wiki/Hausdorff_distance
    # https://loli.github.io/medpy/_modules/medpy/metric/binary.html (command F "hd95")
    # https://eurradiolexp.springeropen.com/articles/10.1186/s41747-020-00200-2

    if (np.count_nonzero(ground) == 0) or (np.count_nonzero(pred) == 0):
        return np.nan

    return hd95(ground, pred)


def computeHausdorff95(pred, ground):

    im1 = np.asarray(pred)
    im2 = np.asarray(ground)

    h_wt = hausdorff95(im1>0, im2>0)
    h_1 = hausdorff95(im1==1, im2==1)
    h_2 = hausdorff95(im1==2, im2==3)
    # h_3 = hausdorff95(im1==3, im2==3)
    # h_4 = hausdorff95(im1==4, im2==4)
    # h_5 = hausdorff95(im1>1, im2>1)

    # return h_wt, h_1, h_2, h_3, h_4, h_5
    return h_wt, h_1, h_2


if __name__ == '__main__':

    # Change this to the number of patients in your training set
    num_train = 278

    # Change this to the number of patients in your testing set
    # num_test = 0

    total_patients = num_train

    # cfg files containing file paths
    # these were generated by the generate script in the train folder

    ground_truth_segmentations = './gt_train.cfg'
    predicted_segmentations = './predictions_train.cfg'

    # initialize 2D array to hold all dice values
    # columns: patients (from 0 to #patients - 1)
    # rows: WT, 1, 2, 3, 4
    dice_stats = [[], [], []]
    sensitivity_stats = [[], [], []]
    specificity_stats = [[], [], []]
    hd_stats = [[], [], []]
    patient_IDs = []

    gtFile = open(ground_truth_segmentations)
    gt_paths = gtFile.readlines()

    predFile = open(predicted_segmentations)
    pred_paths = predFile.readlines()

    print('start')
    for i in range(total_patients):
        this_gt_path = gt_paths[i].strip()
        print('GT - ', this_gt_path)
        this_pred_path = pred_paths[i].strip()
        print('Pred - ', this_pred_path)

        # load the Ground truth
        gth = nib.load(this_gt_path).get_fdata()
        gth = np.rint(gth)

        # load the predicted segmentation inference
        pred = nib.load(this_pred_path).get_fdata()
        pred = np.rint(pred)

        # get CID of this patient for excel file
        file_name = this_gt_path.split('/')[-1]
        pred_file_name = this_pred_path.split('/')[-1]

        cid_array = file_name.split('.')
        cid_name = cid_array[0]
        cid = cid_name.split('_')
        print(i, ' - ', cid[0], ' - ', pred_file_name)
        patient_IDs.append(cid[0])

        # note that for most functions, order of input matters (i.e. pred then ground truth, not vice versa)

        d_wt, d_1, d_2 = computeDiceScores(pred, gth)
        dice_stats[0].append(d_wt)
        dice_stats[1].append(d_1)
        dice_stats[2].append(d_2)
        # dice_stats[3].append(d_3)
        # dice_stats[4].append(d_4)
        # dice_stats[5].append(d_5)

        se_wt, se_1, se_2 = computeSensitivity(pred, gth)
        sensitivity_stats[0].append(se_wt)
        sensitivity_stats[1].append(se_1)
        sensitivity_stats[2].append(se_2)
        # sensitivity_stats[3].append(se_3)
        # sensitivity_stats[4].append(se_4)
        # sensitivity_stats[5].append(se_5)

        sp_wt, sp_1, sp_2 = computeSpecificity(pred, gth)
        specificity_stats[0].append(sp_wt)
        specificity_stats[1].append(sp_1)
        specificity_stats[2].append(sp_2)
        # specificity_stats[3].append(sp_3)
        # specificity_stats[4].append(sp_4)
        # specificity_stats[5].append(sp_5)

        h_wt, h_1, h_2 = computeHausdorff95(pred, gth)
        hd_stats[0].append(h_wt)
        hd_stats[1].append(h_1)
        hd_stats[2].append(h_2)
        # hd_stats[3].append(h_3)
        # hd_stats[4].append(h_4)
        # hd_stats[5].append(h_5)


    # Create an excel file and write the mean & std of each statistic to it
    # You can change this to your desired name

    train_summary_file = 'summary_statistics_train.csv'
    header = [
        'Region',
        'Dice (mean)', 'Dice (median)', 'Dice (std)',
        'Sensitivity (mean)', 'Sensitivity (median)', 'Sensitivity (std)',
        'Hausdorff 95 (mean)', 'Hausdorff 95 (median)', 'Hausdorff 95 (std)']
    train_data = [
        ['Whole Tumor',
        np.nanmean(dice_stats[0][0:num_train]), np.nanmedian(dice_stats[0][0:num_train]), np.nanstd(dice_stats[0][0:num_train]),
        np.nanmean(sensitivity_stats[0][0:num_train]), np.nanmedian(sensitivity_stats[0][0:num_train]), np.nanstd(sensitivity_stats[0][0:num_train]),
        np.nanmean(hd_stats[0][0:num_train]), np.nanmedian(hd_stats[0][0:num_train]), np.nanstd(hd_stats[0][0:num_train])],
        ['Enhancing Core',
        np.nanmean(dice_stats[1][0:num_train]), np.nanmedian(dice_stats[1][0:num_train]), np.nanstd(dice_stats[1][0:num_train]),
        np.nanmean(sensitivity_stats[1][0:num_train]),  np.nanmedian(sensitivity_stats[1][0:num_train]), np.nanstd(sensitivity_stats[1][0:num_train]),
        np.nanmean(hd_stats[1][0:num_train]), np.nanmedian(hd_stats[1][0:num_train]), np.nanstd(hd_stats[1][0:num_train])],
        ['Edema',
        np.nanmean(dice_stats[2][0:num_train]), np.nanmedian(dice_stats[2][0:num_train]), np.nanstd(dice_stats[2][0:num_train]),
        np.nanmean(sensitivity_stats[2][0:num_train]), np.nanmedian(sensitivity_stats[2][0:num_train]), np.nanstd(sensitivity_stats[2][0:num_train]),
        np.nanmean(hd_stats[2][0:num_train]), np.nanmedian(hd_stats[2][0:num_train]), np.nanstd(hd_stats[2][0:num_train])]
    ]

    with open(train_summary_file, 'w', encoding='UTF8', newline='') as train_file:
        writer = csv.writer(train_file)
        writer.writerow(header)
        writer.writerows(train_data)

    per_patient_results_file = 'dice_stats_per_train_patient.csv'
    header = ['Patient', 'WT Dice', 'ET Dice', 'ED Dice']
    transpose_dice = list(map(list, zip(*dice_stats)))
    patient_IDs_col = np.transpose(patient_IDs)
    data = np.c_[patient_IDs_col, transpose_dice]

    with open(per_patient_results_file, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)
