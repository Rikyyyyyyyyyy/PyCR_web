import numpy as np
import random
import copy
import statistics
import matplotlib.pyplot as plt
from scipy.stats import norm
import math
from scipy import special
from scipy.stats import f
import warnings
import matplotlib
from python_scripts.Feature_selection import SelectivityRatio_in
from python_scripts.Feature_selection import vipScore_in
warnings.filterwarnings('ignore')
# get the start and stop number
# INPUT : class number, class data, sample data
# OUTPUT : start number, stop number
matplotlib.use('agg')
def gaussian_algorithm(classNum,class_list,valList,V_rankingAlgoithm,nComponent,output_path):
    ITERATIONS = 100
    sample_matrix = np.array(valList)
    k = 0
    true_means = []
    null_means = []
    # get the list of fisher ratio mean for tru and null distribution
    while k < ITERATIONS:
        # get the half random sample and half random variables list
        half_rand_matrix, sample_ind_list = selectHalfRandom(sample_matrix)
        half_rand_class_list = []
        for z in sample_ind_list:
            half_rand_class_list.append(class_list[z])
        classNum_list = []
        for i in range(classNum):
            classNum_list.append(i + 1)
        # create true distribution with the original class number
        true_dist_classNum = copy.deepcopy(half_rand_class_list)
        # create null distribution with the randomly assigned class number
        null_dist_classNum = []
        for i in range(len(half_rand_class_list)):
            null_dist_classNum.append(random.choice(classNum_list))
        # calculate the tru and null fisher ratio
        if V_rankingAlgoithm == "fisher":
            true_fisherRatio = cal_fish_ratio(half_rand_matrix, true_dist_classNum, classNum)
            null_fisherRatio = cal_fish_ratio(half_rand_matrix, null_dist_classNum, classNum)
        elif V_rankingAlgoithm == 'vip':
            true_fisherRatio = vipScore_in.vipy(half_rand_matrix, true_dist_classNum, nComponent)
            null_fisherRatio = vipScore_in.vipy(half_rand_matrix, null_dist_classNum, nComponent)
        elif V_rankingAlgoithm == 'selectivity':
            true_fisherRatio = SelectivityRatio_in.selrpy(half_rand_matrix, true_dist_classNum, nComponent)
            null_fisherRatio = SelectivityRatio_in.selrpy(half_rand_matrix, null_dist_classNum, nComponent)
        # generate the Theoretical and observed distribution of F values
        if k == 0 and V_rankingAlgoithm == 'fisher':
            dfn = classNum-1
            dfd = len(sample_matrix) - classNum

            x = np.linspace(f.ppf(0.01, dfn, dfd),
                            f.ppf(0.99, dfn, dfd), 100)
            plt.plot(x,f.pdf(x, dfn, dfd),
                    '--', color='#3468eb', lw=2, alpha=0.6, label='F pdf')
            plt.hist(true_fisherRatio, density=True, color="#3468eb", alpha=.95, label="observed F values",
                     range=(0, max(x)), bins=60)
            mn, mx = plt.xlim()
            y_min, y_max = plt.ylim()
            fisher_startNum = f.ppf(q=0.95, dfn=dfn, dfd=dfd)
            fisher_endNum = f.ppf(q=0.5, dfn=dfn, dfd=dfd)
            pos = y_max/2
            plt.plot([fisher_startNum, fisher_startNum], [0, pos], color='blue', label="Start Number")
            plt.plot([fisher_endNum, fisher_endNum], [0, pos], color='red', label="End Number")
            plt.plot(fisher_startNum, pos, color='blue',label="Start Number")
            plt.plot(fisher_endNum, pos, color='red', label="End Number")
            plt.legend(loc='best')
            plt.xlim(mn, mx)
            plt.title("Theoretical and observed distribution of F values")
            plt.savefig(output_path + '/Theoretical_and_observed_distribution_of_F_values.png', bbox_inches="tight")
            plt.figure().clear()
        true_mean_fisher_ratio = np.mean(true_fisherRatio)
        null_mean_fisher_ratio = np.mean(null_fisherRatio)
        true_means.append(true_mean_fisher_ratio)
        null_means.append(null_mean_fisher_ratio)
        k = k + 1
    for i in range(len(true_means)):
        if true_means[i] == np.inf:
            true_means[i] = 0
    for i in range(len(null_means)):
        if null_means[i] == np.inf:
            null_means[i] = 0
    true_fisher_mean = np.mean(true_means)
    true_fisher_std = np.std(true_means)
    null_fisher_mean = np.mean(null_means)
    null_fisher_std = np.std(null_means)

    # generate the CLT distribution
    # replace the inf in mean with the largest number in original matrix
    max_range = max(max(true_means),max(null_means))
    # start the true and null gaussian
    true_n, true_bins, true_patches = plt.hist(true_means, density=True,color="#3468eb",alpha=.6, label="true mean", range=(0,max_range),bins = 35)
    null_n, null_bins, null_patches = plt.hist(null_means, density=True, color="#34ebba", alpha=.6, label=" null mean", range=(0,max_range), bins=35)
    true_mean, true_std = norm.fit(true_means)
    null_mean, null_std = norm.fit(null_means)
    # true_y = ((1 / (np.sqrt(2 * np.pi) * true_fisher_std)) * np.exp(-0.5 * (1 / true_fisher_std * (true_bins - true_fisher_mean)) ** 2))
    true_y = ((1 / (np.sqrt(2 * np.pi) * true_std)) * np.exp(
        -0.5 * (1 / true_std * (true_bins - true_mean)) ** 2))
    plt.plot(true_bins, true_y, '--', color="#3468eb")
    # null_y = ((1 / (np.sqrt(2 * np.pi) * null_fisher_std)) * np.exp(
    #     -0.5 * (1 / null_fisher_std * (null_bins - null_fisher_mean)) ** 2))
    null_y = ((1 / (np.sqrt(2 * np.pi) * null_std)) * np.exp(
        -0.5 * (1 / null_std * (null_bins - null_mean)) ** 2))

    ## Calculate the overlapping between two normalization
    u1 = null_mean
    u2 = true_mean
    a1 = null_std
    a2 = true_std
    c_upper = u2*a1**2 - a2*(u1*a2+a1*math.sqrt((u1-u2)**2+(2*(a1**2 - a2**2) * math.log(a1/a2))))
    c_bottom = a1**2-a2**2
    c = c_upper / c_bottom
    x1 = (c-u1)/(math.sqrt(2)*a1)
    x2 = (c-u2)/(math.sqrt(2)*a2)
    P = 1-0.5*special.erf(x1)+ 0.5*special.erf(x2)
    startNum = statistics.NormalDist(mu=true_fisher_mean, sigma=true_fisher_std).inv_cdf(0.90)
    endNum = statistics.NormalDist(mu=null_fisher_mean, sigma=null_fisher_std).inv_cdf((1-P))
    ## Draw the graph
    plt.plot(null_bins, null_y, '--', color="#34ebba")

    plt.tight_layout()
    mn, mx = plt.xlim()
    y_min, y_max = plt.ylim()
    pos = y_max / 2
    plt.plot([startNum, startNum], [0, pos], color='blue', label="Start Number")
    plt.plot([endNum, endNum], [0, pos], color='red', label="End Number")
    plt.plot(startNum, pos, color='blue')
    plt.plot(endNum,  pos, color='red')
    plt.legend(loc='best')
    plt.xlim(mn, mx)
    if V_rankingAlgoithm == 'fisher':
        plt.ylabel("Likelihood")
        plt.xlabel("Mean of Fisher ratio")
        plt.title("Start and stop number determination via CLT")
        plt.savefig(output_path + '/FisherMean.png', bbox_inches="tight")
    elif V_rankingAlgoithm == 'vip':
        plt.ylabel("Likelihood")
        plt.xlabel("Mean of Vip ratio")
        plt.title("Start and stop number determination via CLT")
        plt.savefig(output_path + '/VipMean.png', bbox_inches="tight")
    elif V_rankingAlgoithm == "selectivity":
        plt.ylabel("Likelihood")
        plt.xlabel("Mean of Selectivity ratio")
        plt.title("Start and stop number determination via CLT")
        plt.savefig(output_path + '/SelectivityMean.png', bbox_inches="tight")
    plt.figure().clear()
    return startNum, endNum


# randomly get half sample, half variable matrix
# INPUT : sample data
# OUTPUT : random selected sample data, selected index
def selectHalfRandom(sample_list):
    idx_list = []
    rand_sample_list = []
    for i in range(len(sample_list)):
        idx_list.append(i)

    total_num = len(sample_list)
    half_num = total_num//2

    rand_idx_list = random.sample(list(idx_list),half_num)
    for idx in rand_idx_list:
        rand_sample_list.append(sample_list[idx])

    return rand_sample_list,rand_idx_list

# calculate the fisher ratio
# INPUT : sample data, class data, class number
# Output : dictionary of fisher ratio with key-variable index, value- fisher ratio
def cal_fish_ratio(sample_list,class_list,classNum):
    # define a fisher ratio list for all columns with default value 0
    fish_ratio = []
    # for each column sample type we calculate one fisher ratio for one column
    for i in range(len(sample_list[0])):
        #define a data list for all class
        # define a data list contain different class data list
        class_data = []
        for k in range(classNum + 1):
            class_data.append([])
        #for each row of data
        all_data = [row[i] for row in sample_list]
        for ind in range(len(all_data)):
            class_data[int(class_list[ind])].append(all_data[ind])
        class_data = [x for x in class_data if x != []]
        # Here we calculate the fisher ratio for that column
        # calculate the first lumda sqr
        all_data_mean = np.mean(all_data)
        lumdaTop1 = 0
        for z in range(len(class_data)):
            class_data_mean = np.mean(class_data[z])
            lumdaTop1 = lumdaTop1 + (((class_data_mean - all_data_mean)**2)*len(class_data[z]))
        lumdaBottom1 = classNum-1
        lumda1 = lumdaTop1/lumdaBottom1
        lumdaTop2_1 = 0
        for n in range(len(class_data)):
            for j in class_data[n]:
                lumdaTop2_1 = lumdaTop2_1 + (j - all_data_mean)**2
        lumdaTop2_2 = 0
        for p in range(len(class_data)):
            class_data_mean = 0
            for data in class_data[p]:
                class_data_mean = class_data_mean + data
            class_data_mean = class_data_mean/len(class_data[p])
            lumdaTop2_2 = lumdaTop2_2 + (((class_data_mean - all_data_mean) ** 2) * len(class_data[p]))
        lumdaBottom2 = len(all_data) - classNum
        lumda2 = (lumdaTop2_1-lumdaTop2_2)/lumdaBottom2
        fisher_ratio = lumda1/lumda2
        fish_ratio.append(fisher_ratio)
    fish_ratio = np.nan_to_num(fish_ratio, nan=(10 ** -12))
    return fish_ratio