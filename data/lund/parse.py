import pandas as pd
import os, re

thisDir = os.path.split(__file__)[0]
rawDir = os.path.join(thisDir,'raw')

fn = 'Propionic Acid - Fluostar E. coli.xlsx'
data = pd.ExcelFile(os.path.join(rawDir,fn))
# design = map(lambda x: re.match(u'pH([0-9.]+) ([0-9]+)mM',x).groups(), data.sheet_names[1:])

newdata = None
newmeta = None

for sn in data.sheet_names[1:]:
    ph,conc = re.match(u'pH([0-9.]+) ([0-9]+)mM',sn).groups()
    tempdata = pd.read_excel(os.path.join(rawDir,fn),sheetname=sn).iloc[:,:4]
    tempdata.columns=['time']+range(3)

    tempmeta = pd.DataFrame([[float(ph),float(conc)]]*3,columns=['pH','propionicAcidmM'])
    tempmeta['rep'] = range(3)

    if newdata is None:
        newdata = tempdata
        newmeta = tempmeta
    else:
        newdata = pd.merge(newdata,tempdata,on='time')
        newdata.columns = ['time']+range(newdata.shape[1]-1)
        newmeta = pd.concat((newmeta,tempmeta),ignore_index=True)

odir = 'propionicAcid-ecoli'
if not odir in os.listdir(thisDir):
    os.mkdir(os.path.join(thisDir,odir))

newdata.to_csv(os.path.join(thisDir,odir,'data.csv'))
newmeta.to_csv(os.path.join(thisDir,odir,'meta.csv'))

# dataset 2

fn = 'Clariostar same across plate E coli BW25113.xlsx'
data = pd.read_excel(os.path.join(rawDir,fn)).iloc[:,:-2]

meta = pd.DataFrame(data.columns[1:],columns=['position'])
data.columns = ['time'] + range(data.shape[1]-1)

odir = 'ecoli-replicate'
if not odir in os.listdir(thisDir):
    os.mkdir(os.path.join(thisDir,odir))

data.to_csv(os.path.join(thisDir,odir,'data.csv'))
meta.to_csv(os.path.join(thisDir,odir,'meta.csv'))
