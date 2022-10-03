import copy
import matplotlib
import numpy as np
from python_scripts.Feature_selection import newScore
from python_scripts.Feature_selection import genStartEndNum2
from sklearn import svm
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.metrics import roc_curve, auc
from scipy.stats.distributions import chi2
from sklearn.multiclass import OneVsRestClassifier
import sys
from scipy.sparse.linalg import svds
from numpy import inf
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import xlsxwriter
import math
from colour import Color
from sklearn.preprocessing import label_binarize
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import scale
from python_scripts.Feature_selection import file_pkg
import warnings
from sklearn.metrics import accuracy_score,precision_score,recall_score
import sys
import matplotlib

warnings.filterwarnings('ignore')
matplotlib.use('agg')
def main(isexternal,howMuchSplit,isMicro,tupaType,isMotabo,MotaboFileName,DataFileName,ClassFileName,sampleNameFile,variableNameFile,scale_type,iteration,survivalRate,V_rankingAlgorithm, nComponent,task_pk):
    ITERATION = iteration

    # generate roc color for ROC curve
    RED = Color("#dc3c40")
    ROC_COLOR = list(RED.range_to(Color("#55a6bc"), ITERATION + 1))

    # set class color list
    CLASS_COLOR = ["#dc3c40", "#55a6bc", 'purple', 'yellowgreen', 'wheat', 'royalblue', '#42d7f5', '#ca7cf7', '#d2f77c']
    CLASS_LABEL = ["o", "x", "4", "*", "+", "D", "8", "s", "p"]

    print("Loading start and stop number .....")
    # create the needed folder to save ouput data
    # read data from input files
    OUTPUT_PATH = file_pkg.create_folder(task_pk)
    if isMotabo:
        sampleList, sampleName, classList, variableName =file_pkg.readMotabo(MotaboFileName)
    else:
        classList = file_pkg.getValFromFileByCols(ClassFileName)[0]
        sampleList = file_pkg.getValFromFileByRows(DataFileName)
        sampleName = file_pkg.getValFromFileByCols(sampleNameFile)[0]
        variableName = file_pkg.getValFromFileByCols(variableNameFile)

    # get the class number from class name
    # generate number version of class name
    unique_class = set(classList)
    unique_class = sorted(list(unique_class))
    classNum = len(unique_class)
    class_trans_dict = {}
    for i in range(classNum):
        class_trans_dict[unique_class[i]] = str(i+1)
    for key in class_trans_dict.keys():
        classList = [sub.replace(key, class_trans_dict[key]) for sub in classList]
    classList = [int(x) for x in classList]
    # create label list for plot
    class_num_label = []
    for i in range(1, classNum + 1):
        class_num_label.append(i)

    # back up the original sample list and class list
    ori_sample = copy.deepcopy(np.array(sampleList))
    ori_class = classList
    #Do class Tupa
    hori_index = []
    indice_list = []
    if tupaType.lower() =='tupa':
        sampleList = tupa(sampleList,classList)
    elif tupaType.lower()=='classtupa':
        sampleList = class_tupa(sampleList, classList)

    for i in range(len(sampleList[0])):
        hori_index.append(i)
    for j in range(len(classList)):
        indice_list.append(j)
    if tupaType.lower() == 'tupa':
        file_pkg.export_file(sampleList, ori_class, indice_list, hori_index, OUTPUT_PATH+ '/tupaAllSample.csv', class_trans_dict,sampleName,variableName)
    elif tupaType.lower() == 'classtupa':
        file_pkg.export_file(sampleList, ori_class, indice_list, hori_index, OUTPUT_PATH+ '/ClassTupaAllSample.csv', class_trans_dict,sampleName,variableName)
    file_pkg.export_file(ori_sample, ori_class, indice_list, hori_index, OUTPUT_PATH +'/original_file.csv', class_trans_dict,sampleName,variableName)
    ## if there is not enough samples to do the external validation no matter what the user says isexternal will be false
    ## use hash table to see how many samples for each class and if countSample < 9 we dont do external
    hash_classCount = [0] * (classNum + 1)
    if len(sampleList) < 50:
        isexternal = False
    for c_num in classList:
        hash_classCount[c_num] += 1
    for i in range(1,classNum+1):
        if hash_classCount[i] < 9:
            isexternal = False

    if not isexternal:
        indices_train = indice_list
        if scale_type == 'SVN':
            scale_training_sample, col_mean = SVN_scale_half_data(sampleList)
        elif scale_type == "autoscale":
            scale_training_sample, scale_training_mean, scale_training_std = scale_half_data(sampleList)
        else:
            scale_training_sample = sampleList

    if isexternal:
        sampleList, external_validation, classList, external_class, indices_train, indices_test = selectRandom(
            sampleList, classList, howMuchSplit)
        # Create stat file with
        if scale_type == 'SVN':
            scale_training_sample, col_mean = SVN_scale_half_data(sampleList)
            scaled_external, col_mean = SVN_scale_half_data(external_validation)
        elif scale_type == "autoscale":
            scale_training_sample, scale_training_mean, scale_training_std = scale_half_data(sampleList)
            scaled_external, scale_training_mean, scale_training_std = scale_half_data(external_validation)
        else:
            scale_training_sample = sampleList
            scaled_external = external_validation

        class_stat_list_noCutoff = []
        class_stat_list_external_noCutoff = []
        for classNum in range(1, int(classNum) + 1):
            class_stat_list_noCutoff.append([])
            # Create stat file with
            class_stat_list_external_noCutoff.append([])
        # Train and predict the class
        clf = svm.SVC(kernel='linear', random_state=42, probability=True)
        clf.fit(scale_training_sample, classList)
        class_pred = clf.predict(scale_training_sample)
        classofic_report = classification_report(classList, class_pred)
        internal_stat_acc = accuracy_score(classList, class_pred)
        internal_stat_sel = precision_score(classList, class_pred, average='micro')
        internal_stat_sen = recall_score(classList, class_pred, average='micro')
        file_pkg.gen_file_by_line(["Selectivity", "Sensitivity", "Accuracy"],
                                          [internal_stat_sel, internal_stat_sen, internal_stat_acc],
                                          OUTPUT_PATH + '/training_stat_report_no_FS.csv')

        report_lines = classofic_report.split('\n')
        report_lines = report_lines[2:]
        # generate the statistic report
        for c in range(0, classNum):
            stat_num = report_lines[c].split(' ')
            stat_num = [i for i in stat_num if i != ""]
            class_stat_list_noCutoff[c].append(stat_num[1:])
        for c in range(classNum):
            file_pkg.gen_file_by_class_matrix(["Selectivity", "Sensitivity", "Accuracy"],
                                              class_stat_list_noCutoff[c][:3], OUTPUT_PATH+ '/training_stat_report_class_' +
                                              [k for k, v in class_trans_dict.items() if v == str(c + 1)][
                                                  0] + '_no_FS.csv')
        # for external
        class_pred_external = clf.predict(scaled_external)
        classofic_report_external = classification_report(external_class, class_pred_external)
        external_stat_acc = accuracy_score(external_class, class_pred_external)
        external_stat_sel = precision_score(external_class, class_pred_external, average='micro')
        external_stat_sen = recall_score(external_class, class_pred_external, average='micro')
        file_pkg.gen_file_by_line(["Selectivity", "Sensitivity", "Accuracy"],
                                          [external_stat_sel, external_stat_sen, external_stat_acc],
                                          OUTPUT_PATH + '/external_stat_report_no_FS.csv')

        report_lines_external = classofic_report_external.split('\n')
        report_lines_external = report_lines_external[2:]
        # generate the statistic report
        for c in range(0, classNum):
            stat_num_external = report_lines_external[c].split(' ')
            stat_num_external = [i for i in stat_num_external if i != ""]
            class_stat_list_external_noCutoff[c].append(stat_num_external[1:])
        for c in range(classNum):
            file_pkg.gen_file_by_class_matrix(["Selectivity", "Sensitivity", "Accuracy"],
                                              class_stat_list_external_noCutoff[c][:3],
                                              OUTPUT_PATH + '/external_stat_report_class_' +
                                              [k for k, v in class_trans_dict.items() if v == str(c + 1)][
                                                  0] + '_no_FS.csv')
    # output the splited training and external variables(if meet the external requirement) in special form
    if isexternal:
        index_indices_train = [x - 1 for x in indices_train]
        index_indices_test = [x - 1 for x in indices_test]
        file_pkg.export_file(ori_sample, ori_class, index_indices_train, hori_index, OUTPUT_PATH + '/training_variables.csv', class_trans_dict, sampleName,variableName)
        file_pkg.export_file(ori_sample, ori_class, index_indices_test, hori_index, OUTPUT_PATH + '/external_variables.csv', class_trans_dict, sampleName,variableName)
    else:
        index_indices_train = [x - 1 for x in indices_train]
        file_pkg.export_file(ori_sample, ori_class, index_indices_train, hori_index, OUTPUT_PATH + '/training_variables.csv', class_trans_dict, sampleName,variableName)
        external_variables_wb = xlsxwriter.Workbook(OUTPUT_PATH + '/external_variables.xlsx')
        external_variables_ws = external_variables_wb.add_worksheet()
        external_variables_ws.write(0, 0, "There is not enough samples to have external validation.")

    # get the start number and the end number
    startNum, endNum = genStartEndNum2.gaussian_algorithm(int(classNum), classList,sampleList,  V_rankingAlgorithm,nComponent,OUTPUT_PATH )

    # create a file to save the generate statistical number(accuracy, sensitivity, selectivity)

    # create a hash table to take count for the show up times for each variables
    hash_list = [0]*(len(sampleList[0]))

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

    # start Iterations
    erro_iterations = 0
    error_msg = []
    for k in range(ITERATION):
        if erro_iterations < ceil(ITERATION, 2):
            print("################## ITERATION "+ str(k)+" ##################")
            try:
                # Start Feature Selection
                return_idx, sample_taining, sample_test, class_training, class_test = newScore.setNumber(int(classNum), classList, sampleList, startNum, endNum, howMuchSplit,k, class_trans_dict, scale_type, V_rankingAlgorithm, nComponent,OUTPUT_PATH)
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

                # scale the data
                if scale_type == 'SNV':
                    scaled_sample_training,col_mean = SVN_scale_half_data(sample_taining)
                    scaled_all_sample = SNV_scale_all_data(sampleList,col_mean)
                elif scale_type == "autoscale":
                    scaled_sample_training,train_mean,train_std = scale_half_data(sample_taining)
                    scaled_all_sample = scale_all_data(sampleList,train_mean,train_std)
                else:
                    scaled_sample_training = sample_taining
                    scaled_all_sample = sampleList


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
                    plt.title('ROC ' + str(ITERATION) + ' iterations')
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
                            label="micro-average ROC curve (area = {0:0.2f})".format(roc_auc["micro"]),
                            color=str(ROC_COLOR[k]),
                        )
                        auc_table.append(roc_auc["micro"])
                        plt.rcParams.update({'font.size':10 })
                        plt.title('ROC ' + str(ITERATION) + ' iterations')
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
        plt.savefig(OUTPUT_PATH + '/rocIterations/roc ' + str(ITERATION) +'.png')
        plt.figure().clear()
    else:
        for i in range(classNum):
            figPlot[i][1].set_title('Roc ' + str(ITERATION) + ' iterations class: ' + [k for k, v in class_trans_dict.items() if v == str(i+1)][0])
            figPlot[i][0].savefig(OUTPUT_PATH + '/rocIterations/roc '+str(ITERATION) +'iterations class: '+[k for k,v in class_trans_dict.items() if v == str(i+1)][0]+'.png')
            figPlot[i][0].clear()

    # save all the auc number in to csv table
    if classNum == 2 or isMicro:
        file_pkg.gen_file_by_list(["Auc Number"],auc_table,OUTPUT_PATH + '/auc_table.csv')
    else:
        for j in range(classNum):
            file_pkg.gen_file_by_list(["Auc Number"],auc_table[i],OUTPUT_PATH + '/auc_table_class_' + [k for k,v in class_trans_dict.items() if v == str(j+1)][0] + '.csv')



    valid_idx = []
    # calculate the show-up ratio for each variable
    for i in range(len(hash_list)):
        prob = float(hash_list[i])/ITERATION
        # we are only taking the ratio more than 30%
        if prob >= survivalRate:
            valid_idx.append(i)

    if len(valid_idx) < 2:
        notEnoughtSelectedVariableErrorMessage(hash_list, survivalRate, variableName, ITERATION, OUTPUT_PATH)
        return

    # generate file for selected training and selected validation in special format
    if isexternal:
        file_pkg.export_file(ori_sample, ori_class, index_indices_train, valid_idx,
                             OUTPUT_PATH + '/selected_training_variables.csv', class_trans_dict, sampleName,
                             variableName)
        file_pkg.export_file(ori_sample, ori_class, index_indices_test, valid_idx,
                             OUTPUT_PATH + '/selected_external_variables.csv', class_trans_dict, sampleName,
                             variableName)
    else:
        file_pkg.export_file(ori_sample, ori_class, index_indices_train, valid_idx,
                             OUTPUT_PATH + '/selected_training_variables.csv', class_trans_dict, sampleName,
                             variableName)
        external_variables_wb = xlsxwriter.Workbook(OUTPUT_PATH + '/selected_external_variables.xlsx')
        external_variables_ws = external_variables_wb.add_worksheet()
        external_variables_ws.write(0, 0, "There is not enough samples to have external validation.")

    class_stat_list_noCutoff = []
    class_stat_list_external_noCutoff = []
    for classNum in range(1, int(classNum) + 1):
        class_stat_list_noCutoff.append([])
        # Create stat file with
        class_stat_list_external_noCutoff.append([])
    # Train and predict the class
    clf_FS = svm.SVC(kernel='linear', random_state=42, probability=True)
    clf_FS.fit(scale_training_sample[:, valid_idx], classList)
    class_pred = clf_FS.predict(scale_training_sample[:, valid_idx])
    classofic_report = classification_report(classList, class_pred)
    internal_stat_acc_w_FS = accuracy_score(classList, class_pred)
    internal_stat_sel_w_FS = precision_score(classList, class_pred, average='micro')
    internal_stat_sen_w_FS = recall_score(classList, class_pred, average='micro')
    file_pkg.gen_file_by_line(["Selectivity", "Sensitivity", "Accuracy"],
                                      [internal_stat_sel_w_FS, internal_stat_sen_w_FS, internal_stat_acc_w_FS],
                                      OUTPUT_PATH + '/training_stat_report_with_FS.csv')


    report_lines = classofic_report.split('\n')
    report_lines = report_lines[2:]
    # generate the statistic report
    for c in range(0, classNum):
        stat_num = report_lines[c].split(' ')
        stat_num = [i for i in stat_num if i != ""]
        class_stat_list_noCutoff[c].append(stat_num[1:])
    for c in range(classNum):
        file_pkg.gen_file_by_class_matrix(["Selectivity", "Sensitivity", "Accuracy"],
                                          class_stat_list_noCutoff[c][:3], OUTPUT_PATH + '/training_stat_report_class_' +
                                          [k for k, v in class_trans_dict.items() if v == str(c + 1)][
                                              0] + '_with_FS.csv')
    # for external
    if isexternal:
        class_pred_external = clf_FS.predict(scaled_external[:, valid_idx])
        classofic_report_external = classification_report(external_class, class_pred_external)
        external_stat_acc_w_FS = accuracy_score(external_class, class_pred_external)
        external_stat_sel_w_FS = precision_score(external_class, class_pred_external, average='micro')
        external_stat_sen_w_FS = recall_score(external_class, class_pred_external, average='micro')
        file_pkg.gen_file_by_line(["Selectivity", "Sensitivity", "Accuracy"],
                                          [external_stat_sel_w_FS, external_stat_sen_w_FS, external_stat_acc_w_FS],
                                          OUTPUT_PATH + '/external_stat_report_with_FS.csv')
        report_lines_external = classofic_report_external.split('\n')
        report_lines_external = report_lines_external[2:]
        # generate the statistic report
        for c in range(0, classNum):
            stat_num_external = report_lines_external[c].split(' ')
            stat_num_external = [i for i in stat_num_external if i != ""]
            class_stat_list_external_noCutoff[c].append(stat_num_external[1:])
        for c in range(classNum):
            file_pkg.gen_file_by_class_matrix(["Selectivity", "Sensitivity", "Accuracy"],
                                              class_stat_list_external_noCutoff[c][:3],
                                              OUTPUT_PATH + '/external_stat_report_class_' +
                                              [k for k, v in class_trans_dict.items() if v == str(c + 1)][
                                                  0] + '_with_FS.csv')
    ####################################  START GRAPH CODE ###################################
    # scale data
    # if scale_type == 'SNV':
    #     scale_training_sample, col_mean= SVN_scale_half_data(sampleList)
    #     scaled_external, col_mean= SVN_scale_half_data(external_validation)
    # else:
    #     scale_training_sample, scale_training_mean, scale_training_std = scale_half_data(sampleList)
    #     scaled_external, scale_training_mean, scale_training_std = scale_half_data(external_validation)

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
        for i in range(len(external_class)):
            external_class_index_list[external_class[i]].append(i)

    # calculaye the score for PCA, generate the PCA graph for traning and external
    class_variables = scale_training_sample[:, valid_idx]
    dummyU, dummyS, V = svds(class_variables, k=2)
    V = np.transpose(V)
    score = np.dot(scaled_all_sample[:,valid_idx], V)
    for z in range(1, classNum+1):
        class_score = score[class_index_list[z],:]
        x_ellipse, y_ellipse = confident_ellipse(class_score[:, 0], class_score[:, 1])
        plt.plot(x_ellipse, y_ellipse,color=CLASS_COLOR[z-1])
        plt.fill(x_ellipse, y_ellipse,color=CLASS_COLOR[z-1], alpha=0.3)
        class_Xt = score[class_index_list[z], :]
        plt.scatter(class_Xt[:, 0], class_Xt[:, 1], c=CLASS_COLOR[z-1], marker=CLASS_LABEL[0], label='training ' + [k for k,v in class_trans_dict.items() if v == str(z)][0])
    pU, pS, pV = np.linalg.svd(class_variables)
    pca_percentage_val = np.cumsum(pS) / sum(pS)
    p2_percentage = pca_percentage_val[0] * 100
    p1_percentage = pca_percentage_val[1] * 100
    plt.xlabel("PC1(%{0:0.3f}".format(p1_percentage) + ")",fontsize=15)
    plt.ylabel("PC2 (%{0:0.3f}".format(p2_percentage) + ")",fontsize=15)
    plt.rcParams.update({'font.size': 10})
    plt.title('PCA training')
    plt.legend()
    plt.savefig(OUTPUT_PATH + '/pca_taining.png')

    if isexternal:
        external_Xt = np.dot(scaled_external[:, valid_idx], V)
        for n in range(1, classNum + 1):
            class_external_Xt = external_Xt[external_class_index_list[n], :]
            plt.scatter(class_external_Xt[:, 0], class_external_Xt[:, 1], c=CLASS_COLOR[n - 1], marker=CLASS_LABEL[1],
                        label='external ' + [k for k, v in class_trans_dict.items() if v == str(n)][0])
        plt.title('PCA Training , Validation, with Feature Selection ')
        plt.rcParams.update({'font.size': 10})
        plt.legend()
        plt.savefig(OUTPUT_PATH + '/pca_external.png')
        plt.figure().clear()

        # generate confusion matrix and statistical report
        clf_extern = svm.SVC(kernel='linear', random_state=0, probability=True)
        clf_extern.fit(scale_training_sample[:, valid_idx], classList)
        class_pred = clf_extern.predict(scaled_external[:, valid_idx])
        conf_matrix = confusion_matrix(external_class, class_pred)
        file_pkg.gen_file_by_matrix(conf_matrix,OUTPUT_PATH + '/confusion_matrix.csv')
        clf_extern_no_FS = svm.SVC(kernel='linear', random_state=0, probability=True)
        clf_extern_no_FS.fit(scale_training_sample, classList)
        class_pred_no_FS = clf_extern_no_FS.predict(scaled_external)
        conf_matrix_no_FS = confusion_matrix(external_class, class_pred_no_FS)
        file_pkg.gen_file_by_matrix(conf_matrix_no_FS, OUTPUT_PATH + '/confusion_matrix_no_FS.csv')


    # generate ROC for external validation and selected variables
    if isexternal:
        if classNum == 2:
           gen_roc_graph(scale_training_sample[:,valid_idx],classList,scaled_external[:,valid_idx],external_class,OUTPUT_PATH + "/rocExternal/roc_external.png", 'ROC External ')
        else:
            mul_roc_graph(classNum,class_num_label,classList,external_class,scale_training_sample[:,valid_idx],scaled_external[:,valid_idx],ROC_COLOR,OUTPUT_PATH + "/rocExternal/ROC External ",isMicro,'ROC External ', class_trans_dict)


    # generate 4 SVM graph
    # graph 1: training without feature selection
    gen_pca(scale_training_sample, classNum, class_index_list, CLASS_COLOR, CLASS_LABEL,OUTPUT_PATH +  '/PCATrainNoFS.png','PCA Training, No Feature Selection ',class_trans_dict)
    # generate predict ROC
    if classNum == 2:
        gen_roc_graph(scale_training_sample,classList,scale_training_sample,classList,OUTPUT_PATH + '/rocTrainNoFS/rocTrainNoFS.png','ROC Training, No Feature Selection ')
    else:
        mul_roc_graph(classNum, class_num_label, classList, classList, scale_training_sample,
                      scale_training_sample, ROC_COLOR, OUTPUT_PATH + '/rocTrainNoFS/rocTrainNoFS',isMicro,'ROC Training, No Feature Selection ', class_trans_dict)

    # graph 2: validation without feature selection
    if isexternal:
        gen_pca(scaled_external, classNum, external_class_index_list, CLASS_COLOR, CLASS_LABEL, OUTPUT_PATH + '/PCAValiNoFS.png','PCA Validation, No Feature Selection ',class_trans_dict)
        # generate predict ROC
        if classNum == 2:
            gen_roc_graph(scale_training_sample,classList,scaled_external,external_class,OUTPUT_PATH + '/rocValiNoFS/rocValiNoFS.png', 'ROC Validation, No Feature Selection ')
        else:
            mul_roc_graph(classNum, class_num_label, classList, external_class, scale_training_sample,
                          scaled_external, ROC_COLOR, OUTPUT_PATH + '/rocValiNoFS/rocValiNoFS',isMicro,'ROC Validation, No Feature Selection ', class_trans_dict)


    # graph 3: training with feature selection
    gen_pca(scale_training_sample[:,valid_idx], classNum, class_index_list, CLASS_COLOR, CLASS_LABEL,OUTPUT_PATH + '/PCATrainWithFS.png','PCA Training, With Feature Selection ',class_trans_dict)
    # generate predict ROC
    if classNum == 2:
        gen_roc_graph(scale_training_sample[:,valid_idx],classList,scale_training_sample[:,valid_idx],classList,OUTPUT_PATH + '/rocTrainFS/rocTrainFS.png','ROC Training, With Feature Selection ')
    else:
        mul_roc_graph(classNum, class_num_label, classList, classList, scale_training_sample[:,valid_idx],
                      scale_training_sample[:, valid_idx], ROC_COLOR, OUTPUT_PATH + '/rocTrainFS/rocTrainFS',isMicro, 'ROC Training, With Feature Selection ', class_trans_dict)


    # graph 4: validation with feature selection
    if isexternal:
        gen_pca(scaled_external[:, valid_idx], classNum, external_class_index_list, CLASS_COLOR, CLASS_LABEL,
                OUTPUT_PATH + '/PCAValiWithFS.png','PCA Validation, With Feature Selection ',class_trans_dict)

        # generate predict ROC
        if classNum == 2:
            gen_roc_graph(scale_training_sample[:,valid_idx],classList,scaled_external[:,valid_idx],external_class,OUTPUT_PATH + '/rocValiFS/rocValiFS.png', 'ROC Validation, With Feature Selection ' )
        else:
            mul_roc_graph(classNum, class_num_label, classList, external_class, scale_training_sample[:, valid_idx],
                          scaled_external[:, valid_idx], ROC_COLOR,OUTPUT_PATH + '/rocValiFS/rocValiFS',isMicro, 'ROC Validation, With Feature Selection ', class_trans_dict)

    # graph 5: PCA with Internal and external without FS
    class_variables_no_FS = scale_training_sample
    dummyU, dummyS, V_no_FS = svds(class_variables_no_FS, k=2)
    V_no_FS = np.transpose(V_no_FS)
    score_no_FS = np.dot(scaled_all_sample, V_no_FS)
    for z in range(1, classNum+1):
        class_score_no_FS = score_no_FS[class_index_list[z],:]
        x_ellipse, y_ellipse = confident_ellipse(class_score_no_FS[:, 0], class_score_no_FS[:, 1])
        plt.plot(x_ellipse, y_ellipse,color=CLASS_COLOR[z-1])
        plt.fill(x_ellipse, y_ellipse,color=CLASS_COLOR[z-1], alpha=0.3)
        class_Xt_no_FS = score_no_FS[class_index_list[z], :]
        plt.scatter(class_Xt_no_FS[:, 0], class_Xt_no_FS[:, 1], c=CLASS_COLOR[z-1], marker=CLASS_LABEL[0], label='training ' + [k for k,v in class_trans_dict.items() if v == str(z)][0])
    # calculating the PCA percentage value
    pU_no_FS, pS_no_FS, pV_no_FS = np.linalg.svd(class_variables_no_FS)
    pca_percentage_val_no_FS = np.cumsum(pS_no_FS) / sum(pS_no_FS)
    p2_percentage = pca_percentage_val_no_FS[0] * 100
    p1_percentage = pca_percentage_val_no_FS[1] * 100
    plt.xlabel("PC1(%{0:0.3f}".format(p1_percentage) + ")")
    plt.ylabel("PC2 (%{0:0.3f}".format(p2_percentage) + ")")
    plt.rcParams.update({'font.size': 10})
    if isexternal:
        external_Xt = np.dot(scaled_external, V_no_FS)
        for n in range(1, classNum+1):
            class_external_Xt = external_Xt[external_class_index_list[n], :]
            plt.scatter(class_external_Xt[:, 0], class_external_Xt[:, 1], c=CLASS_COLOR[n-1], marker=CLASS_LABEL[1],
                               label='external ' + [k for k,v in class_trans_dict.items() if v == str(n)][0])
    plt.title('PCA Training , Validation, No Feature Selection')
    plt.rcParams.update({'font.size': 10})
    plt.legend()
    plt.savefig(OUTPUT_PATH + '/pca_No_FS.png',bbox_inches="tight" )
    plt.figure().clear()

    return

    ####################################  END GRAPH CODE ###################################

# scale half of the sample
# INPUT : sample data list
# OUTPUT: scaled  sample data, mean of the sample, stander deviation for the sample
def scale_half_data(samples):
    samples = np.array(samples)
    samples_mean = samples.mean(axis=0)
    samples_std = np.std(samples, axis=0)
    np.set_printoptions(threshold=sys.maxsize)
    functionTop = np.subtract(samples, samples_mean)
    scaled_samples = np.divide(functionTop, samples_std)
    scaled_samples = np.nan_to_num(scaled_samples, nan=(10**-12))
    for list in scaled_samples:
        list[list==inf] = 10**-12
    return scaled_samples, samples_mean, samples_std

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

# after get all the selected variables we make them a matrix and calculate the mean by using stander normal variate
# INPUT : all sample data list
# OUTPUT: scaled all sample data, the mean of all the variables
def SVN_scale_half_data(samples):
    sd = StandardScaler(with_mean=True, with_std=False)
    sd.fit(samples)
    col_mean = sd.mean_
    scaled_samples = scale(samples, axis=1, with_mean=True, with_std=True)
    return scaled_samples, col_mean

# after get all the selected variables we make them a matrix and calculate the mean by using stander normal variate
# INPUT : all sample data list,

# OUTPUT: scaled all sample data
def SNV_scale_all_data(samples,col_mean):
    scaled_samples = scale(samples, axis=1, with_mean=True, with_std=True)
    scaled_samples = np.subtract(scaled_samples, col_mean)
    return scaled_samples

# split the sample data randomly by the rate of spliting (0-1)
# INPUT : sample data list, class list, rate of spliting
# OUTPUT : training data, validation data, training class, validation class, training data index, validation ata index
def selectRandom(sample_list,class_list,howMuchSplit):
    indices = np.arange(1,len(class_list)+1)
    sample_matrix = np.array(sample_list)
    class_matrix = np.array(class_list)
    X_train, X_test, y_train, y_test, indices_train, indices_test = train_test_split(sample_matrix, class_matrix, indices, test_size=float(howMuchSplit), stratify=class_matrix)
    return X_train, X_test, y_train, y_test, indices_train, indices_test

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

# generate ROC graph for data set more than 2 classes
# INPUT : class number, label of class number, training classes, predict classes, training data, predict data, color list for the roc graph, is Micro ROC, title of the graph, original class name
# OUTPUT : None
def mul_roc_graph(classNum, class_num_label, trainingClass, predicClass, trainingVal, predicVal, roc_colors, output_filename,isMicro,graph_title,class_trans_dict):
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
            label="micro-average ROC curve (area = {0:0.2f})".format(roc_auc["micro"]),
            color=str(roc_colors[1]),
        )
    else:
        for k in range(classNum):
            figPlots[k][1].plot(
                fpr[k],
                tpr[k],
                color=str(roc_colors[1]),
                label="ROC curve (area = %0.3f)" % roc_auc[k],
            )
            figPlots[k][1].legend()
    plt.rcParams.update({'font.size': 14})
    if classNum ==2 or isMicro:
        plt.savefig(output_filename+'.png')
        plt.figure().clear()
    else:
        for j in range(classNum):
            figPlots[j][1].set_title(graph_title +'class '+ [k for k,v in class_trans_dict.items() if v == str(j+1)][0])
            figPlots[j][0].savefig(output_filename +'class '+ [k for k,v in class_trans_dict.items() if v == str(j+1)][0] + '.png')
            figPlots[j][0].clear()

# generate ROC graph for data set have 2 classes
# INPUT : training data, training class, predict data, predict class, name of the output file, title of the graph
# OUTPUT : None
def gen_roc_graph(training_sample,training_class,predict_sample,predict_class, fileName, graph_title):
    # Create a svm Classifier
    clf = svm.SVC(kernel='linear', random_state=0, probability=True)  # Linear Kernel
    # Train the model using the training sets
    clf.fit(training_sample, training_class)
    class_pred = clf.predict_proba(predict_sample)
    class_pred = class_pred[:, 1]
    auc_external = metrics.roc_auc_score(predict_class, class_pred)
    fpr, tpr, _ = metrics.roc_curve(predict_class, class_pred, pos_label=2)
    plt.plot(fpr, tpr, label="micro-average ROC curve (area = {0:0.3f})".format(auc_external))
    plt.title(graph_title)
    plt.rcParams.update({'font.size': 14})
    plt.legend(loc=4)
    plt.savefig(fileName,bbox_inches="tight")
    plt.figure().clear()

# generate PCA graph
# INPUT : training data, number of class, class index list, class color list, class label list, name of the output file, original class name
# OUTPUT : None
def gen_pca(training_sample,classNum,class_index_list,class_color,class_label,fileName,graph_title, class_trans_dict):
    dummyU, dummyS, V = svds(training_sample, k=2)
    V = np.transpose(V)
    Xt_training_noFS = np.dot(training_sample, V)
    for z in range(1, classNum + 1):
        class_Xt_training_noFS = Xt_training_noFS[class_index_list[z], :]
        x_ellipse, y_ellipse = confident_ellipse(class_Xt_training_noFS[:, 0], class_Xt_training_noFS[:, 1])
        plt.plot(x_ellipse, y_ellipse, color=class_color[z - 1])
        plt.fill(x_ellipse, y_ellipse, color=class_color[z - 1], alpha=0.3)
        plt.scatter(class_Xt_training_noFS[:, 0], class_Xt_training_noFS[:, 1], c=class_color[z - 1],
                    marker=class_label[0], label='class ' + [k for k,v in class_trans_dict.items() if v == str(z)][0])
    # calculating the PCA percentage value
    pU, pS, pV = np.linalg.svd(training_sample)
    pca_percentage_val = np.cumsum(pS) / sum(pS)
    p2_percentage = pca_percentage_val[0] * 100
    p1_percentage = pca_percentage_val[1] * 100
    plt.xlabel("PC1(%{0:0.3f}".format(p1_percentage) + ")")
    plt.ylabel("PC2 (%{0:0.3f}".format(p2_percentage) + ")")
    plt.title(graph_title)
    plt.rcParams.update({'font.size': 10})
    plt.legend()
    plt.savefig(fileName,bbox_inches="tight")
    plt.figure().clear()

# pre-processing data algorithm, total useful peak area for irespective of class
# INPUT : sample data, class data
# OUTPUT : processed sample data
def class_tupa(X,Y):
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

# pre-processing data algorithm, total useful peak area depend on class
# INPUT : sample data, class data
# OUTPUT : processed sample data

def tupa(X,Y):
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


# isexternal,howMuchSplit,isMicro,tupaType,isMotabo,MotaboFileName,DataFileName,ClassFileName,sampleNameFile,variableNameFile
## Tupa Selection: tupa, classtupa, notupa
## Scale Selection: SNV,AutoScale
#main(True,0.5,False,'notupa',False,'Input/mota_data.csv','Input/data_pureOil.csv','Input/class_pureOil_2.csv','Input/sampleName_pureOil.csv','Input/Vname_pureOil.csv','AutoScale',10,0.85)
#main(True,0.5,False,'classTupa',False,'Input/mota_data.csv','Input/data_algae.csv','Input/class_algae_string.csv','Input/S_name.csv','Input/v_name.csv','AutoScale',10,0.85)

## Needed parameters
## 1 is external
## 2 the rate of splite the trainning and validation
## 3 is Micro for ROC
## 4 What kind of TUPA : a) classtupa b)tupa c)notupa
## 5 is the input data from motabo analize
## 6 your motabo data file name, if not using motabo data just input None instead
## 7 your data file name (not motabo data )
## 8 your class file name (not motabo data )
## 9 your sample name file name (not motabo data )
## 10 your variable name file name (not motabo data )
## 11 how would you like to scale your data: a) AotuScale b)SNV
## 12 how many iterations you like
## 13 the survival rate
def runPyCR(isexternal,rateSplit,isMicro,tupaType,isMotabo,motaboFileName,dataFileName,classFileName,sampleNameFileName,variableNameFileName,scaleType,howManyIteration,survivalrate,V_rankingAlgorithm,nComponent, task_pk):
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
    main(isexternal, rateSplit, isMicro, tupaType, isMotabo, motaboFileName, dataFileName, classFileName,
         sampleNameFileName, variableNameFileName, scaleType, howManyIteration, survivalrate, V_rankingAlgorithm,
         nComponent, task_pk)

# if __name__ == "__main__":
#     if sys.argv[1].lower() == 'true':
#         isexternal = True
#     else:
#         isexternal = False
#     rateSplit = float(sys.argv[2])
#     if sys.argv[3].lower() == 'true':
#         isMicro = True
#     else:
#         isMicro = False
#     tupaType = sys.argv[4]
#     if sys.argv[5].lower() == 'true':
#         isMotabo = True
#     else:
#         isMotabo = False
#     motaboFileName = sys.argv[6]
#     dataFileName = sys.argv[7]
#     classFileName = sys.argv[8]
#     sampleNameFileName = sys.argv[9]
#     variableNameFileName = sys.argv[10]
#     scaleType = sys.argv[11]
#     howManyIteration = int(sys.argv[12])
#     survivalrate = float(sys.argv[13])
#     V_rankingAlgorithm = sys.argv[14]
#     try:
#         nComponent = int(sys.argv[15])
#     except:
#         nComponent = 0
#     task_pk = sys.argv[16]
#
#     main(isexternal,rateSplit,isMicro,tupaType,isMotabo,motaboFileName,dataFileName,classFileName,sampleNameFileName,variableNameFileName,scaleType,howManyIteration,survivalrate,V_rankingAlgorithm,nComponent, task_pk)