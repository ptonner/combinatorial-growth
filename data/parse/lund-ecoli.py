import pandas as pd
import os, re

thisDir = 'lund'
rawDir = os.path.join('data','raw')

fn = 'Propionic Acid - Fluostar E. coli.xlsx'
data = pd.ExcelFile(os.path.join(rawDir,thisDir,fn))

newdata = None
newmeta = None

for sn in data.sheet_names[1:]:
    ph,conc = re.match(u'pH([0-9.]+) ([0-9]+)mM',sn).groups()
    # tempdata = pd.read_excel(os.path.join(rawDir,fn),sheetname=sn).iloc[:,:4]
    tempdata = pd.read_excel(os.path.join(rawDir,thisDir,fn),sheetname=sn).iloc[:,:4]
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
if not odir in os.listdir(os.path.join('data','normalized',thisDir)):
    os.mkdir(os.path.join('data','normalized',thisDir,odir))

newdata.to_csv(os.path.join('data','normalized',thisDir,odir,'data.csv'),index=False)
newmeta.to_csv(os.path.join('data','normalized',thisDir,odir,'meta.csv'),index=False)

# dataset 2

fn = 'Clariostar same across plate E coli BW25113.xlsx'
data = pd.read_excel(os.path.join(rawDir,thisDir,fn)).iloc[:,:-2]
data.columns = ['time'] + range(data.shape[1]-1)
data.time = 1.*data.time/60

meta = pd.DataFrame(data.columns[1:],columns=['position'])


odir = 'ecoli-replicate'
if not odir in os.listdir(os.path.join('data','normalized',thisDir)):
    os.mkdir(os.path.join('data','normalized',thisDir,odir))

data.to_csv(os.path.join('data','normalized',thisDir,odir,'data.csv'),index=False)
meta.to_csv(os.path.join('data','normalized',thisDir,odir,'meta.csv'),index=False)
