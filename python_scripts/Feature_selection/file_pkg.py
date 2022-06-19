import pandas as pd
import csv
import os
import numpy as np
import glob
import warnings
import shutil
warnings.filterwarnings('ignore')
# create empty folder to save output data
# INPUT : None
# OUTPUT : None
def create_folder(task_pk):
    OUTPUT_PATH = 'static/images/featureSelection/temp/output/output' + str(task_pk)
    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)
    # Create the needed directory if directory not exist
    if not os.path.exists(OUTPUT_PATH + '/animation'):
        os.makedirs(OUTPUT_PATH + '/animation')
    if not os.path.exists(OUTPUT_PATH + '/rocExternal'):
        os.makedirs(OUTPUT_PATH + '/rocExternal')
    if not os.path.exists(OUTPUT_PATH + '/rocIterations'):
        os.makedirs(OUTPUT_PATH + '/rocIterations')
    if not os.path.exists(OUTPUT_PATH + '/rocTrainFS'):
        os.makedirs(OUTPUT_PATH + '/rocTrainFS')
    if not os.path.exists(OUTPUT_PATH + '/rocTrainNoFS'):
        os.makedirs(OUTPUT_PATH + '/rocTrainNoFS')
    if not os.path.exists(OUTPUT_PATH + '/rocValiFS'):
        os.makedirs(OUTPUT_PATH + '/rocValiFS')
    if not os.path.exists(OUTPUT_PATH + '/rocValiNoFS'):
        os.makedirs(OUTPUT_PATH + '/rocValiNoFS')
    return OUTPUT_PATH


# output csv file content as list by column
# INPUT : file name
# OUTPUT : data list
def getValFromFileByCols(fileName):
    df = pd.read_csv(fileName,header=None)
    row_count, column_count = df.shape
    retData = []
    for col in range(column_count):
        tempData = []
        for row in range(row_count):
            tempData.append(str(df.iloc[row][col]))
        retData.append(tempData)
    return retData


# output csv file content as list by row
# INPUT : file name
# OUTPUT : data list
def getValFromFileByRows(fileName):
    df = pd.read_csv(fileName,header=None)
    row_count, column_count = df.shape
    retData = []
    for row in range(row_count):
        tempData = []
        for col in range(column_count):
            tempData.append(float(df.iloc[row][col]))
        retData.append(tempData)
    return retData

# generate file by the input matrix for sample data
# INPUT: matrix, output file name
# OUTPUT : None
def gen_file_by_matrix(matrix,fileName):
    with open(fileName, 'w', newline='') as f:
        writer = csv.writer(f)
        # write multiple rows
        for row in matrix:
            writer.writerow(row)

# generate file by the input matrix for class data
# INPUT: data header,matrix, output file name
# OUTPUT : None
def gen_file_by_class_matrix(header,matrix,fileName):
    with open(fileName, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        # write multiple rows
        for row in matrix:
            writer.writerow(row)

def gen_file_by_line(header,line,fileName):
    with open(fileName, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        # write multiple rows
        writer.writerow(line)

# generate file by the input matrix by list (one dimension) by row
# INPUT : data header, list, output file name
# OUTPUT : None
def gen_file_by_list(header,list,fileName):
    with open(fileName, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header+list)

# generate file by the input matrix by list (one dimension) by column
# INPUT : data header, list, output file name
# OUTPUT : NOne
def gen_file_by_list_col(header,list,fileName):
    with open(fileName, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerow(list)
# read motaboanalize format csv file
# INPUT : file name
# OUTPUT: sample data, sample name, class data, variable name
def readMotabo(fileName):
    df = pd.read_csv(fileName, header=None)
    row_count, column_count = df.shape
    sampleName = []
    variableName = []
    classList = []
    sampleList = []
    for col in range(1,column_count):
        sampleName.append(str(df.iloc[0][col]))
        classList.append(str(df.iloc[1][col]))
    for row in range(2,row_count):
        variableName.append(str(df.iloc[row][0]))
    for c in range(1, column_count):
        tempData = []
        for r in range(2,row_count):
            tempData.append(float(df.iloc[r][c]))
        sampleList.append(tempData)
    return sampleList, sampleName, classList, variableName

# generate motaboanalize format file
# INPUT : sample data, class data, row index, column index, original class name, sample name, variable name
# OUTPUT : None
def export_file(variable, class_list, indice, hori, fileName, label_dic,sampleName,variableName):
    with open(fileName, 'w', newline='') as f:
        writer = csv.writer(f)
        class_list = np.array(class_list)
        trans_class_list = []
        for i in class_list:
            trans_class_list += [k for k, v in label_dic.items() if v == str(i)]
        # write multiple rows
        sampleName_row = [sampleName[i] for i in indice]
        sampleName_row.insert(0, "")
        writer.writerow(sampleName_row)
        class_row = [trans_class_list[i] for i in indice]
        class_row.insert(0, "Label")
        writer.writerow(class_row)
        variable = np.array(variable)

        variable = variable[:, list(hori)]
        variable = variable[list(indice),:]

        variableName = [variableName[i] for i in hori]
        variable = np.transpose(variable)
        temp_vari = np.ndarray.tolist(variable)
        for i in range(len(temp_vari)):
            temp_vari[i].insert(0,str(variableName[i]))
            writer.writerow(temp_vari[i])
            writer.writerow(temp_vari[i])

def clearGenerateErrorMessage(msgs,path):
    shutil.rmtree(path)
    if not os.path.exists(path):
        os.makedirs(path)
    with open(path + '/ErrorMessage.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        # write multiple rows
        for msg in msgs:
            writer.writerow(msg)


