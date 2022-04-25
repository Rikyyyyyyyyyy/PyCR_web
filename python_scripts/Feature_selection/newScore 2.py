import operator
import copy
from numpy import inf
import sys
from scipy.sparse.linalg import svds
import fisherRatio_in
import gen_clust
import numpy as np
from sklearn.model_selection import train_test_split

def setNumber(classNum, classList, allSampleList, startNum, endNum):
    # get sample matrix from file, column is variable and row is sample
    allSampleList = np.array(allSampleList)
    #get the half randomly selected sample and calculate the fisher ration
    sample_training, sample_test, class_training, class_test = selectHalfRandom(allSampleList, classList)
    fisherRatio = fisherRatio_in.cal_ratio(sample_training, class_training, classNum)
    sorted_fisherRatio = sorted(fisherRatio.items(), key=operator.itemgetter(1), reverse=True)

    # get the start variable list and end variable list by startNum and end Numx
    startNumList = []
    endNumList = []
    for i in sorted_fisherRatio:
        if i[1] > startNum:
            startNumList.append(i[0])
        if i[1]< startNum and i[1]>endNum:
            endNumList.append(i[0])
    #calculate the old score with all the variables inside
    scaled_half_samples,half_mean,half_svd = scale_half_data(sample_training)
    scaled_all_samples = scale_all_data(allSampleList,half_mean,half_svd)
    temp_score = calScore(scaled_half_samples, scaled_all_samples)
    oldScore = gen_clust.RunClust(temp_score,classList,2)
    finalOutPutIdx = []
    copy_all_scaled_samples = copy.deepcopy(scaled_all_samples)
    copy_half_scaled_samples = copy.deepcopy(scaled_half_samples)

    all_variable_idx = []
    for v in range(len(allSampleList[0])):
        all_variable_idx.append(v)

    # get rid of the variable form teh start variable list and calculate the score again
    # compare with the the old score
    # if the new score is lower than the old score, we need save the variable in selected variable list
    # if the new score is higher than the old score, we need put the variable back
    for idx in startNumList:
        all_variable_idx.remove(idx)
        temp_scaled_half_samples = scaled_half_samples[:, all_variable_idx]
        temp_scaled_all_samples = scaled_all_samples[:, all_variable_idx]
        temp_score = calScore(temp_scaled_half_samples, temp_scaled_all_samples)
        newScore = gen_clust.RunClust(temp_score, classList, 2)
        if newScore > oldScore:
            oldScore = newScore

        if newScore < oldScore:
            finalOutPutIdx.append(idx)
            all_variable_idx.append(idx)
            all_variable_idx.sort()

    # set threshold incase we dont have enough variables
    finalOutPutIdx = np.array(finalOutPutIdx)
    selected_all_matrix = copy_all_scaled_samples[:, (finalOutPutIdx.astype(int))]
    if selected_all_matrix.shape[1] < 3:
        finalOutPutIdx = startNumList[:10]

    # calculate the old score with all pre-selected variables
    finalOutPutIdx = np.array(finalOutPutIdx)
    selected_all_matrix = copy_all_scaled_samples[:, (finalOutPutIdx.astype(int))]
    selected_half_matrix = copy_half_scaled_samples[:, (finalOutPutIdx.astype(int))]
    temp_score = calScore(selected_half_matrix, selected_all_matrix)
    oldScore = gen_clust.RunClust(temp_score, classList, 2)
    finalOutPutIdx = list(finalOutPutIdx)

    # add the variable into the selected variable list
    # compare with the the old score
    # if the new score is lower than the old score, we need put the variable back
    # if the new score is higher than the old score, we need save the variable in selected variable list
    for index in endNumList:
        finalOutPutIdx.append(index)
        finalOutPutIdx = np.array(finalOutPutIdx)
        selected_all_matrix = copy_all_scaled_samples[:, (finalOutPutIdx)]
        selected_half_matrix = copy_half_scaled_samples[:, (finalOutPutIdx)]
        finalOutPutIdx = list(finalOutPutIdx)
        temp_score = calScore(selected_half_matrix, selected_all_matrix)
        newScore = gen_clust.RunClust(temp_score, classList, 2)
        print("old: " + str(oldScore))
        print("new: " + str(newScore))

        if newScore >= oldScore:
            oldScore = newScore
        if newScore < oldScore:
            finalOutPutIdx.remove(index)
    return finalOutPutIdx, sample_test, class_training, class_test

# scale all data with provide mean and std
def scale_all_data(samples,mean,std):
    functionTop = np.subtract(samples, mean)
    scaled_samples = np.divide(functionTop, std)
    for list in scaled_samples:
        list[list==inf] = 10**-12
    scaled_samples = np.nan_to_num(scaled_samples, nan=(10**-12))
    return scaled_samples

def scale_half_data(samples):
    # after get all the selected variables we make them a metrix and calculate the mean
    samples = np.array(samples)
    samples_mean = samples.mean(axis=0)
    samples_std = np.std(samples, axis=0)
    np.set_printoptions(threshold=sys.maxsize)
    functionTop = np.subtract(samples,samples_mean)
    scaled_samples = np.divide(functionTop, samples_std)
    scaled_samples = np.nan_to_num(scaled_samples,nan=(10**-12))
    for list in scaled_samples:
        list[list==inf] = 10**-12

    return scaled_samples, samples_mean, samples_std

# randomly select half variables from the selected_scaled_variables_list
def selectHalfRandom(sample_list,class_list):
    sample_matrix = np.array(sample_list)
    class_matrix = np.array(class_list)
    X_train, X_test, y_train, y_test = train_test_split(sample_matrix, class_matrix, test_size=0.5)
    return X_train, X_test, y_train, y_test

def calScore(rand_variable_list,all_variable_list):
    # rand_variable_list = csc_matrix(rand_variable_list,dtype=float)
    dummyU,dummyS,V = svds(rand_variable_list, k=2)
    V = np.transpose(V)
    score = np.dot(all_variable_list, V)
    return score

















