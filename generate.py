import pandas as pd
import numpy as np
import os
import sys
try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen

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
	print('Calculating for dataset %s and runLogs '%datasetId).join([str(x) for x in folders])
	
try:
	mktReturnsFileName = 'historicalData/%s/market_returns.csv'%datasetId
	if not os.path.isfile(mktReturnsFileName):
		url = 'https://raw.githubusercontent.com/Auquan/auquan-historical-data/master/qq2Data/%s/market_returns.csv' % (
			dataSetId)
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
		try:
			temp = pd.read_csv('runLogs/'+logFolder+'/marketFeatures.csv',index_col=0, parse_dates=True)
		except IOError:
			continue
		returns = temp['capital'].diff()/temp['capitalUsage'].max()
		returns.fillna(0, inplace=True)
		if returns.index.equals(mkt.index) or returns.index.isin(mkt.index).all():
			metrics = np.polyfit(mkt['returns'][returns.index].values, returns.values, 1)
			print('Alpha:%.3f%% Beta: %.3f'%(metrics[1]*100, metrics[0]) )

		else:
			print('Dates do not match. Not the same backtest')
except:
	print('Market Returns file not found')
