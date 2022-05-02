import operator
import copy
from numpy import inf
import sys
from scipy.sparse.linalg import svds
from python_scripts.Feature_selection import fisherRatio_in
from python_scripts.Feature_selection import gen_clust
import numpy as np
import math
import os
import shutil
import imageio
import matplotlib.pyplot as plt
import matplotlib
from sklearn.model_selection import train_test_split
from scipy.stats.distributions import chi2
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import scale
import warnings
from python_scripts.Feature_selection import SelectivityRatio
from python_scripts.Feature_selection import vipScore
warnings.filterwarnings('ignore')
matplotlib.use('agg')
# start backward Feature Selection and Forward Feature selection
# INPUT : class number, class data, sample data, start number, stop number , spliting rate, iteration number(in main), original class name, scale type
# OUTPUT : selected variable index, training sample data, testing sample data, training class data, testing class data
def setNumber(classNum, classList, allSampleList, startNum, endNum,howMuchSplit,iternum, class_trans_dict,scale_type, V_rankingAlgorithm, nComponent,outputPath):
    CLASS_COLOR = ["#dc3c40", "#55a6bc", 'purple', 'yellowgreen', 'wheat', 'royalblue', '#42d7f5', '#ca7cf7', '#d2f77c']
    CLASS_LABEL = ["o", "x", "4", "*", "+", "D", "8", "s", "p"]
    allSampleList = np.array(allSampleList)
    #get the half randomly selected sample and calculate the fisher ration
    sample_training, sample_test, class_training, class_test = selectRandom(allSampleList, classList,howMuchSplit)
    if V_rankingAlgorithm == 'fisher':
        fisherRatio = fisherRatio_in.cal_ratio(sample_training, class_training, classNum)
    elif V_rankingAlgorithm == 'vip':
        fisherRatio = vipScore.vipy(sample_training, class_training, nComponent)
    elif V_rankingAlgorithm == 'selectivity':
        fisherRatio = SelectivityRatio.selrpy(sample_training, class_training, nComponent)
    sorted_fisherRatio = sorted(fisherRatio.items(), key=operator.itemgetter(1), reverse=True)

    # get the start variable list and end variable list by startNum and end Num
    startNumList = []
    endNumList = []
    sorted_fisher_idx = []
    # select all the variable with fisher ration larger than start number as start variables, selecte all the variable with fisher ratio between start and stop number as stop variables.

    for i in sorted_fisherRatio:
        if i[1] > startNum:
            startNumList.append(i[0])
        if i[1]< startNum and i[1]>endNum:
            endNumList.append(i[0])
        sorted_fisher_idx.append(i[0])

    # scale the data
    if scale_type == 'SVN':
        scaled_half_samples, col_mean = SVN_scale_half_data(sample_training)
        scaled_all_samples = SVN_scale_all_data(allSampleList, col_mean)
    else:
        scaled_half_samples, half_mean, half_std = scale_half_data(sample_training)
        scaled_all_samples = scale_all_data(allSampleList, half_mean, half_std)

    temp_score = calScore(scaled_half_samples[:,startNumList], scaled_all_samples[:,startNumList])
    oldScore = gen_clust.RunClust(temp_score,classList,classNum)

    # get rid of the variable form teh start variable list and calculate the score again
    # compare with the the old score
    # if the new score is lower than the old score, we need save the variable in selected variable list
    # if the new score is higher than the old score, we need put the variable back
    finalOutPutIdx = copy.copy(startNumList)
    class_index_list = []
    for i in range(classNum + 1):
        class_index_list.append([])
    for i in range(len(classList)):
        class_index_list[classList[i]].append(i)
    picCounter = 0

    #  Calculate the first score and get the sign
    sign_scaled_half_samples = scaled_half_samples[:, finalOutPutIdx]
    sign_scaled_all_samples = scaled_all_samples[:, finalOutPutIdx]
    dummyU, dummyS, V = svds(sign_scaled_half_samples, k=2)
    V = V.transpose()
    score = np.dot(sign_scaled_all_samples, V)
    score1 = score[:,0]
    score2 = score[:,1]

    # start the backward selection
    for idx in startNumList:
        if len(finalOutPutIdx) >2:
            finalOutPutIdx.remove(idx)
            temp_scaled_half_samples = scaled_half_samples[:, finalOutPutIdx]
            temp_scaled_all_samples = scaled_all_samples[:, finalOutPutIdx]
            temp_score = calScore(temp_scaled_half_samples, temp_scaled_all_samples)
            newScore = gen_clust.RunClust(temp_score, classList, classNum)
            s_old = round(oldScore, 4)
            s_new = round(newScore, 4)
            if newScore > oldScore:
                oldScore = newScore
                print("REMOVED, SCORES [new: old] - ["+ str(s_new) + ":"+str(s_old) + "]" )
            elif newScore < oldScore:
                print("KEPT   , SCORES [new: old] - ["+ str(s_new) + ":"+str(s_old) + "]" )
                finalOutPutIdx.append(idx)
                # generate the PCA graph for the first iteration and gather together to form a gif  animation
                if iternum ==0:
                    dummyU, dummyS, V = svds(temp_scaled_half_samples, k=2)
                    V = V.transpose()
                    score = np.dot(temp_scaled_all_samples, V)
                    temp_score1 = score[:,0]
                    temp_score1 = np.transpose(temp_score1)
                    temp_score2 = score[:, 1]
                    temp_score2 = np.transpose(temp_score2)
                    sign_val1 = np.dot(temp_score1,score1)
                    sign_val2 = np.dot(temp_score2, score2)
                    sign1 = np.sign(sign_val1)
                    sign2 = np.sign(sign_val2)
                    if sign1<0:
                        score[:,0] =  -score[:,0]
                    if sign2<0:
                        score[:,1] = -score[:,1]
                    for z in range(1, classNum + 1):
                        class_score = score[class_index_list[z], :]
                        x_ellipse, y_ellipse = confident_ellipse(class_score[:, 0], class_score[:, 1])
                        plt.plot(x_ellipse, y_ellipse, color=CLASS_COLOR[z - 1])
                        plt.fill(x_ellipse, y_ellipse, color=CLASS_COLOR[z - 1], alpha=0.3)
                        class_Xt = score[class_index_list[z], :]
                        plt.scatter(class_Xt[:, 0], class_Xt[:, 1], c=CLASS_COLOR[z - 1], marker=CLASS_LABEL[0],
                                    label='training ' + [k for k,v in class_trans_dict.items() if v == str(z)][0])
                    # calculating the PCA percentage value
                    pU, pS, pV = np.linalg.svd(temp_scaled_half_samples)
                    pca_percentage_val = np.cumsum(pS) / sum(pS)
                    p2_percentage = pca_percentage_val[0] * 100
                    p1_percentage = pca_percentage_val[1] * 100
                    plt.xlabel("PC1(%{0:0.3f}".format(p1_percentage) + ")")
                    plt.ylabel("PC2 (%{0:0.3f}".format(p2_percentage) + ")")
                    plt.rcParams.update({'font.size': 10})
                    plt.legend()
                    plt.savefig(outputPath + '/animation/' + str(picCounter) + '.png')
                    plt.figure().clear()
                    picCounter += 1
        else:
            break

    # start forward selection
    for index in endNumList:
        finalOutPutIdx.append(index)
        temp_selected_all_matrix = scaled_all_samples[:, finalOutPutIdx]
        temp_selected_half_matrix = scaled_half_samples[:, finalOutPutIdx]
        temp_score = calScore(temp_selected_half_matrix, temp_selected_all_matrix)
        newScore = gen_clust.RunClust(temp_score, classList, classNum)
        e_old = round(oldScore, 4)
        e_new = round(newScore, 4)
        if newScore > oldScore:
            oldScore = newScore
            print("ADD    , SCORES [new: old] - ["+ str(e_new) + ":"+str(e_old) + "]" )
            # generate the PCA graph for the first iteration and gather together to form a gif  animation
            if iternum ==0:
                dummyU, dummyS, V = svds(temp_selected_half_matrix, k=2)
                V = V.transpose()
                score = np.dot(temp_selected_all_matrix, V)
                temp_score1 = score[:, 0]
                temp_score1 = np.transpose(temp_score1)
                temp_score2 = score[:, 1]
                temp_score2 = np.transpose(temp_score2)
                sign_val1 = np.dot(temp_score1, score1)
                sign_val2 = np.dot(temp_score2, score2)
                sign1 = np.sign(sign_val1)
                sign2 = np.sign(sign_val2)
                if sign1 < 0:
                    score[:, 0] = -score[:, 0]
                if sign2 < 0:
                    score[:, 1] = -score[:, 1]
                for z in range(1, classNum + 1):
                    class_score = score[class_index_list[z], :]
                    x_ellipse, y_ellipse = confident_ellipse(class_score[:, 0], class_score[:, 1])
                    plt.plot(x_ellipse, y_ellipse, color=CLASS_COLOR[z - 1])
                    plt.fill(x_ellipse, y_ellipse, color=CLASS_COLOR[z - 1], alpha=0.3)
                    class_Xt = score[class_index_list[z], :]
                    plt.scatter(class_Xt[:, 0], class_Xt[:, 1], c=CLASS_COLOR[z - 1], marker=CLASS_LABEL[0],
                                label='training ' + [k for k,v in class_trans_dict.items() if v == str(z)][0])
                # calculating the PCA percentage value
                pU, pS, pV = np.linalg.svd(temp_selected_half_matrix)
                pca_percentage_val = np.cumsum(pS) / sum(pS)
                p2_percentage = pca_percentage_val[0] * 100
                p1_percentage = pca_percentage_val[1] * 100
                plt.xlabel("PC1(%{0:0.3f}".format(p1_percentage) + ")")
                plt.ylabel("PC2 (%{0:0.3f}".format(p2_percentage) + ")")
                plt.rcParams.update({'font.size': 10})
                plt.legend()
                plt.savefig(outputPath + '/animation/' + str(picCounter) + '.png')
                plt.figure().clear()
                picCounter += 1
        elif newScore < oldScore:
            finalOutPutIdx.remove(index)
            print("IGNORED, SCORES [new: old] - ["+ str(e_new) + ":"+str(e_old) + "]" )
    png_dir = outputPath + '/animation/'
    images = []
    for file_num in range(len(sorted(os.listdir(png_dir)))-1):
        file_name = str(file_num)+'.png'
        if file_name.endswith('.png') and file_name != "0.png":
            file_path = os.path.join(png_dir, file_name)
            images.append(imageio.imread(file_path))
    imageio.mimsave(outputPath + '/animation.gif', images)
    shutil.rmtree(png_dir)
    return finalOutPutIdx, sample_training, sample_test, class_training, class_test

# scale samples with the mean and std from previous scaling
# INPUT : all sample data list, mean of previous scaling, stander deviation of previous scaling
# OUTPUT: scaled all sample data
def scale_all_data(samples,mean,std):
    functionTop = np.subtract(samples, mean)
    scaled_samples = np.divide(functionTop, std)
    for list in scaled_samples:
        list[list==inf] = 10**-12
    scaled_samples = np.nan_to_num(scaled_samples, nan=(10**-12))
    return scaled_samples



# scale half of the sample
# INPUT : sample data list
# OUTPUT: scaled  sample data, mean of the sample, stander deviation for the sample
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

# after get all the selected variables we make them a matrix and calculate the mean by using stander normal variate
# INPUT : all sample data list
# OUTPUT: scaled all sample data, the mean of all the variables
def SVN_scale_half_data(samples):

    sd = StandardScaler( with_mean=True, with_std=False)
    sd.fit(samples)
    col_mean = sd.mean_
    scaled_samples = scale(samples, axis=1, with_mean=True, with_std=True)
    return scaled_samples, col_mean

# after get all the selected variables we make them a matrix and calculate the mean by using stander normal variate
# INPUT : all sample data list
# OUTPUT: scaled all sample data, the mean of all the variables
def SVN_scale_all_data(samples,col_mean):
    scaled_samples = scale(samples, axis=1, with_mean=True, with_std=True)
    scaled_samples = np.subtract(scaled_samples, col_mean)
    return scaled_samples

# split the sample data randomly by the rate of spliting (0-1)
# INPUT : sample data list, class list, rate of spliting
# OUTPUT : training data, validation data, training class, validation class, training data index, validation ata index
def selectRandom(sample_list,class_list, howMuchSplit):
    sample_matrix = np.array(sample_list)
    class_matrix = np.array(class_list)
    X_train, X_test, y_train, y_test = train_test_split(sample_matrix, class_matrix, test_size=float(howMuchSplit), stratify=class_matrix)
    return X_train, X_test, y_train, y_test

# calculate the score for cluster resolution
# INPUT : random selected sample data, sample data
# OUTPUT : score
def calScore(rand_variable_list,all_variable_list):
    dummyU,dummyS,V = svds(rand_variable_list, k=2)
    V = np.transpose(V)
    score = np.dot(all_variable_list, V)
    return score

# generate confident ellipse in graph
# INPUT : score one, score two, confident interval
# OUTPUT : x axis confident ellipse, y axis confident ellipse
def confident_ellipse(score1, score2, confident_interval = 0.95):
    score1 = np.array(score1)
    score2 = np.array(score2)
    chi_2 = chi2.ppf(confident_interval, df=2)
    d1 = score1.mean(axis=0)
    d2 = score2.mean(axis=0)
    data = [score1,score2]
    covMat = np.cov(data)
    eivec, eigval, Vh1 = np.linalg.svd(covMat)
    phi1 = math.atan2(eivec[0][1], eivec[0][0])
    if phi1 < 0:
        phi1 = phi1 + 2*math.pi
    theta = np.arange(0, 2*math.pi, 0.01)
    x_ellipse = []
    y_ellipse = []
    for i in theta:
        x_temp = d1 + math.sqrt(chi_2) * math.sqrt(eigval[0]) * math.cos(i) * math.cos(phi1) - math.sqrt(chi_2) * math.sqrt(eigval[1]) * math.sin(i) * math.sin(phi1)
        y_temp = d2 + math.sqrt(chi_2) * math.sqrt(eigval[0]) * math.cos(i) * math.sin(phi1) + math.sqrt(chi_2) * math.sqrt(eigval[1]) * math.sin(i) * math.cos(phi1)
        y_ellipse.append(y_temp)
        x_ellipse.append(x_temp)
    return x_ellipse, y_ellipse
