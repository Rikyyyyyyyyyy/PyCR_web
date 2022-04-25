import numpy as np
import xlrd
import newScore
import pandas as pd
import genStartEndNum2
import sys
from sklearn import svm
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
from sklearn import metrics
from sklearn.decomposition import PCA

def main():
    sample_file_path = sys.argv[1]
    class_file_path = sys.argv[2]
    print(class_file_path)
    task_id = sys.argv[3]
    # get the class list
    classList = getValFromFileByCols(class_file_path)
    classMatrix = np.array(classList)
    # get the max class number as classNum
    classNum = max(classList)
    # get the variable list
    sampleList = getValFromFileByRows(sample_file_path)
    sampleMatrix = np.array(sampleList)
    # get the start number and the end number
    startNum, endNum = genStartEndNum2.gaussian_algorithm(int(classNum), classList, sampleList)
    # create a hash table to take count for the show up times for each variables
    hash_list = [0]*1500
    for k in range(3):
        printStr = "###################################" + str(k)
        print(printStr)
        # getting the selected index
        return_idx, sample_test, class_training, class_test = newScore.setNumber(int(classNum), classList, sampleList, startNum, endNum)

        for j in return_idx:
            hash_list[j] = hash_list[j]+1

        # if k == 0:
        #     valid_idx = return_idx
        # else:
        #     valid_idx = []
        #     # calculate the show-up ratio for each variable
        #     for i in range(len(hash_list)):
        #         prob = float(hash_list[i]) / float(k)
        #         print(prob)
        #         # we are only taking the ratio more than 30%
        #         if prob > 0.9:
        #             valid_idx.append(i)
        #
        # selectedVariables = sampleMatrix[:, valid_idx]

        # generate PCA visualization
        # pca = PCA()
        # Xt = pca.fit_transform(selectedVariables)
        # plot = plt.scatter(Xt[:, 0], Xt[:, 1], c=classList)
        # class_label_list = []
        # for classLabel in range(1, int(classNum)+1):
        #     class_label_list.append(classLabel)
        #
        # plt.legend(handles=plot.legend_elements()[0], labels=class_label_list)
        # plt.show()

        # Create a svm Classifier
        # clf = svm.SVC(kernel='linear',class_weight={1: 10})  # Linear Kernel
        #
        # # Train the model using the training sets
        # clf.fit(selectedVariables, classList)
        #
        # # generate the roc curve
        # metrics.plot_roc_curve(clf, sample_test, class_test)
        # plt.show()

    valid_idx = []
    # calculate the show-up ratio for each variable
    for i in range(len(hash_list)):
        prob = float(hash_list[i])/3.0
        # we are only taking the ratio more than 30%
        print(prob)
        if prob > 0.9:
            valid_idx.append(i)
    print(valid_idx)
    genfile(valid_idx, sample_file_path, task_id)

# generate file of variables by the variable index
def genfile(indexList, fileName,task_id):
    wb = xlrd.open_workbook(fileName)
    # select the first sheet from xlsx file
    sheet = wb.sheet_by_index(0)

    first_col = sheet.col_values(indexList[0])
    df = pd.DataFrame(first_col)
    for i in range(1, len(indexList)):
        col = sheet.col_values(indexList[i])
        new_df = pd.DataFrame(col)
        df = pd.concat([df, new_df], axis=1)
    output_name = 'static/images/featureSelection/out/output' + task_id + '.xlsx'
    writer = pd.ExcelWriter(output_name, engine='xlsxwriter')
    df.to_excel(writer, index=False, header=None)

# get the list of samples from the original file
def getValFromFileByRows(fileName):
    wb = xlrd.open_workbook(fileName)
    # select the first sheet from xlsx file
    sheet = wb.sheet_by_index(0)
    samples = []
    # add all the variables in cluster into the variables list
    for i in range(0, sheet.nrows):
        temp_col1 = []
        for z in range(0, sheet.ncols):
            temp_col1.append(float(sheet.cell_value(i, z)))
        samples.append(temp_col1)
    return samples

def getValFromFileByCols(fileName):
    wb = xlrd.open_workbook(fileName)
    # select the first sheet from xlsx file
    sheet = wb.sheet_by_index(0)
    samples = []
    # add all the variables in cluster into the variables list
    for z in range(0, sheet.ncols):
        temp_col1 = []
        for i in range(0, sheet.nrows):
            temp_col1.append(float(sheet.cell_value(i, z)))
        samples.append(temp_col1)
    if sheet.ncols == 1:
        return samples[0]
    else:
        return samples
main()
