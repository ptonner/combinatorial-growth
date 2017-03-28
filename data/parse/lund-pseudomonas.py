import pandas as pd
import numpy as np
import re, os
#
# dirs = ['PA01-acetic']
#
# for d in dirs:
#     if not d in os.listdir("data/normalized/lund/pseudomonas/"):
#         os.mkdir("data/normalized/lund/pseudomonas/"+d)

def parseFile(f,strain=None,header=0):

    pa = pd.read_excel(f,sheetname=None,header=header)
    useSheets = [s for s in pa.keys() if re.match('(pH ?[0-9.]+,? [0-7.]+ ?(mM)?)|(All pH 0 mM)',s)]

    data = meta = None

    # print useSheets

    for s in useSheets:

        m = re.match('pH ?([0-9.]+),? ([0-7.]+) ?(mM)?',s)

        if m:
            ph = m.group(1)
            la = m.group(2)
        else:
            ph = None
            la = 0

        temp = pa[s]
        #temp = temp.loc[:,['Time (hours)','Rep1','Rep2','Rep3']]

        if ph is None:
            temp = temp.iloc[:,:8]

            newmeta = pd.DataFrame([[ph,la]]*7,columns=['pH','mM-acid'])
            newmeta['pH'] = [7,6.5,6,5.5,5,4.5,4]
            newmeta['batch'] = 1
        else:
            temp = temp.iloc[:,:7]

            newmeta = pd.DataFrame([[ph,la]]*6,columns=['pH','mM-acid'])
            newmeta['batch'] = [0]*3 + [1]*3

        if not strain is None:
            newmeta['strain'] = strain

        if meta is None:
            meta = newmeta
        else:
            meta = pd.concat((meta,newmeta),0)

        if data is None:
            data = temp
        else:
            if header is None:
                data = pd.merge(data,temp,on=0)
            else:
                data = pd.merge(data,temp,on='Time (hours)')

    data.columns = ['time'] + range(data.shape[1]-1)
    meta.index = range(meta.shape[0])

    return data,meta

targets = [
        ('PA01 Acetic 15 min time points 14.10.16', 'PA01', 'acetic', 0),
        ('Propionic acid 15 min time points PA01 02.11.16', 'PA01', 'propionic', 0),
        ('PAB Lactic Acid (1)', 'PAB', 'lactic', 0),
        ('PA01 Lactic Acid (1)', 'PA01', 'lactic', 0),
        ('PA01 Butyric Acid 15 min time points 10.11.16', 'PA01', 'butyric', None),
        ('PA01 Potassium Sorbate 01.12.16', 'PA01', 'potassium-sorbate', None),
        ('PA1054 Acetic Acid', 'PA1054', 'acetic', None),
        ('PA1054 Propionic Acid', 'PA1054', 'propionic', None),
    ]

for f, strain, acid, header in targets:
    print f
    data,meta = parseFile("data/raw/lund/%s.xlsx"%f,strain=strain, header=header)

    meta['acid'] = acid
    meta['genus'] = 'pseudomonas'
    meta['strain'] = strain
    meta.index = range(meta.shape[0])

    d = "%s-%s"%(strain,acid)
    if not d in os.listdir("data/normalized/lund/pseudomonas/"):
        os.mkdir("data/normalized/lund/pseudomonas/"+d)

    data.to_csv("data/normalized/lund/pseudomonas/%s-%s/data.csv"%(strain, acid),index=False)
    meta.to_csv("data/normalized/lund/pseudomonas/%s-%s/meta.csv"%(strain, acid),index=False)

#
# data,meta = parseFile("data/raw/lund/PA01 Acetic 15 min time points 14.10.16.xlsx",strain='PA01')
# meta['acid'] = 'acetic'
# meta['genus'] = 'pseudomonas'
# meta['strain'] = 'PA01'
# meta.index = range(meta.shape[0])
#
# data.to_csv("data/normalized/lund/pseudomonas/PA01-acetic/data.csv",index=False)
# meta.to_csv("data/normalized/lund/pseudomonas/PA01-acetic/meta.csv",index=False)
#
#
# data2,meta2 = parseFile("data/raw/lund/Propionic acid 15 min time points PA01 02.11.16.xlsx",strain='PA1054')
# meta2['acid'] = 'propionic'
# meta['genus'] = 'pseudomonas'
# meta['strain'] = 'PA01'
#
# data = pd.merge(data,data2,on='time')
# meta = pd.concat((meta,meta2),0)
#
# data.columns = ['time'] + range(data.shape[1]-1)
# # data = data.iloc[4:,:]
# data.to_csv("data/normalized/lund/pseudomonas/data.csv",index=False)
#
# meta.index = range(meta.shape[0])
# meta.to_csv("data/normalized/lund/pseudomonas/meta.csv",index=False)

#
# data,meta = parseFile("data/raw/Propionic Acid - Fluostar E. coli.xlsx")
#
# data.columns = ['time'] + range(data.shape[1]-1)
# data = data.iloc[4:,:]
# data += 3e-2
# data.to_csv("ecoli-data.csv",index=False)
#
# meta.index = range(meta.shape[0])
# meta.to_csv("ecoli-meta.csv",index=False)
