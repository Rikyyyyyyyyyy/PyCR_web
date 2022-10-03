from ctypes import sizeof
from queue import Full
import pandas as pd
import csv
import os
import numpy as np
import warnings
import shutil
import urllib.request
import boto3
warnings.filterwarnings('ignore')

def getValFromFileByRows(fileName,local_path,pk):
    BUCKETNAME = 'pycr'
    s3 = boto3.client('s3')
    full_local_path = str(local_path)+'/static/images/reconstruct/temp_input/temp_input'+str(pk)+'.csv'
    # print(full_path_filename)
    # file = urllib.request.urlopen(full_path_filename)
    # df = pd.read_csv(file,header=None)
    # row_count, column_count = df.shape
    # retData = []
    # counter=0
    # for row in range(1,row_count):
    #     print("reading"+str(counter)+"...")
    #     tempData = []
    #     counter+=1
    #     for col in range(column_count):
    #         tempData.append(float(df.iloc[row][col]))
    #     retData.append(tempData)
    s3.download_file(BUCKETNAME, fileName, full_local_path)
    return full_local_path