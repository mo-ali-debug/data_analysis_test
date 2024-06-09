#%%#CODE FOR DATA ANALYST INTERVIEW
import pandas as pd
import numpy as np
import os
#always excute in cwd - place data files in code folder
from os.path import abspath, dirname
os.chdir(dirname(abspath(__file__)))

from pathlib import Path
from matplotlib import pyplot as plt

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


def NormaliseData(df):
    means = df.mean()
    for col in df:
        df[col] = df[col] - df[col].mean()
    return df


def plotAll(df):
    plt.figure()
    for col in df:
        x = np.arange(0 ,len(df[col]))
        y = df[col]
        #plt.xticks(x, my_xticks ,rotation = 45, fontsize =10)
        plt.plot(x, y , label = col)
        plt.grid(True)
        plt.xlabel('sample No')
        plt.ylabel('Value a.u')
        #plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        #plt.savefig('rollingMonth.png', dpi = 300 ,  bbox_inches='tight')


#path to data files
path = 'datasets/'
#read in datasets and concat as per file order
data = GetDataAndConcat(path)

#remove nan and 0 collumns from datafile
#datasts that contains nan are kept in droppedData dataframe
data, droppedData = RemoveNanAndZeros(data)

#baseline dataset
NormaliseData(data) 

plotAll(data)





# %%
