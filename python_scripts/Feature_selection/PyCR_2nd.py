
import sys
import copy
import math
import warnings
import matplotlib
import xlsxwriter
import numpy as np
import pandas as pd 
from enum import auto
from numpy import inf
from pydoc import plain
from sklearn import svm
from colour import Color
from sklearn import metrics
import matplotlib.pyplot as plt
from sklearn import preprocessing
from scipy.sparse.linalg import svds
from bioinfokit.visuz import cluster
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale
from sklearn.metrics import roc_curve, auc
from scipy.stats.distributions import chi2
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import label_binarize
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
from sklearn.multiclass import OneVsRestClassifier
from sklearn.model_selection import train_test_split
from python_scripts.Feature_selection import newScore
from python_scripts.Feature_selection import file_pkg
from python_scripts.Feature_selection import genStartEndNum2
from sklearn.metrics import accuracy_score,precision_score,recall_score
matplotlib.use('agg')
warnings.filterwarnings('ignore')

def mainPyCR(isexternal,splitRatio,isMicro,tupaType,isMotabo,MotaboFileName,DataFileName,ClassFileName,sampleNameFile,variableNameFile,external_type,ex_isMotabo, ex_MotaboFileName,ex_DataFileName,ex_ClassFileName,ex_sampleNameFile,ex_variableNameFile, scale_type,norm_type,iteration,survivalRate,V_rankingAlgorithm, nComponent,task_pk):
    # Iterations for feature selection 
    ITERATION = iteration

    # create a normalization objects 
    NORM = Normalization()

    # generate roc color for ROC curve
    RED = Color("#dc3c40")
    ROC_COLOR = list(RED.range_to(Color("#55a6bc"), ITERATION + 1))

    # set class color list
    CLASS_COLOR = ["#dc3c40", "#55a6bc", 'purple', 'yellowgreen', 'wheat', 'royalblue', '#42d7f5', '#ca7cf7', '#d2f77c']
    CLASS_LABEL = ["o", "x", "4", "*", "+", "D", "8", "s", "p"]

    # create the needed folder to save ouput data
    # read data from input files
    OUTPUT_PATH = file_pkg.create_folder(task_pk)

    

    # read Internal data from input file 
    if isMotabo:
        sampleList, sampleName, classList, variableName =file_pkg.readMotabo(MotaboFileName)
    else:
        classList = file_pkg.getValFromFileByCols(ClassFileName)[0]
        sampleList = file_pkg.getValFromFileByRows(DataFileName)
        sampleName = file_pkg.getValFromFileByCols(sampleNameFile)[0]
        variableName = file_pkg.getValFromFileByCols(variableNameFile)
    
    
    # external file split in 2 ways 
        #1 input a external file directly 
        #2 aplit file from sample file by given ratio
    if isexternal:
        if external_type == 'file':
            if ex_isMotabo:
                externalList, externalSampleName, externalClassList, externalVariableName =file_pkg.readMotabo(ex_MotaboFileName)
            else:
                externalClassList = file_pkg.getValFromFileByCols(ex_ClassFileName)[0]
                externalList = file_pkg.getValFromFileByRows(ex_DataFileName)
                externalSampleName = file_pkg.getValFromFileByCols(ex_sampleNameFile)[0]
                externalVariableName = file_pkg.getValFromFileByCols(ex_variableNameFile)
            index_indices = [x for x in range(len(externalClassList))]
        elif external_type == 'split':
            sampleList, externalList, classList, externalClassList, indices_train, index_indices = selectRandom(sampleList,classList,splitRatio)
    else:
        index_indices = [x for x in range(len(classList))]
    
    # get the class number from class name
    # generate number version of class name
    unique_class = set(classList)
    unique_class = sorted(list(unique_class))
    classNum = len(unique_class)
    class_trans_dict = {}
    for i in range(classNum):
        class_trans_dict[unique_class[i].replace(" ","").replace("/","-")] = str(i+1)
    classList = [class_trans_dict[sub.replace(" ","").replace("/","-")]for sub in classList]
    classList = [int(x) for x in classList]
    # create label list for plot
    class_num_label = [ i for i in range(1, classNum + 1)]

    if isexternal:
        externalClassList = [class_trans_dict[sub.replace(" ","").replace("/","-")]for sub in externalClassList]
        externalClassList = [int(x) for x in externalClassList]

    file_pkg.export_file(sampleList, classList, [i for i in range(len(sampleList))], [i for i in range(len(variableName))], OUTPUT_PATH +'/additional_information/original_file.csv', class_trans_dict,sampleName,variableName)


    # group different sample index by different class
    class_index_list = []
    external_class_index_list = []
    for i in range(classNum+1):
        class_index_list.append([])
    for i in range(len(classList)):
        class_index_list[classList[i]].append(i)
    if isexternal:
        for i in range(classNum+1):
            external_class_index_list.append([])
        for i in range(len(externalClassList)):
            external_class_index_list[externalClassList[i]].append(i)
    
    # Normalization & Scaling & Tupa for Internal Data  
    sampleList = NORM.func_dict[tupaType](sampleList,classList)
    sampleList = NORM.func_dict[scale_type](sampleList)
    sampleList = NORM.func_dict[norm_type](sampleList)

    # Normalization & Scaling & Tua for External Data 
    if isexternal:
        externalList = NORM.func_dict[tupaType](externalList,externalClassList)
        externalList = NORM.func_dict[scale_type](externalList)
        externalList = NORM.func_dict[norm_type](externalList) 

    # Genrate  PCA graph with no Feature selection 

    
    if isexternal:
        if classNum == 2:
            gen_roc_graph(externalList,externalClassList,externalList,externalClassList,OUTPUT_PATH + "/roc_curve/roc_before_FS.png")
        else:
            mul_roc_graph(classNum,class_num_label,externalClassList,externalClassList,externalList,externalList,ROC_COLOR,OUTPUT_PATH + "/roc_curve/roc_before_FS.png ",isMicro, class_trans_dict)
        gen_pca(externalList,classNum,external_class_index_list,CLASS_COLOR, CLASS_LABEL,OUTPUT_PATH +  '/PCA/pca_graph/PCA_before_FS.png', class_trans_dict)
        gen_biplot_loading(externalList,classNum,external_class_index_list,OUTPUT_PATH+'/PCA/biplot_graph/biplot_before_FS.png',OUTPUT_PATH+'/PCA/loading_plot/loading_before_FS')
        gen_stat_report(externalList,externalClassList,OUTPUT_PATH+'/additional_information/staticReport_before_FS.csv') 
        file_pkg.gen_matlab_plot(externalList,externalSampleName,externalClassList,externalVariableName,OUTPUT_PATH)  
    else:
        gen_pca(sampleList,classNum,class_index_list,CLASS_COLOR, CLASS_LABEL,OUTPUT_PATH +  '/PCA/pca_graph/PCA_before_FS.png', class_trans_dict)
        gen_biplot_loading(sampleList,classNum,class_index_list,OUTPUT_PATH+'/PCA/biplot_graph/biplot_before_FS.png',OUTPUT_PATH+'/PCA/loading_plot/loading_before_FS')
        gen_stat_report(sampleList,classList,OUTPUT_PATH+'/additional_information/staticReport_before_FS.csv')  
        file_pkg.gen_matlab_plot(sampleList,sampleName,classList,variableName,OUTPUT_PATH)
        if classNum == 2:
            gen_roc_graph(sampleList,classList,sampleList,classList,OUTPUT_PATH + "/roc_curve/roc_before_FS.png")
        else:
            mul_roc_graph(classNum,class_num_label,classList,classList,sampleList,sampleList,ROC_COLOR,OUTPUT_PATH + "/roc_curve/roc_before_FS.png ",isMicro, class_trans_dict)
    
    # get the start number and the end number
    startNum, endNum = genStartEndNum2.gaussian_algorithm(int(classNum), classList,sampleList,  V_rankingAlgorithm,nComponent,OUTPUT_PATH )


    # create a list of plot when there are more than 2 classes
    # create a AUC number list to collect all the AUC numbers during the iterations
    figPlot = []
    if classNum == 2 or isMicro:
        auc_table = []
    else:
        auc_table = []
        for i in range(classNum+1):
            figPlot.append(plt.subplots(1))
            auc_table.append([])
    # create a hash table to take count for the show up times for each variables
    hash_list = [0]*(len(sampleList[0]))
    # start Iterations
    erro_iterations = 0
    error_msg = []
    for k in range(ITERATION):
        if erro_iterations < ceil(ITERATION, 2):
            print("################## ITERATION "+ str(k)+" ##################")
            try:
                # Start Feature Selection
                return_idx, sample_taining, sample_test, class_training, class_test = newScore.setNumber(int(classNum), classList, sampleList, startNum, endNum, splitRatio,k, class_trans_dict, scale_type, V_rankingAlgorithm, nComponent,OUTPUT_PATH)
                # calculate the probability of selection for each variables
                # valid index is the probability of variable that over the survival rate
                for j in return_idx:
                    hash_list[j] = hash_list[j]+1
                if k == 0:
                    valid_idx = return_idx
                else:
                    valid_idx = []
                    # calculate the show-up ratio for each variable
                    for i in range(len(hash_list)):
                        prob = float(hash_list[i])/float(k+1)
                        # we are only taking the ratio more than 30%
                        if prob >= survivalRate:
                            valid_idx.append(i)

                selectedVariables = sample_taining[:, valid_idx]
                # Train and predict the class
                clf = svm.SVC(kernel='linear', random_state=0, probability=True)
                clf.fit(selectedVariables, class_training)
                class_pred = clf.predict(sample_test[:, valid_idx])
                classofic_report = classification_report(class_test, class_pred)
                report_lines = classofic_report.split('\n')
                report_lines = report_lines[2:]
                # generate the ROC curve
                if classNum == 2:
                    class_pred = clf.predict_proba(sample_test[:, valid_idx])
                    class_pred = class_pred[:, 1]
                    auc_num = metrics.roc_auc_score(class_test, class_pred)
                    auc_table.append(auc_num)
                    fpr, tpr, _ = metrics.roc_curve(class_test, class_pred, pos_label=2)
                    plt.plot(fpr, tpr, color=str(ROC_COLOR[k]))
                    plt.rcParams.update({'font.size': 10})
                    # plt.title('ROC ' + str(ITERATION) + ' iterations')
                else:
                    training_class = label_binarize(class_training, classes=class_num_label)
                    predict_class = label_binarize(class_test, classes=class_num_label)
                    classifier = OneVsRestClassifier(
                        svm.SVC(kernel="linear", probability=True, random_state=0)
                    )
                    y_score = classifier.fit(selectedVariables, training_class).decision_function(sample_test[:,valid_idx])

                    # Compute ROC curve and ROC area for each class
                    fpr = dict()
                    tpr = dict()
                    roc_auc = dict()
                    for i in range(classNum):
                        fpr[i], tpr[i], _ = metrics.roc_curve(predict_class[:, i], y_score[:, i])
                        roc_auc[i] = auc(fpr[i], tpr[i])
                    # Compute micro-average ROC curve and ROC area
                    fpr["micro"], tpr["micro"], _ = roc_curve(predict_class.ravel(), y_score.ravel())
                    roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])

                    if isMicro:
                        plt.plot(
                            fpr["micro"],
                            tpr["micro"],
                            label=" (area = {0:0.2f})".format(roc_auc["micro"]),
                            color=str(ROC_COLOR[k]),
                        )
                        auc_table.append(roc_auc["micro"])
                        plt.rcParams.update({'font.size':10 })
                        # plt.title('ROC ' + str(ITERATION) + ' iterations')
                    else:
                        for i in range(classNum):
                            auc_table[i].append(roc_auc[i])
                            figPlot[i][1].plot(
                                fpr[i],
                                tpr[i],
                                color=str(ROC_COLOR[k]),
                            )
                        plt.rcParams.update({'font.size': 10})
                plt.rcParams.update({'font.size': 10})
            except Exception as e:
                k -= 1
                erro_iterations += 1
                error_msg.append(e)
                pass
        else:
            badRankingErrorMessage(OUTPUT_PATH)
            return
    # save the roc graph for N iterations
    if classNum ==2 or isMicro:
        plt.savefig(OUTPUT_PATH + '/roc_curve/rocIterations/rocIterations.png')
        plt.figure().clear()
    else:
        for i in range(classNum):
            # figPlot[i][1].set_title('Roc ' + str(ITERATION) + ' iterations class: ' + [k for k, v in class_trans_dict.items() if v == str(i+1)][0])
            figPlot[i][0].savefig(OUTPUT_PATH + '/roc_curve/rocIterations/roc '+str(ITERATION) +'iterations class: '+[k for k,v in class_trans_dict.items() if v == str(i+1)][0]+'.png')
            figPlot[i][0].clear()
    # save all the auc number in to csv table
    if classNum == 2 or isMicro:
        file_pkg.gen_file_by_list(["Auc Number"],auc_table,OUTPUT_PATH + '/roc_curve/rocIterations/auc_interations_table.csv')
    else:
        for j in range(classNum):
            file_pkg.gen_file_by_list(["Auc Number"],auc_table[i],OUTPUT_PATH + '/roc_curve/rocIterations/auc_table_class_' + [k for k,v in class_trans_dict.items() if v == str(j+1)][0] + '.csv')

    valid_idx = []
    # calculate the show-up ratio for each variable
    for i in range(len(hash_list)):
        prob = float(hash_list[i])/ITERATION
        # we are only taking the ratio more than 30%
        if prob >= survivalRate:
            valid_idx.append(i)

    # If there is no enought valid variable selected, return error message 
    if len(valid_idx) < 2:
        notEnoughtSelectedVariableErrorMessage(hash_list, survivalRate, variableName, ITERATION, OUTPUT_PATH)
        return

    # generate selected variable file 
    if isexternal:
        file_pkg.export_file(externalList, externalClassList, index_indices, valid_idx,
                             OUTPUT_PATH + '/selected_variable/selected_variables.csv', class_trans_dict, sampleName,
                             variableName)
    else:
        file_pkg.export_file(sampleList, classList, index_indices, valid_idx,
                             OUTPUT_PATH + '/selected_variable/selected_variables.csv', class_trans_dict, sampleName,
                             variableName)
    # generate PCA graph after Feature selection
    if isexternal:
        if classNum == 2:
            gen_roc_graph(externalList[:,valid_idx],externalClassList,externalList[:,valid_idx],externalClassList,OUTPUT_PATH + "/roc_curve/roc_after_FS.png")
        else:
            mul_roc_graph(classNum,class_num_label,externalClassList,externalClassList,externalList[:, valid_idx],externalList[:, valid_idx],ROC_COLOR,OUTPUT_PATH + "/roc_curve/roc_after_FS.png ",isMicro, class_trans_dict)
        gen_pca(externalList[:, valid_idx], classNum, external_class_index_list, CLASS_COLOR, CLASS_LABEL,
                OUTPUT_PATH + '/PCA/pca_graph/PCA_after_FS.png',class_trans_dict)
        gen_biplot_loading(externalList[:, valid_idx],classNum,external_class_index_list,OUTPUT_PATH+'/PCA/biplot_graph/biplot_after_FS.png',OUTPUT_PATH+'/PCA/loading_plot/loading_after_FS')
        gen_stat_report(externalList[:, valid_idx],externalClassList,OUTPUT_PATH+'/additional_information/staticReport_after_FS.csv') 
        if external_type == 'file':
            file_pkg.export_file(externalList, externalClassList,index_indices, valid_idx, OUTPUT_PATH +'/additional_information/selected_variable.csv', class_trans_dict,externalSampleName,externalVariableName)
        else:
            file_pkg.export_file(externalList, externalClassList,[i for i in range(len(externalClassList))], valid_idx, OUTPUT_PATH +'/additional_information/selected_variable.csv', class_trans_dict,externalSampleName,externalVariableName)

    else:
        if classNum == 2:
            gen_roc_graph(sampleList[:, valid_idx],classList,sampleList[:, valid_idx],classList,OUTPUT_PATH + "/roc_curve/roc_after_FS.png")
        else:
            mul_roc_graph(classNum,class_num_label,classList,classList,sampleList[:, valid_idx],sampleList[:, valid_idx],ROC_COLOR,OUTPUT_PATH + "/roc_curve/roc_after_FS.png ",isMicro, class_trans_dict)
        gen_biplot_loading(sampleList[:,valid_idx],classNum,class_index_list,OUTPUT_PATH+'/PCA/biplot_graph/biplot_after_FS.png',OUTPUT_PATH+'/PCA/loading_plot/loading_after_FS')
        gen_pca(sampleList[:,valid_idx],classNum,class_index_list,CLASS_COLOR, CLASS_LABEL,OUTPUT_PATH +  '/PCA/pca_graph/PCA_after_FS.png', class_trans_dict)
        gen_stat_report(sampleList[:, valid_idx],classList,OUTPUT_PATH+'/additional_information/staticReport_after_FS.csv') 
        file_pkg.export_file(sampleList, classList, [i for i in range(len(sampleList))], valid_idx, OUTPUT_PATH +'/additional_information/selected_variable.csv', class_trans_dict,sampleName,variableName)

    pdf_report_variables =[]
    for indx in valid_idx:
        v_name = variableName[indx]
        temp = [str(indx+3),v_name]
        pdf_report_variables.append(temp)
    file_pkg.gen_overview_report(OUTPUT_PATH,pdf_report_variables)
    file_pkg.gen_detail_report(OUTPUT_PATH,pdf_report_variables)

def gen_biplot_loading(data,classNum,class_index_list,fileName_bi, fileName_lo):
    pca = PCA(n_components=2)
    pca_laodings = PCA(n_components=2)
    score_loading = pca_laodings.fit(data) 
    score = pca.fit_transform(data)
    plt.scatter(score[:,0], score[:,1], color='b')
    loadings = pca_laodings.components_
    loadings = loadings
    plt.scatter(loadings[0]*500,loadings[1]*500, color='r')

    # Add the axis labels
    plt.xlabel('PC 1 (%.2f%%)' % (pca.explained_variance_ratio_[0]*100))
    plt.ylabel('PC 2 (%.2f%%)' % (pca.explained_variance_ratio_[1]*100)) 

    # Done
    plt.savefig(fileName_bi,bbox_inches="tight")
    plt.figure().clear()

    # generate loading graph for PC1
    variable_idx = [i+1 for i in range(len(data[0]))]

    plt.scatter(variable_idx,loadings[0],Color='b')
    # Add the axis labels
    plt.xlabel('Variable index')
    plt.ylabel('PC 1 (%.2f%%)' % (pca.explained_variance_ratio_[1]*100)) 

    # Done
    plt.savefig(fileName_lo+'_PC1.png',bbox_inches="tight")
    plt.figure().clear()

    # generate loading plot for PC2
    variable_idx = [i+1 for i in range(len(data[0]))]

    plt.scatter(variable_idx,loadings[1],Color='b')
    # Add the axis labels
    plt.xlabel('Variable index')
    plt.ylabel('PC 2 (%.2f%%)' % (pca.explained_variance_ratio_[1]*100)) 

    # Done
    plt.savefig(fileName_lo+'_PC2.png',bbox_inches="tight")
    plt.figure().clear()

        
# generate STAT report 
def gen_stat_report(data,classList,fileName):
    clf_FS = svm.SVC(kernel='linear', random_state=42, probability=True)
    clf_FS.fit(data, classList)
    class_pred = clf_FS.predict(data)
    internal_stat_acc_w_FS = accuracy_score(classList, class_pred)
    internal_stat_sel_w_FS = precision_score(classList, class_pred, average='micro')
    internal_stat_sen_w_FS = recall_score(classList, class_pred, average='micro')
    file_pkg.gen_file_by_line(["Selectivity", "Sensitivity", "Accuracy"],
                                      [internal_stat_sel_w_FS, internal_stat_sen_w_FS, internal_stat_acc_w_FS],
                                      fileName)

# generate PCA graph
# INPUT : training data, number of class, class index list, class color list, class label list, name of the output file, original class name
# OUTPUT : None
def gen_pca(sampleData,classNum,class_index_list,class_color,class_label,fileName,class_trans_dict):
    pca = PCA(n_components=2)
    score = pca.fit_transform(sampleData)
    dummyU, dummyS, V = svds(sampleData, k=2)
    V = np.transpose(V)
    score = np.dot(sampleData, V)
    for z in range(1, classNum + 1):
        class_score = score[class_index_list[z], :]
        x_ellipse, y_ellipse = confident_ellipse(class_score[:, 0], class_score[:, 1])
        plt.plot(x_ellipse, y_ellipse, color=class_color[z - 1])
        plt.fill(x_ellipse, y_ellipse, color=class_color[z - 1], alpha=0.3)
        plt.scatter(class_score[:, 0], class_score[:, 1], c=class_color[z - 1],
                    marker=class_label[0], label= [k for k,v in class_trans_dict.items() if v == str(z)][0])
    # calculating the PCA percentage value
    pU, pS, pV = np.linalg.svd(sampleData)
    pca_percentage_val = np.cumsum(pS) / sum(pS)
    p2_percentage = pca_percentage_val[0] * 100
    p1_percentage = pca_percentage_val[1] * 100
    # Add the axis labels
    plt.xlabel('PC 1 (%.2f%%)' % (pca.explained_variance_ratio_[0]*100))
    plt.ylabel('PC 2 (%.2f%%)' % (pca.explained_variance_ratio_[1]*100)) 
    # plt.title(graph_title)
    plt.rcParams.update({'font.size': 10})
    plt.legend(loc="upper right",prop={'size': 5})
    plt.savefig(fileName,bbox_inches="tight")
    plt.figure().clear()

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


def selectRandom(sample_list,class_list,howMuchSplit):
    indices = np.arange(1,len(class_list)+1)
    sample_matrix = np.array(sample_list)
    class_matrix = np.array(class_list)
    X_train, X_test, y_train, y_test, indices_train, indices_test = train_test_split(sample_matrix, class_matrix, indices, test_size=float(howMuchSplit), stratify=class_matrix)
    return X_train, X_test, y_train, y_test, indices_train, indices_test

def notEnoughtSelectedVariableErrorMessage(hash_list,survivalRate,variableName,iterations,path):
    hash_list = list(map(lambda x: x/iterations, hash_list))
    sorted_index = [i[0] for i in sorted(enumerate(hash_list), key=lambda x: x[1])]
    sorted_index.reverse()
    return_str = []
    return_str.append("Sorry, the survival rate your pick is not work, here is the top five variable survival rate:\n")
    for i in range(5):
        return_str .append ("[" + variableName[sorted_index[i]][0] +":" + str(hash_list[sorted_index[i]]) +"]\n")
    return_str.append( "We suggest you pick a survival rate lower than above.\n")
    file_pkg.clearGenerateErrorMessage(return_str,path)

def badRankingErrorMessage(path):
    file_pkg.clearGenerateErrorMessage(['Indeterminate start number. Please select a different variable ranking metric.'], path)

def ceil(a, b):
    return -1 * (-a // b)

# generate ROC graph for data set have 2 classes
# INPUT : training data, training class, predict data, predict class, name of the output file, title of the graph
# OUTPUT : None
def gen_roc_graph(training_sample,training_class,predict_sample,predict_class, fileName):
    # Create a svm Classifier
    clf = svm.SVC(kernel='linear', random_state=0, probability=True)  # Linear Kernel
    # Train the model using the training sets
    clf.fit(training_sample, training_class)
    class_pred = clf.predict_proba(predict_sample)
    class_pred = class_pred[:, 1]
    auc_external = metrics.roc_auc_score(predict_class, class_pred)
    fpr, tpr, _ = metrics.roc_curve(predict_class, class_pred, pos_label=2)
    plt.plot(fpr, tpr, label="(area = {0:0.3f})".format(auc_external))
    # plt.title(graph_title)
    plt.rcParams.update({'font.size': 14})
    plt.legend(loc="upper right",prop={'size': 5})
    plt.savefig(fileName,bbox_inches="tight")
    plt.figure().clear()

# generate ROC graph for data set more than 2 classes
# INPUT : class number, label of class number, training classes, predict classes, training data, predict data, color list for the roc graph, is Micro ROC, title of the graph, original class name
# OUTPUT : None
def mul_roc_graph(classNum, class_num_label, trainingClass, predicClass, trainingVal, predicVal, roc_colors, output_filename,isMicro,class_trans_dict):
    figPlots = []
    for w in range(classNum):
        figPlots.append(plt.subplots(1))
    training_class = label_binarize(trainingClass, classes=class_num_label)
    predict_class = label_binarize(predicClass, classes=class_num_label)
    classifier = OneVsRestClassifier(
        svm.SVC(kernel="linear", probability=True, random_state=0)
    )
    y_score = classifier.fit(trainingVal, training_class).decision_function(
        predicVal)

    # Compute ROC curve and ROC area for each class
    fpr = dict()
    tpr = dict()
    roc_auc = dict()
    for i in range(classNum):
        fpr[i], tpr[i], _ = metrics.roc_curve(predict_class[:, i], y_score[:, i])
        roc_auc[i] = auc(fpr[i], tpr[i])

    # Compute micro-average ROC curve and ROC area
    fpr["micro"], tpr["micro"], _ = roc_curve(predict_class.ravel(), y_score.ravel())
    roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])
    if isMicro:
        plt.plot(
            fpr["micro"],
            tpr["micro"],
            label="(area = {0:0.2f})".format(roc_auc["micro"]),
            color=str(roc_colors[1]),
        )
    else:
        for k in range(classNum):
            figPlots[k][1].plot(
                fpr[k],
                tpr[k],
                color=str(roc_colors[1]),
                label="(area = %0.3f)" % roc_auc[k],
            )
            figPlots[k][1].legend()
    plt.rcParams.update({'font.size': 14})
    if classNum ==2 or isMicro:
        plt.savefig(output_filename+'.png')
        plt.figure().clear()
    else:
        for j in range(classNum):
            # figPlots[j][1].set_title(graph_title +'class '+ [k for k,v in class_trans_dict.items() if v == str(j+1)][0])
            figPlots[j][0].savefig(output_filename +'class '+ [k for k,v in class_trans_dict.items() if v == str(j+1)][0] + '.png')
            figPlots[j][0].clear()


def runPyCR(isexternal,rateSplit,isMicro,tupaType,isMotabo,motaboFileName,dataFileName,classFileName,sampleNameFileName,variableNameFileName,external_type,ex_isMotabo, ex_MotaboFileName,ex_DataFileName,ex_ClassFileName,ex_sampleNameFile,ex_variableNameFile,scaleType,normType,howManyIteration,survivalrate,V_rankingAlgorithm,nComponent, task_pk):
    if isexternal == 'true':
        isexternal = True
    else:
        isexternal = False
    if isMicro == 'true':
        isMicro = True
    else:
        isMicro = False
    if isMotabo == 'true':
        isMotabo = True
    else:
        isMotabo = False
    try:
        nComponent = int(nComponent)
    except:
        nComponent = 0
    if rateSplit:
        rateSplit = (1-rateSplit)

    mainPyCR(isexternal, rateSplit, isMicro, tupaType, isMotabo, motaboFileName, dataFileName, classFileName,
         sampleNameFileName, variableNameFileName, external_type,ex_isMotabo, ex_MotaboFileName,ex_DataFileName,ex_ClassFileName,ex_sampleNameFile,ex_variableNameFile, scaleType, normType, howManyIteration, survivalrate, V_rankingAlgorithm,
         nComponent, task_pk)


class Normalization:
    def __init__(self):
        # for scale Method is must have either [Auto scale/Mean center]
        # for norm Method is optional [normalization/SVN/None ]
        # for tupa Method is optional [tupa/classTupa/None]
        self.func_dict = {'tupa':self.tupa,'classtupa':self.class_tupa,'notupa':self.tupa_plain,'norm':self.norm_normalization,'SVN':self.svn_normalization,'nonorm':self.plain,'autoscale':self.auto_scale, 'meancenter':self.mean_center_scale}

    # pre-processing data algorithm, total useful peak area depend on class
    # INPUT : sample data, class data
    # OUTPUT : processed sample data
    def tupa(self,X,Y):
        cls = np.array(Y)
        X = np.array(X)
        cls = np.unique(cls)
        usetupa =[]
        return_sampleList=[]
        for i in range(len(X[0])):
            temp_vari = X[:,i]
            if 0 not in temp_vari:
                usetupa.append(1)
            else:
                usetupa.append(0)
        for i in range(len(Y)):
            X_temp = X[i]
            mul_temp = copy.copy(X_temp)
            for k in range(len(mul_temp)):
                mul_temp[k] = mul_temp[k]*usetupa[k]
            temp_sum = np.sum(mul_temp)
            temp_div = np.divide(X_temp,temp_sum)
            return_sampleList.append(temp_div.tolist())
        return return_sampleList

    # pre-processing data algorithm, total useful peak area for irespective of class
    # INPUT : sample data, class data
    # OUTPUT : processed sample data
    def class_tupa(self,X,Y):
        cls = np.array(Y)
        X = np.array(X)
        cls = np.unique(cls)
        numCls = len(cls)
        class_idx = []
        return_sampleList = []
        for j in range(numCls):
            class_idx.append([])
        for z in range(len(Y)):
            class_idx[Y[z]-1].append(z)
        usetupa =[]
        for i in range(numCls):
            temp_usetupa =[]
            X_temp = X[class_idx[i],:]
            for i in range(len(X_temp[0])):
                temp_vari = X_temp[:,i]
                if 0 not in temp_vari:
                    temp_usetupa.append(1)
                else:
                    temp_usetupa.append(0)
            usetupa.append(temp_usetupa)
        for i in range(len(Y)):
            X_temp = X[i]
            mul_temp = copy.copy(X_temp)
            for k in range(len(mul_temp)):
                mul_temp[k] = mul_temp[k]*usetupa[Y[i]-1][k]
            temp_sum = np.sum(mul_temp)
            temp_div = np.divide(X_temp,temp_sum)
            return_sampleList.append(temp_div.tolist())
        return return_sampleList

    # after get all the selected variables we make them a matrix and calculate the mean by using stander normal variate
    # INPUT : all sample data list,
    # OUTPUT: scaled all sample data
    def svn_normalization(self,samples):
        sd = StandardScaler(with_mean=True, with_std=False)
        sd.fit(samples)
        col_mean = sd.mean_
        scaled_samples = scale(samples, axis=1, with_mean=True, with_std=True)
        scaled_samples = np.subtract(scaled_samples, col_mean)
        return scaled_samples

    def norm_normalization(self,samples):
        normalized = preprocessing.normalize(samples)
        return normalized

    def mean_center_scale(self,samples):
        samples = np.array(samples)
        samples_mean = samples.mean(axis=0)
        np.set_printoptions(threshold=sys.maxsize)
        scaled_samples = np.subtract(samples, samples_mean)
        return scaled_samples

    # scale samples with the mean and std from previous scaling
    # INPUT : all sample data list, mean of previous scaling, stander deviation of previous scaling
    # OUTPUT: scaled all sample data
    def auto_scale(self,samples):
        samples = np.array(samples)
        samples_mean = samples.mean(axis=0)
        samples_std = np.std(samples, axis=0)
        np.set_printoptions(threshold=sys.maxsize)
        functionTop = np.subtract(samples, samples_mean)
        scaled_samples = np.divide(functionTop, samples_std)
        scaled_samples = np.nan_to_num(scaled_samples, nan=(10**-12))
        for list in scaled_samples:
            list[list==inf] = 10**-12
        return scaled_samples
    
    def plain(self,samples):
        return samples
    def tupa_plain(self,samples,classList):
        return samples
    

