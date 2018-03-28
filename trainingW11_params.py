from backtester.trading_system_parameters import TradingSystemParameters
from backtester.features.feature import Feature
from datetime import timedelta
from backtester.dataSource.quant_quest_data_source import QuantQuestDataSource
# from backtester.timeRule.quant_quest_time_rule import QuantQuestTimeRule
from backtester.executionSystem.simple_execution_system import SimpleExecutionSystem
from backtester.orderPlacer.backtesting_order_placer import BacktestingOrderPlacer
from backtester.trading_system import TradingSystem
from backtester.version import updateCheck
from backtester.constants import *
from backtester.features.feature import Feature
import pandas as pd
import numpy as np
import os

## Make your changes to the functions below.
## You need to specify features you want to use in getInstrumentFeatureConfigDicts()
## You need to specify ANY RATIO FEATURES you want to use in getMarketFeatureConfigDicts()
## and create your predictions using these features in getPrediction()
## Don't change any other function
## The toolbox does the rest for you, from downloading and loading data to running backtest

################################################
###    SPECIFY PATH TO EXECUTION FILE HERE   ###
################################################

import urllib

path_to_file = 'https://raw.githubusercontent.com/Auquan/quant-quest-2/master/training_execution_system.py'
fileName = 'training_execution_system.py'
if not os.path.isfile(fileName):
    urllib.urlretrieve (path_to_file, fileName)

from training_execution_system import TrainingExecutionSystem

####################################
###    SPECIFY THE PAIRS HERE    ###
####################################

PAIRIDS = {1 : ['AGW', 'FFA'],
           2 : ['CHV', 'GYJ']}


class MyTradingFunctions():

    def __init__(self):  #Put any global variables here
        self.count = 0
        self.params = {}


    def getSymbolsToTrade(self):
        return [stock for sublist in PAIRIDS.values() for stock in sublist]




    ####################################
    ## FILL THESE THREE FUNCTIONS BELOW ##
    ####################################

    '''
    Specify all Features you want to use by  by creating config dictionaries.
    Create one dictionary per feature and return them in an array.

    Feature config Dictionary have the following keys:

        featureId: a str for the type of feature you want to use
        featureKey: {optional} a str for the key you will use to call this feature
                    If not present, will just use featureId
        params: {optional} A dictionary with which contains other optional params if needed by the feature

    msDict = {'featureKey': 'ms_5',
              'featureId': 'moving_sum',
              'params': {'period': 5,
                         'featureName': 'basis'}}

    return [msDict]

    You can now use this feature by in getPRediction() calling it's featureKey, 'ms_5'
    '''

    def getInstrumentFeatureConfigDicts(self):

        #############################################################################
        ### TODO: FILL THIS FUNCTION TO CREATE DESIRED FEATURES for each stock.   ###
        ### USE TEMPLATE BELOW AS EXAMPLE                                         ###
        #############################################################################
        ma1Dict = {'featureKey': 'ma_90',
                   'featureId': 'moving_average',
                   'params': {'period': 90,
                              'featureName': 'stockVWAP'}}
        ma2Dict = {'featureKey': 'ma_5',
                   'featureId': 'moving_average',
                   'params': {'period': 5,
                              'featureName': 'stockVWAP'}}
        sdevDict = {'featureKey': 'sdev_90',
                    'featureId': 'moving_sdev',
                    'params': {'period': 90,
                               'featureName': 'stockVWAP'}}
        momDict = {'featureKey': 'mom_90',
                   'featureId': 'momentum',
                   'params': {'period': 30,
                              'featureName': 'stockVWAP'}}
        return [ma1Dict, ma2Dict, sdevDict, momDict]



    def getMarketFeatureConfigDicts(self):
        #############################################################################
        ### TODO: FILL THIS FUNCTION TO CREATE a ratio feature                    ###
        ### AND DESIRED FEATURES for each ratio.                                  ###
        ### USE TEMPLATE BELOW AS EXAMPLE                                         ###
        #############################################################################

        ratio1Dict = {'featureKey': 'ratio1',
                     'featureId': 'ratio',
                     'params': {'instrumentId1': PAIRIDS[1][0],
                                'instrumentId2': PAIRIDS[1][1],
                                'featureName': 'stockVWAP'}}
        ratio2Dict = {'featureKey': 'ratio2',
                     'featureId': 'ratio',
                     'params': {'instrumentId1': PAIRIDS[2][0],
                                'instrumentId2': PAIRIDS[2][1],
                                'featureName': 'stockVWAP'}}
        ma11Dict = {'featureKey': 'ma_r1_90',
                   'featureId': 'moving_average',
                   'params': {'period': 90,
                              'featureName': 'ratio1'}}
        ma21Dict = {'featureKey': 'ma_r1_10',
                   'featureId': 'moving_average',
                   'params': {'period': 10,
                              'featureName': 'ratio1'}}
        sdev1Dict = {'featureKey': 'sdev_r1_90',
                    'featureId': 'moving_sdev',
                    'params': {'period': 90,
                               'featureName': 'ratio1'}}
        ma12Dict = {'featureKey': 'ma_r2_90',
                   'featureId': 'moving_average',
                   'params': {'period': 90,
                              'featureName': 'ratio2'}}
        ma22Dict = {'featureKey': 'ma_r2_10',
                   'featureId': 'moving_average',
                   'params': {'period': 10,
                              'featureName': 'ratio2'}}
        sdev2Dict = {'featureKey': 'sdev_r2_90',
                    'featureId': 'moving_sdev',
                    'params': {'period': 90,
                               'featureName': 'ratio2'}}
        correl1Dict = {'featureKey': 'correl_r1_90',
                    'featureId': 'cross_instrument_correlation',
                    'params': {'period': 90,
                               'instrumentId1': PAIRIDS[1][0],
                                'instrumentId2': PAIRIDS[1][1],
                                'featureName': 'stockVWAP'}}
        correl2Dict = {'featureKey': 'correl_r2_90',
                    'featureId': 'cross_instrument_correlation',
                    'params': {'period': 90,
                               'instrumentId1': PAIRIDS[2][0],
                                'instrumentId2': PAIRIDS[2][1],
                                'featureName': 'stockVWAP'}}
        
        # customFeatureDict = {'featureKey': 'custom_mrkt_feature',
        #                      'featureId': 'my_custom_mrkt_feature',
        #                      'params': {'param1': 'value1'}}
        return [ratio1Dict, ma11Dict, ma21Dict, sdev1Dict, correl1Dict, 
                ratio2Dict, ma12Dict, ma22Dict, sdev2Dict, correl2Dict]

    '''
    Combine all the features to create the desired predictions for each stock.
    'predictions' is Pandas Series with stock as index and predictions as values
    We first call the holder for all the instrument features for all stocks as
        lookbackInstrumentFeatures = instrumentManager.getLookbackInstrumentFeatures()
    Then call the dataframe for a feature using its feature_key as
        ms5Data = lookbackInstrumentFeatures.getFeatureDf('ms_5')
    This returns a dataFrame for that feature for ALL stocks for all times upto lookback time
    Now you can call just the last data point for ALL stocks as
        ms5 = ms5Data.iloc[-1]
    You can call last datapoint for one stock 'ABC' as
        value_for_abs = ms5['ABC']

    Output of the prediction function is used by the toolbox to make further trading decisions and evaluate your score.
    '''


    def getPrediction(self, time, updateNum, instrumentManager, predictions):

        # self.updateCount() - uncomment if you want a counter
        # holder for all the instrument features for all instruments
        lookbackInstrumentFeatures = instrumentManager.getLookbackInstrumentFeatures()

        #############################################################################################
        ###  TODO : FILL THIS FUNCTION TO RETURN A BUY (1) or SELL (0) prediction for each pair   ###
        ###  USE TEMPLATE BELOW AS EXAMPLE                                                        ###
        #############################################################################################

        lookbackMarketFeatures = instrumentManager.getDataDf()
        
        if len(lookbackMarketFeatures)>0:
            currentMarketFeatures = lookbackMarketFeatures.iloc[-1]
            # IMPLEMENT THIS
            z_score = pd.Series(index = PAIRIDS.keys())
            for i in PAIRIDS.keys():
                if currentMarketFeatures['sdev_r%s_90'%i] != 0:
                  z_score[i] = (currentMarketFeatures['ma_r%s_10'%i] - currentMarketFeatures['ma_r%s_90'%i]) / currentMarketFeatures['sdev_r%s_90'%i]
                else:
                  z_score[i] = 0
                #z_score = z_score + instrument.getDataDf()['position']/20000

                if currentMarketFeatures['correl_r%s_90'%i] < 0.5:
                  z_score[i] = 0


                if z_score[i] > 1:
                    print(i, z_score[i], ' is greater than 1')
                    predictions[PAIRIDS[i][0]] = 0
                    predictions[PAIRIDS[i][1]] = 1
                elif z_score[i] < -1:
                    print(i, z_score[i], ' is less than -1')
                    predictions[PAIRIDS[i][0]] = 1
                    predictions[PAIRIDS[i][1]] = 0
                elif (z_score[i] > 0.5) or (z_score[i] < -0.5) :
                    print(i, z_score[i], ' is less than -0.5 or greater than 0.5')
                    predictions[PAIRIDS[i][0]] = 0.75
                    predictions[PAIRIDS[i][1]] = 0.25
                else:
                    print(i, z_score[i], ' is between -0.5 and 0.5')
                    predictions[PAIRIDS[i][0]] = 0.5
                    predictions[PAIRIDS[i][1]] = 0.5

        return predictions


    def updateCount(self):
        self.count = self.count + 1

class MyCustomFeature(Feature):
    ''''
    Custom Feature to implement for instrument. This function would return the value of the feature you want to implement.
    1. create a new class MyCustomFeatureClassName for the feature and implement your logic in the function computeForInstrument() -

    2. modify function getCustomFeatures() to return a dictionary with Id for this class
        (follow formats like {'my_custom_feature_identifier': MyCustomFeatureClassName}.
        Make sure 'my_custom_feature_identifier' doesnt conflict with any of the pre defined feature Ids

        def getCustomFeatures(self):
            return {'my_custom_feature_identifier': MyCustomFeatureClassName}

    3. create a dict for this feature in getInstrumentFeatureConfigDicts() above. Dict format is:
            customFeatureDict = {'featureKey': 'my_custom_feature_key',
                                'featureId': 'my_custom_feature_identifier',
                                'params': {'param1': 'value1'}}
    You can now use this feature by calling it's featureKey, 'my_custom_feature_key' in getPrediction()
    '''
    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        # Custom parameter which can be used as input to computation of this feature
        param1Value = featureParams['param1']

        # A holder for the all the instrument features
        lookbackInstrumentFeatures = instrumentManager.getLookbackInstrumentFeatures()

        # dataframe for a historical instrument feature (basis in this case). The index is the timestamps
        # atmost upto lookback data points. The columns of this dataframe are the stocks/instrumentIds.
        lookbackInstrumentValue = lookbackInstrumentFeatures.getFeatureDf('stockVWAP')

        # The last row of the previous dataframe gives the last calculated value for that feature (basis in this case)
        # This returns a series with stocks/instrumentIds as the index.
        currentValue = lookbackInstrumentValue.iloc[-1]

        if param1Value == 'value1':
            return currentValue * 0.1
        else:
            return currentValue * 0.5


class MyTradingParams(TradingSystemParameters):
    '''
    initialize class
    place any global variables here
    '''
    def __init__(self, tradingFunctions):
        self.__tradingFunctions = tradingFunctions
        super(MyTradingParams, self).__init__()
        self.__dataSetId = 'trainingW9_trainingData'
        self.__instrumentIds = self.__tradingFunctions.getSymbolsToTrade()
        self.__capitalMultiplier = 10


    '''
    Returns an instance of class DataParser. Source of data for instruments
    '''

    def getDataParser(self):
        instrumentIds = self.__tradingFunctions.getSymbolsToTrade()
        return QuantQuestDataSource(cachedFolderName='historicalData/',
                                    dataSetId=self.__dataSetId,
                                    instrumentIds=instrumentIds)

    '''
    Returns an instance of class TimeRule, which describes the times at which
    we should update all the features and try to execute any trades based on
    execution logic.
    For eg, for intra day data, you might have a system, where you get data
    from exchange at a very fast rate (ie multiple times every second). However,
    you might want to run your logic of computing features or running your execution
    system, only at some fixed intervals (like once every 5 seconds). This depends on your
    strategy whether its a high, medium, low frequency trading strategy. Also, performance
    is another concern. if your execution system and features computation are taking
    a lot of time, you realistically wont be able to keep upto pace.
    '''
    def getTimeRuleForUpdates(self):
        return QuantQuestTimeRule(cachedFolderName='historicalData/',
                                  dataSetId=self.__dataSetId)

    '''
    Returns a timedetla object to indicate frequency of updates to features
    Any updates within this frequncy to instruments do not trigger feature updates.
    Consequently any trading decisions that need to take place happen with the same
    frequency
    '''

    def getFrequencyOfFeatureUpdates(self):
        return timedelta(0, 30)  # minutes, seconds

    def getStartingCapital(self):
        return 1000*self.__capitalMultiplier

    '''
    This is a way to use any custom features you might have made.
    Returns a dictionary where
    key: featureId to access this feature (Make sure this doesnt conflict with any of the pre defined feature Ids)
    value: Your custom Class which computes this feature. The class should be an instance of Feature
    Eg. if your custom class is MyCustomFeature, and you want to access this via featureId='my_custom_feature',
    you will import that class, and return this function as {'my_custom_feature': MyCustomFeature}
    '''

    def getCustomFeatures(self):
        return {'my_custom_feature': MyCustomFeature,
                'prediction': TrainingPredictionFeature,
                'spread': SpreadCalculator,
                'fees_and_spread': FeesCalculator,
                'Sharpe': SharpeCalculator}


    def getInstrumentFeatureConfigDicts(self):
        # ADD RELEVANT FEATURES HERE

        predictionDict = {'featureKey': 'prediction',
                                'featureId': 'prediction',
                                'params': {}}
        spreadConfigDict = {'featureKey': 'spread',
                            'featureId': 'spread',
                            'params': {'instrbid': 'Bid Price',
                                       'instrask': 'Ask Price'}}
        feesConfigDict = {'featureKey': 'fees',
                          'featureId': 'fees_and_spread',
                          'params': self.setFees()}
        profitlossConfigDict = {'featureKey': 'pnl',
                                'featureId': 'pnl',
                                'params': {'price': self.getPriceFeatureKey(),
                                           'fees': 'fees'}}
        capitalConfigDict = {'featureKey': 'capital',
                             'featureId': 'capital',
                             'params': {'price': 'stockVWAP',
                                        'fees': 'fees',
                                        'capitalReqPercent': 0.95}}


        stockFeatureConfigs = self.__tradingFunctions.getInstrumentFeatureConfigDicts()


        return {INSTRUMENT_TYPE_STOCK: stockFeatureConfigs + [predictionDict,
        spreadConfigDict, feesConfigDict,profitlossConfigDict,capitalConfigDict]}

    '''
    Returns an array of market feature config dictionaries
        market feature config Dictionary has the following keys:
        featureId: a string representing the type of feature you want to use
        featureKey: a string representing the key you will use to access the value of this feature.this
        params: A dictionary with which contains other optional params if needed by the feature
    '''

    def getMarketFeatureConfigDicts(self):
    # ADD RELEVANT FEATURES HERE
        scoreDict = {'featureKey': 'score',
                     'featureId': 'Sharpe',
                     'params': {}}

        marketFeatureConfigs = self.__tradingFunctions.getMarketFeatureConfigDicts()
        return marketFeatureConfigs + [scoreDict]


    def getPrediction(self, time, updateNum, instrumentManager):

        predictions = pd.Series(index = self.__instrumentIds)

        predictions = self.__tradingFunctions.getPrediction(time, updateNum, instrumentManager, predictions)

        return predictions

    '''
    Returns the type of execution system we want to use. Its an implementation of the class ExecutionSystem
    It converts prediction to intended positions for different instruments.
    '''

    def getExecutionSystem(self):
        return SimpleExecutionSystem(enter_threshold=0.7, 
                                    exit_threshold=0.55, 
                                    longLimit=10000,
                                    shortLimit=10000, 
                                    capitalUsageLimit=0.10 * self.getStartingCapital(), 
                                    lotSize = 10000, 
                                    limitType='D', price='stockVWAP')

    '''
    Returns the type of order placer we want to use. its an implementation of the class OrderPlacer.
    It helps place an order, and also read confirmations of orders being placed.
    For Backtesting, you can just use the BacktestingOrderPlacer, which places the order which you want, and automatically confirms it too.
    '''

    def getOrderPlacer(self):
        return BacktestingOrderPlacer()

    '''
    Returns the amount of lookback data you want for your calculations. The historical market features and instrument features are only
    stored upto this amount.
    This number is the number of times we have updated our features.
    '''

    def getLookbackSize(self):
        return 360


    def getPriceFeatureKey(self):
        return 'stockVWAP'

    def getDataSetId(self):
        return self.__dataSetId

    def setDataSetId(self, dataSetId):
        self.__dataSetId = dataSetId

    def getInstrumentsIds(self):
        return self.__instrumentIds

    def setFees(self):
        return {'brokerage': 0.0001,'spread': 'spread'}

    def setCapital(self, capital):
        self.__capitalMultiplier = 5000



class TrainingPredictionFeature(Feature):

    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        tf = MyTradingFunctions()
        t= MyTradingParams(tf)
        return t.getPrediction(time, updateNum, instrumentManager)


class SpreadCalculator(Feature):

    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        try:
            currentStockBidPrice = instrumentLookbackData.getFeatureDf(featureParams['instrbid']).iloc[-1]
            currentStockAskPrice = instrumentLookbackData.getFeatureDf(featureParams['instrask']).iloc[-1]
        except KeyError:
            logError('Bid and Ask Price Feature Key does not exist')

        currentSpread = currentStockAskPrice - currentStockBidPrice
        return currentSpread / 2.0


class FeesCalculator(Feature):

    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()

        priceData = instrumentLookbackData.getFeatureDf('stockVWAP')
        positionData = instrumentLookbackData.getFeatureDf('position')
        currentPosition = positionData.iloc[-1]
        previousPosition = 0 if updateNum < 2 else positionData.iloc[-2]
        changeInPosition = currentPosition - previousPosition
        fees = pd.Series(np.abs(changeInPosition)*featureParams['brokerage'],index = instrumentManager.getAllInstrumentsByInstrumentId())
        if len(priceData)>1:
            currentPrice = priceData.iloc[-1]
        else:
            currentPrice = 0

        fees = fees*currentPrice + np.abs(changeInPosition)*instrumentLookbackData.getFeatureDf(featureParams['spread']).iloc[-1]
        return fees
        


class SharpeCalculator(Feature):
    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        lookbackMarketFeatures = instrumentManager.getDataDf()

        pnl = lookbackMarketFeatures['pnl'].iloc[-1]
        var = lookbackMarketFeatures['variance'].iloc[-1]
        if var !=0:
            sharpe = pnl/np.sqrt(var)
        else:
            sharpe = 0

        return 0


if __name__ == "__main__":
    if updateCheck():
        print('Your version of the auquan toolbox package is old. Please update by running the following command:')
        print('pip install -U auquan_toolbox')
    else:
        tf = MyTradingFunctions()
        tsParams = MyTradingParams(tf)
        tradingSystem = TradingSystem(tsParams)
    # Set onlyAnalyze to True to quickly generate csv files with all the features
    # Set onlyAnalyze to False to run a full backtest
    # Set makeInstrumentCsvs to False to not make instrument specific csvs in runLogs. This improves the performance BY A LOT
        tradingSystem.startTrading(onlyAnalyze=False, shouldPlot=True, makeInstrumentCsvs=True)