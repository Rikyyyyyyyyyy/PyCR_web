import pandas as pd
import csv
import os
import numpy as np
import warnings
import shutil
from io import BytesIO
import urllib.request
from fpdf import FPDF
import awswrangler as wr
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
    if not os.path.exists(OUTPUT_PATH + '/roc_curve/rocIterations'):
        os.makedirs(OUTPUT_PATH + '/roc_curve/rocIterations')
    if not os.path.exists(OUTPUT_PATH + '/roc_curve'):
        os.makedirs(OUTPUT_PATH + '/roc_curve')
    if not os.path.exists(OUTPUT_PATH + '/roc_curve'):
        os.makedirs(OUTPUT_PATH + '/roc_curve')
    if not os.path.exists(OUTPUT_PATH + '/PCA/pca_graph'):
        os.makedirs(OUTPUT_PATH + '/pca/pca_graph')
    if not os.path.exists(OUTPUT_PATH + '/PCA/biplot_graph'):
        os.makedirs(OUTPUT_PATH + '/pca/biplot_graph')
    if not os.path.exists(OUTPUT_PATH + '/PCA/loading_plot'):
        os.makedirs(OUTPUT_PATH + '/pca/loading_plot')
    if not os.path.exists(OUTPUT_PATH + '/selected_variable'):
        os.makedirs(OUTPUT_PATH + '/selected_variable')
    if not os.path.exists(OUTPUT_PATH + '/additional_information'):
        os.makedirs(OUTPUT_PATH + '/additional_information')
    if not os.path.exists(OUTPUT_PATH + '/matlab_plot'):
        os.makedirs(OUTPUT_PATH + '/matlab_plot')
    return OUTPUT_PATH



# output csv file content as list by column
# INPUT : file name (csv file)
# OUTPUT : data list
def getValFromFileByCols(fileName):
    full_path_filename = 'https://' + 'pycr' + '.s3.us-east-2.amazonaws.com/' + fileName
    file = urllib.request.urlopen(full_path_filename)
    if '.xlsx' in fileName:
        df = pd.read_excel(full_path_filename, header=None)
    if '.csv' in fileName:
        df = pd.read_csv(file,header=None)
    row_count, column_count = df.shape
    retData = []
    for col in range(column_count):
        tempData = []
        for row in range(row_count):
            tempData.append(str(df.iloc[row][col]))
        retData.append(tempData)
    return retData


# output csv file content as list by row
# INPUT : file name (csv file)
# OUTPUT : data list
def getValFromFileByRows(fileName):
    full_path_filename = 'https://' + 'pycr' + '.s3.amazonaws.com/' + fileName
    file = urllib.request.urlopen(full_path_filename)
    if '.xlsx' in fileName:
        df = pd.read_excel(full_path_filename, header=None)
    if '.csv' in fileName:
        df = pd.read_csv(file,header=None)
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
    full_path_filename = 'https://' + 'pycr' + '.s3.amazonaws.com/' + fileName
    file = urllib.request.urlopen(full_path_filename)
    if fileName.lower().endswith(".xlsx"):
        df = pd.read_excel(full_path_filename, header=None)
    if fileName.lower().endswith(".csv"):
        df = pd.read_csv(file,header=None)
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
        sampleName_row.insert(1,"")
        writer.writerow(sampleName_row)
        class_row = [trans_class_list[i] for i in indice]
        class_row.insert(0, "position")
        class_row.insert(1, "Label")
        writer.writerow(class_row)
        variable = np.array(variable)

        variable = variable[:, list(hori)]
        variable = variable[list(indice),:]

        variableName = [variableName[i] for i in hori]
        variableIndex = [i+1 for i in hori]
        variable = np.transpose(variable)
        temp_vari = np.ndarray.tolist(variable)
        for i in range(len(temp_vari)):
            temp_vari[i].insert(0,str(variableIndex[i]))
            temp_vari[i].insert(1,str(variableName[i]))
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


def gen_overview_report(path,selected_variables):
    pdf = FPDF()
    # Add a page
    pdf.add_page()

    # set style and size of font
    # that you want in the pdf
    
    # create a cell
    pdf.set_font("Arial",'B', size = 20)
    pdf.cell(200, 10, txt = "Overview Report",
            ln = 2, align = 'C')
    ## PCA graphs 
    pdf.set_font("Arial",'B', size = 10)
    pdf.cell(200, 10, txt = '1) PCA before Feature Selection ',
        ln = 1, align = 'L')
    pdf.image(path+'/pca/pca_graph/PCA_before_FS.png',x=10,y=40,w=84,h=70)
    pdf.image(path+'/pca/biplot_graph/biplot_before_FS.png',x=120,y=40,w=84,h=70)
    # used to make white space for picture to fit in the roght position
    for i in range(8):
        pdf.cell(200, 10, txt = '',
        ln = 1, align = 'L')
    pdf.cell(200, 10, txt = '2) PCA after Feature Selection ',
        ln = 1, align = 'L')
    pdf.image(path+'/pca/pca_graph/PCA_after_FS.png',x=10,y=130,w=84,h=70)
    pdf.image(path+'/pca/biplot_graph/biplot_after_FS.png',x=120,y=130,w=84,h=70)
    # used to make white space for picture to fit in the roght position
    for i in range(8):
        pdf.cell(200, 10, txt = '',
        ln = 1, align = 'L')
     ## Selected variables 
    pdf.set_font("Arial",'B', size = 10)
    pdf.cell(200, 10, txt = '3) Selected Variables',
        ln = 1, align = 'L')
    pdf.set_font("Arial", size = 10)
    th = pdf.font_size
    for row in selected_variables:
        pdf.cell(20, 2*th, "")
        for datum in row:
            # Enter data in colums
            pdf.cell(40, 2*th, str(datum), border=1)
        pdf.ln(2*th)
    # used to make white space for picture to fit in the roght position
    for i in range(8):
        pdf.cell(200, 10, txt = '',
        ln = 1, align = 'L')
    outputPath = path+"/overview_report"+".pdf"
    pdf.output(outputPath,'F')  

def gen_detail_report(path,selected_variables):
    pdf = FPDF()
    # Add a page
    pdf.add_page()

    # set style and size of font
    # that you want in the pdf
    
    # create a cell
    pdf.set_font("Arial",'B', size = 20)
    pdf.cell(200, 10, txt = "Detail Report",
            ln = 2, align = 'C')
    ## PCA graphs 
    pdf.set_font("Arial",'B', size = 10)
    pdf.cell(200, 10, txt = '1) PCA before Feature Selection ',
        ln = 1, align = 'L')
    pdf.image(path+'/pca/pca_graph/PCA_before_FS.png',x=10,y=40,w=84,h=70)
    pdf.image(path+'/pca/biplot_graph/biplot_before_FS.png',x=120,y=40,w=84,h=70)
    # used to make white space for picture to fit in the roght position
    for i in range(8):
        pdf.cell(200, 10, txt = '',
        ln = 1, align = 'L')
    pdf.cell(200, 10, txt = '2) PCA after Feature Selection ',
        ln = 1, align = 'L')
    pdf.image(path+'/pca/pca_graph/PCA_after_FS.png',x=10,y=130,w=84,h=70)
    pdf.image(path+'/pca/biplot_graph/biplot_after_FS.png',x=120,y=130,w=84,h=70)
    # used to make white space for picture to fit in the roght position
    for i in range(8):
        pdf.cell(200, 10, txt = '',
        ln = 1, align = 'L')
    ## Selected variables 
    pdf.set_font("Arial",'B', size = 10)
    pdf.cell(200, 10, txt = '3) Selected Variables',
        ln = 1, align = 'L')
    pdf.set_font("Arial", size = 10)
    th = pdf.font_size
    for row in selected_variables:
        pdf.cell(20, 2*th, "")
        for datum in row:
            # Enter data in colums
            pdf.cell(40, 2*th, str(datum), border=1)
        pdf.ln(2*th)

    ## new content for detail report
    pdf.add_page()
    ## ROC graphs 
    pdf.set_font("Arial",'B', size = 10)
    pdf.cell(200, 10, txt = '4) ROC Iterations graph ',
        ln = 1, align = 'L')
    pdf.set_font("Arial",'B', size = 7)
    pdf.cell(200, 10, txt = '   **Depend on how many iterations you have, the color start at red and tend to be blue when the interation goes.',
        ln = 1, align = 'L')
    pdf.image(path+'/roc_curve/rocIterations/rocIterations.png',x=50,y=30,w=84,h=70)

    # used to make white space for picture to fit in the roght position
    for i in range(8):
        pdf.cell(200, 10, txt = '',
        ln = 1, align = 'L')

    ## Loading plots
    pdf.set_font("Arial",'B', size = 10)
    pdf.cell(200, 10, txt = '5) Loading Plots before FS',
        ln = 1, align = 'L')
    pdf.image(path+'/pca/loading_plot/loading_before_FS_PC1.png',x=10,y=130,w=84,h=70)
    pdf.image(path+'/pca/loading_plot/loading_before_FS_PC2.png',x=120,y=130,w=84,h=70)
    for i in range(9):
        pdf.cell(200, 10, txt = '',
        ln = 1, align = 'L')
    pdf.cell(200, 10, txt = '5) Loading Plots after FS',
        ln = 1, align = 'L')
    pdf.set_font("Arial",'B', size = 7)
    pdf.image(path+'/pca/loading_plot/loading_after_FS_PC1.png',x=10,y=220,w=84,h=70)
    pdf.image(path+'/pca/loading_plot/loading_after_FS_PC2.png',x=120,y=220,w=84,h=70)

    ## new content for detail report
    pdf.add_page()
    ## Loading plots
    pdf.set_font("Arial",'B', size = 10)
    pdf.cell(200, 10, txt = '6) Start and Stop number ',
        ln = 1, align = 'L')
    pdf.set_font("Arial",'B', size = 7)
    pdf.image(path+'/additional_information/startStopNum.png',x=50,y=30,w=84,h=70)
    

    ## output the report as pdf 
    outputPath = path+"/detail_report"+".pdf"
    pdf.output(outputPath,'F') 

def gen_matlab_plot(data,sampleName,classList,variableName,path):
    with open(path+'/matlab_plot/sampleName.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        # write multiple rows
        for sn in sampleName:
            writer.writerow([sn])

    with open(path+'/matlab_plot/Y_block.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        # write multiple rows
        for cl in classList:
            writer.writerow([str(cl)])

    with open(path+'/matlab_plot/variableName.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        # write multiple rows
        writer.writerow(variableName)
    
    with open(path+'/matlab_plot/X_block.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        # write multiple rows
        for d in data:
            writer.writerow(d)

    

