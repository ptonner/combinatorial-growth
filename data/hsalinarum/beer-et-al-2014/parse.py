import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

from datetime import timedelta

thisDir = os.path.split(__file__)[0]
data_dir = os.path.join(thisDir,'raw')

plates = os.listdir(data_dir)
plates = filter(lambda x: not 'csv' in x,plates)

combined = pd.DataFrame()
key = pd.DataFrame()
data = pd.DataFrame()

for p in plates:
    files = os.listdir(os.path.join(data_dir,p))

    database = pd.read_csv(os.path.join(data_dir,p,"DatabaseKB"+p[:-2]+".txt"))
    if database.shape[1] == 1:
        database = pd.read_csv(os.path.join(data_dir,p,"DatabaseKB"+p[:-2]+".txt"),sep="\t")
    database['plate'] = p

    result = pd.read_csv(os.path.join(data_dir,p,"ResultsKB"+p[:-2]+".csv"),index_col=False)

    # if there is an unnamed index before time column, delete it
    if result.columns[0] != 'Time':
        del result[result.columns[0]]

    result.columns = ['Time'] + result.columns[1:].str.extract("Well[ .]?([0-9]*)").tolist()

    # convert times to hour values using the timedelta fxn
    tdelt = result.Time.str.split(":").apply(lambda x: timedelta(hours=int(x[0]), minutes=int(x[1]), seconds=int(x[2])))
    tdelt = tdelt - tdelt.values[0]
    tdelt = tdelt/np.timedelta64(1,'h') # convert to hours
    tdelt = tdelt.round(1)
    result['Time'] = tdelt

    # merge results and database
    database['Well'] = result.columns[1:]
    merged = pd.merge(database,result.iloc[:,1:].T,left_on='Well',right_index=True)
    merged.columns = merged.columns[:database.shape[1]].tolist() + result.Time.tolist()

    merged.to_csv(os.path.join(data_dir,p+'_merged.csv'),index=False)
    result.to_csv(os.path.join(data_dir,p+'_data.csv'),index=False)
    database.to_csv(os.path.join(data_dir,p+'_design.csv'),index=False)

    if combined.shape[0]==0:
        combined = merged
        key = database
        data = result
    else:
        combined = combined.append(merged)
        key = key.append(database)

        result.index = range(data.shape[0],data.shape[0]+result.shape[0])
        data = data.append(result)
    print p,data.shape, key.shape

# this is the first column that isn't a data measurement
time_ind = combined.columns.tolist().index('Arg.Concentration')

data = combined.iloc[:,:time_ind].T
meta = combined.iloc[:,time_ind:]

data = np.log2(data)

data.to_csv(os.path.join(thisDir,'data.csv'))
meta.to_csv(os.path.join(thisDir,'meta.csv'),index=False)

# combined.iloc[:,:time_ind] = np.log2(combined.iloc[:,:time_ind])
