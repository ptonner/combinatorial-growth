import pandas as pd
import numpy as np
import re

def parseFile(f,strain=None):

	pa = pd.read_excel(f,sheetname=None)
	useSheets = [s for s in pa.keys() if re.match('(pH ?[0-9.]+,? [0-7.]+ ?(mM)?)|(All pH 0 mM)',s)]

	data = meta = None

	for s in useSheets:
		print s

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

			newmeta = pd.DataFrame([[ph,la]]*7,columns=['pH','mM lactic acid'])
			newmeta['pH'] = [7,6.5,6,5.5,5,4.5,4]
			newmeta['bio'] = 1
		else:
			temp = temp.iloc[:,:7]

			newmeta = pd.DataFrame([[ph,la]]*6,columns=['pH','mM lactic acid'])
			newmeta['bio'] = range(1,7)

		if not strain is None:
			newmeta['strain'] = strain

		if meta is None:
			meta = newmeta
		else:
			meta = pd.concat((meta,newmeta),0)

		if data is None:
			data = temp
		else:
			data = pd.merge(data,temp,on='Time (hours)')

	data.columns = ['time'] + range(data.shape[1]-1)
	meta.index = range(meta.shape[0])

	return data,meta

# data,meta = parseFile("data/raw/lund/PA01 Lactic Acid (1).xlsx",strain='PA01')
# data2,meta2 = parseFile("data/raw/lund/PAB Lactic Acid (1).xlsx",strain='PA1054')

# data = pd.merge(data,data2,on='time')
# meta = pd.concat((meta,meta2),0)

data,meta = parseFile("data/raw/lund/PA01 Acetic 15 min time points 14.10.16.xlsx",strain='PA01')

data.columns = ['time'] + range(data.shape[1]-1)
data = data.iloc[4:,:]
data.to_csv("data/normalized/lund/pseudomonas/data.csv",index=False)

meta.index = range(meta.shape[0])
meta.to_csv("data/normalized/lund/pseudomonas/meta.csv",index=False)
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
