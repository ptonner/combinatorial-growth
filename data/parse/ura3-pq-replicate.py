import pandas as pd
import os, re, datetime, time

thisDir = 'ura3-pq-replicate'
fn = 'PQ_test.csv'

data = pd.read_csv(os.path.join('data','raw',thisDir,fn))

def convert_time(x):
    delta = datetime.datetime(*x[:-2]) - datetime.datetime(*t[0][:-2])
    return 24*delta.days + float(delta.seconds)/3600

def parse_time(t):
	try:
		return time.struct_time(time.strptime(t,'%H:%M:%S'))
	except ValueError, e:
		try:
			t = time.strptime(t,'%d %H:%M:%S')
			t = list(t)
			t[2]+=1
			return time.struct_time(t)
		except ValueError, e:
			raise Exception("Time format unknown")

t = data['Time'].apply(parse_time)
t = t.apply(convert_time).round(2)
data['Time'] = t

del data['Blank']

data.to_csv(os.path.join('data','normalized',thisDir,'data.csv'),index=False)

# fn = 'PQ_test_key.csv'
# meta = pd.read_csv(os.path.join(thisDir,fn))
fn = 'PQ_test_key.xlsx'
meta = pd.read_excel(os.path.join('data','raw',thisDir,fn))

meta['mM_PQ'] = meta.Condition.str.extract('([0-9.]*)mM PQ')
meta.loc[meta['mM_PQ'].isnull(),'mM_PQ'] = 0
meta.to_csv(os.path.join('data','normalized',thisDir,'meta.csv'),index=False)
