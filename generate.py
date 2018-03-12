import pandas as pd
import numpy as np
import os
import sys
try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen

from pandas.tseries.frequencies import to_offset
from functools import partial


def resampleData(series, period):
    return series.groupby(partial(round, freq=period))

def round(t, freq):
    freq = to_offset(freq)
    return pd.Timestamp((t.value // freq.delta.value) * freq.delta.value)

print('MAKE SURE you have specified the correct dataset and logFolder')
print('')
if len(sys.argv)==1:
	datasetId = 'trainingW5_trainingData'
	folders = next(os.walk('runLogs/'))[1]
	print('DatasetId and runLog folder not provided. Calculating for default dataset %s and all runLogs'%datasetId)
elif len(sys.argv)==2:
	datasetId = sys.argv[1]
	folders = next(os.walk('runLogs/'))[1]
	print('RunLog folder not provided. Calculating for dataset %s and all runLogs'%datasetId)
else:
	datasetId = sys.argv[1]
	folders = sys.argv[2:]
	print(('Calculating for dataset %s and runLogs '%datasetId).join([str(x) for x in folders]))
	
try:
	mktReturnsFileName = 'historicalData/%s/market_returns.csv'%datasetId
	if not (os.path.isfile(mktReturnsFileName)):
		url = 'https://raw.githubusercontent.com/Auquan/auquan-historical-data/master/qq2Data/%s/market_returns.csv' % (datasetId)
		print(url)
		response = urlopen(url)
		status = response.getcode()
		if status == 200:
			print('Downloading Market Returns to file: %s' % (mktReturnsFileName))
			with open(mktReturnsFileName, 'w') as f:
				f.write(response.read().decode('utf8'))
		else:
			print('File not found. Please check internet')
	mkt = pd.read_csv('historicalData/%s/market_returns.csv'%datasetId, index_col=0, parse_dates=True)

	data = None
	for logFolder in folders:
		print('Calculating Metrics for %s'%logFolder)
		temp = pd.read_csv('runLogs/'+logFolder+'/marketFeatures.csv',index_col=0, parse_dates=True)
		try:
			temp = pd.read_csv('runLogs/'+logFolder+'/marketFeatures.csv',index_col=0, parse_dates=True)
		except IOError:
			continue
		returns = temp['capital'].diff()/temp['capitalUsage'].max()
		returns.fillna(0, inplace=True)
		sampledreturns = resampleData(returns, '1D').last()
        sampledreturns[1:] = np.diff(sampledreturns)
        sampledreturns = sampledreturns/temp['capitalUsage'].max()
        
        cumret = (mkt['returns'] + 1).cumprod()
        sampledDf = resampleData(cumret, '1D').last()
        if sampledreturns.index.equals(sampledDf.index) or sampledreturns.index.isin(sampledDf.index).all():
            rets = (sampledDf/sampledDf.shift(1))-1
            rets[0] = mkt.iloc[0]
            metrics = np.polyfit(rets[sampledreturns.index].values, sampledreturns.values, 1)
            print('Alpha:%.3f%% Beta: %.3f'%(metrics[1]*100, metrics[0]) )
        else:
			print('Dates do not match. Not the same backtest')
except:
	print('Market Returns file not found')
