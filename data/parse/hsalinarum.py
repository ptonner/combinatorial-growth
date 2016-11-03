import pandas as pd
import os, re, datetime, time

#thisDir = os.path.split(__file__)[0]
thisDir = 'hsalinarum'
fn = '20161010PQ_osmo.csv'

data = pd.read_csv(os.path.join('data','raw',thisDir,fn),encoding='utf-16')

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

odir = 'gradientTest-1'
if not odir in os.listdir(os.path.join('data','normalized',thisDir)):
    os.mkdir(os.path.join('data','normalized',thisDir,odir))


data.to_csv(os.path.join('data','normalized',thisDir,'gradientTest-1','data.csv'),index=False)

fn = '20161010PQ_osmo_key.xlsx'
meta = pd.read_excel(os.path.join('data','raw',thisDir,fn))
meta.to_csv(os.path.join('data','normalized',thisDir,'gradientTest-1','meta.csv'),index=False)
