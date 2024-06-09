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
    smooteddf = pd.DataFrame()
    for col in df:
        smooteddf[col] = df[col] - df[col].mean() #remove baseline
        smooteddf[col] = smooteddf[col]/abs(smooteddf[col]).max()
        smooteddf[col] = savgol_filter(smooteddf[col] ,41, 3) # window size 51, polynomial order 3
    return smooteddf

# def findandPlotPeaks(filteredData, thresholdValue):
#     plt.figure()
#     for col in filteredData:
#         peaks = find_peaks(filteredData[col], height=(-thresholdValue, thresholdValue))
#         # plt.plot(-thresholdValue, "--", color="gray")
#         # plt.plot(thresholdValue, ":", color="gray")
#         plt.plot(filteredData[col])
#         for peak in peaks:
#             plt.plot(peaks[peak] , filteredData[col][peaks], 'X')


def plotAll(df,numtoPlot):
    plt.figure()
    for i , col in enumerate(df):
        x = np.arange(0 ,len(df[col]))
        y = df[col]
        #plt.xticks(x, my_xticks ,rotation = 45, fontsize =10)
        plt.plot(x, y , label = col)
        plt.grid(True)
        plt.xlabel('sample No')
        plt.ylabel('Value a.u')
        if (i == numtoPlot):
            break

        #plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        #plt.savefig('rollingMonth.png', dpi = 300 ,  bbox_inches='tight')



#%%
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

#plot 30 datasets to investiagate feetures
plotAll(filteredData,30)


###############################################################
#FEATURE EXTRACTION
#plot the max and min differtiated dataset to pick the transition points
def find_Transitions(filteredData,filestoplot):
    for i, col in enumerate(filteredData):
        plt.figure()
        max = filteredData[col].diff().idxmax()
        min = filteredData[col].diff().idxmin()
        plt.plot(filteredData[col])
        plt.axvline(max)
        plt.axvline(min)
        if (i == filestoplot):
            break
        





# %%
find_Transitions(filteredData,0)
# %%
