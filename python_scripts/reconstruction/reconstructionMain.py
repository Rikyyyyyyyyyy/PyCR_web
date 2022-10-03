from csv import reader
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from python_scripts.reconstruction import read_file


def csvreadline(file, outputfilename,local_path,pk):
    '''
    Reads the imported csv line by line and groups them into bactches of 3 rows
    The batches of 3 rows are then called with sort() to sort them into the finalized array
    '''
    rows = 0
    triplerow = []
    count = 0
    #  Opens the csv file in read mode
    file_path = read_file.getValFromFileByRows(file,local_path,pk)
    
    with open(file_path, 'r') as read_obj:
        csv_reader = reader(read_obj)  #  read line by line so only one line is in emmory at a time
        header = next(csv_reader)  # skips the header row at the top of the csv
        if header != None:
            for row in csv_reader:
                triplerow.append(row)  # appends row in memory to 'triple row'
                rows += 1
                if rows == 3:  #  if three rows are in it calls sort() and resets the triplerow container and row counter
                    sort(triplerow, outputfilename)
                    triplerow = []
                    rows = 0
                count +=1
                        
def sort(rows, outputfilename):
    '''
    This sorts the recieved 'triple row' into its repsective spot in the sorted array list
    For example sorted[10][42] represents the 11th aquisition at the (42+30) 72 m/z
    '''
    sorted_row = [0]*1200  #  makes the empty list of 0s for array
    count = 0
    row1 = rows[0]
    for item in rows[0]:
        if count > 1:
            if item != '':
                position = round(float(item)) - 30
                index = row1.index(item)
                value = rows[1][index]
                sorted_row[position] = value
        count += 1
    writeline(sorted_row, outputfilename)
        
def writeline(sorted_row, outputfilename):
    with open(outputfilename, 'a', newline= '') as f:
        writer = csv.writer(f)
        writer.writerow(sorted_row)
        
def reconstruct1D(matrixfile, modulation, acqusition,task_pk):
    mod = int(acqusition*modulation)
    mat = pd.read_csv(matrixfile).to_numpy()
    tl = np.mod(np.size(mat, axis=0), mod)
    tl = np.ceil(tl).astype(int)
    mat = mat[:-tl, :]
    tnsr = mat.reshape(int(np.size(mat, axis=0) / mod), mod, np.size(mat, axis=1))
    mat2 = np.sum(np.sum(tnsr, axis=1), axis=1)
    plt.plot(mat2, linewidth=0.75) #aspect='auto'
    plt.xlabel('Retention Time')
    plt.ylabel('Abundance')
    plt.savefig('static/images/reconstruct/output/output'+str(task_pk)+'.png',bbox_inches="tight")

def process(inputfilename, modulation, acquisition_rate,task_pk,local_path):
    outputfilename = 'static/images/reconstruct/temp/temp'+str(task_pk) + 'MatrixOutput.csv'
    # Reads raw data and converts to readable matrix
    csvreadline(inputfilename, outputfilename,local_path,task_pk)
    # Reads matrix and reconstucts 1D
    reconstruct1D(outputfilename, modulation, acquisition_rate,task_pk)  
    
def run1dreconstruct(inputFile,task_pk,local_path):
    print("Doing the work")
    modulation = 2.2  # Change this value to the modulation period in seconds
    acquisition_rate = 100  # Change this value to the acquisition rate in Hz
    process(inputFile, modulation, acquisition_rate,task_pk,local_path)    
