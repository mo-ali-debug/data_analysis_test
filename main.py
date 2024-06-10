#%%#CODE FOR DATA ANALYST INTERVIEW
import pandas as pd
import numpy as np
import os
from pathlib import Path
from matplotlib import pyplot as plt
from scipy.signal import savgol_filter
from scipy.signal import find_peaks

#always excute in cwd - place data files in code folder
from os.path import abspath, dirname
os.chdir(dirname(abspath(__file__)))

def GetDataAndConcat(path):
    #list and sort files
    dflist = []
    files = os.listdir(path)
    if(len(files) == 0):
        print('Path contains no files')
        return

    files.sort()
    for file in files:
        if file.endswith('csv'):
            dflist.append(pd.read_csv(path+file))
    
    #return concatinated dataframes into one also transpose it.
    return pd.concat(dflist, ignore_index=True).transpose()


def RemoveNanAndZeros(df):
    intialNum = len(df.columns)
    print('Intial datasets = ' + str(intialNum))

    #collumns containing nan
    nanCollumnsNumbers = df.columns[df.isna().any()].tolist()
    droppedCollumns = df[nanCollumnsNumbers]
    #drop collumns in our live dataset
    df = df.dropna(axis=1)
    nonNanCollumns = len(df.columns)
    print('Number of columns with NaNs removed = ' + str(intialNum - nonNanCollumns))
    
    #find collumns that are 0, if the Standard deviation is 0 we can assume the entire collumn is 0.
    df  = df.loc[:, df.std() > 0]
    print('Number of empty columns removed = ' + str(nonNanCollumns - len(df.columns)))
    print("Final number of datasets = " +str(len(df.columns)))

    return df, droppedCollumns


def NormaliseDataAndSmooth(df):
    smootheddf = pd.DataFrame()
    for col in df:
        smootheddf[col] = df[col] - df[col].mean() #remove baseline
        smootheddf[col] = savgol_filter(smootheddf[col] ,17, 3) # window size 51, polynomial order 3
        smootheddf[col] = smootheddf[col]/abs(smootheddf[col]).max()
    return smootheddf

def plotANumberOfDatasets(df,numtoPlot):
    plt.figure()
    for i , col in enumerate(df):
        x = np.arange(0 ,len(df[col]))
        y = df[col]
        #plt.xticks(x, my_xticks ,rotation = 45, fontsize =10)
        plt.plot(x, y , label = col)
        plt.grid(True)
        plt.xlabel('sample No')
        plt.ylabel('Value a.u')
        plt.show()
        if (i == numtoPlot):
            break

def findandplotOnePeak(filteredData, datasetNo):
    #postive peak
    negativePeak = []
    filteredData = filteredData.reset_index(drop=True)
    # for col in filteredData:
    peaks, _ = find_peaks(abs(filteredData[datasetNo]), prominence=0.4)
    negativePeak.append(peaks)
    plt.plot(filteredData[datasetNo])
    plt.vlines(peaks, filteredData[datasetNo].min(), filteredData[datasetNo].max(), linestyles='dashed')
    plt.grid(True)
    plt.xlabel('sample No')
    plt.ylabel('Value a.u')
    plt.title('Dataset ' + str(datasetNo) + ' Peak sample locations 1 = '  + str(peaks[0])+ ' Peak 2 = '+ str(peaks[1]) )
    plt.savefig('findPeaks.png', dpi=200)    
    print(negativePeak)


def GetPeaksinData(filteredData):
    #postive peak
    peakFound = []
    filteredData = filteredData.reset_index(drop=True)
    for col in filteredData:
        peaks, _ = find_peaks(abs(filteredData[col]), prominence=0.4)
        peakFound.append(peaks)
    return peakFound

def GetStats(filteredData, numofPeaks):
    filteredData = filteredData.reset_index(drop=True)
    stats = pd.DataFrame()
    std = []
    mean = []
    pk2pk = []
    peakNo =[]
    for i , col in enumerate(filteredData):
        std.append(filteredData[col].std())
        mean.append(filteredData[col].mean())
        pk2pk.append(abs(filteredData[col].max() - filteredData[col].min()))
        peakNo.append(peaks[i])
    stats['Standard Deviation'] = std
    stats['Mean'] = mean
    stats['Peak-to-Peak'] = pk2pk
    stats['No of Peaks'] = peaks
    stats.to_csv('dataStats.csv')
    return stats


#path to data files
path = 'datasets/'

###############################################################
#DATA PREPERATION
#read in datasets and concat as per file order
data = GetDataAndConcat(path)

#remove nan and 0 collumns from datafile
#datasts that contains nan are kept in droppedData dataframe
data, droppedData = RemoveNanAndZeros(data)

#baseline datasets using mean values
filteredData = NormaliseDataAndSmooth(data) 

#plot 10 datasets to investiagate feetures
plotANumberOfDatasets(filteredData,10)
plotANumberOfDatasets(data,10)

###############################################################
#FEATURE EXTRACTION
#extract peaks

findandplotOnePeak(filteredData,801)
peaks = GetPeaksinData(filteredData)

#get some stats 
stats = GetStats(filteredData, peaks)
# %%
