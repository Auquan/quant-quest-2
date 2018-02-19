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
import pandas as pd


## Make your changes to the functions below.
## You only need to specify features you want to use in getInstrumentFeatureConfigDicts()
## and create your predictions using these features in getPrediction()
## Don't change any other function
## The toolbox does the rest for you, from downloading and loading data to running backtest

class MyTradingFunctions():

    def __init__(self):  #Put any global variables here
        self.count = 0
        self.params = {}

    ####################################
    ## FILL THESE THREE FUNCTIONS BELOW ##
    ####################################
    '''
    Specify the stock names that you want to trade.
    Make sure that there are atleast 10 stocks or your submission will not be evaluated by the submission portal.
    '''

    def getSymbolsToTrade(self):
        return ['AGW', 'CHV']
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
        rsiDict = {'featureKey': 'rsi_30',
                   'featureId': 'rsi',
                   'params': {'period': 30,
                              'featureName': 'stockVWAP'}}
        return [ma1Dict, ma2Dict, sdevDict, momDict, rsiDict]

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
        ###  TODO : FILL THIS FUNCTION TO RETURN A BUY (1) or SELL (0) prediction for each stock  ###
        ###  USE TEMPLATE BELOW AS EXAMPLE                                                        ###
        #############################################################################################

        # dataframe for a historical instrument feature (ma_5 in this case). The index is the timestamps
        # of upto lookback data points. The columns of this dataframe are the stock symbols/instrumentIds.
        ma5Data = lookbackInstrumentFeatures.getFeatureDf('ma_5')
        ma90Data = lookbackInstrumentFeatures.getFeatureDf('ma_90')
        sdevData = lookbackInstrumentFeatures.getFeatureDf('sdev_90')

        # Get the last row of the dataframe, the most recent datapoint
        if len(ma5Data.index) > 0:
            ma5 = ma5Data.iloc[-1]
            ma90 = ma90Data.iloc[-1]
            sdev = sdevData.iloc[-1]

            #create Zscore

            z_score = (ma5 - ma90)/sdev
            z_score[sdev==0] = 0


            predictions[z_score>1] = 0  #Sell the stock
            predictions[z_score<-1] = 1 #Buy the stock
            predictions[(z_score<1) & (z_score>0.5)] = 0.25 # Don't sell but don't close existing positions either
            predictions[(z_score>-1) & (z_score<-0.5)] = 0.75 # Don't buy but don't close existing positions either
            predictions[(z_score>-.5) & (z_score<0.5)] = 0.5 # Close existing positions

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
        self.__dataSetId = 'trainingW5_trainingData'
        self.__instrumentIds = self.__tradingFunctions.getSymbolsToTrade()


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

    def getBenchmark(self):
        return 'SPY'

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
                'fees_and_spread': FeesCalculator,
                'benchmark_PnL': BuyHoldPnL}


    def getInstrumentFeatureConfigDicts(self):
        # ADD RELEVANT FEATURES HERE

        predictionDict = {'featureKey': 'prediction',
                                'featureId': 'prediction',
                                'params': {}}
        feesConfigDict = {'featureKey': 'fees',
                          'featureId': 'fees_and_spread',
                          'params': {}}
        profitlossConfigDict = {'featureKey': 'pnl',
                                'featureId': 'pnl',
                                'params': {'price': self.getPriceFeatureKey(),
                                           'fees': 'fees'}}
        capitalConfigDict = {'featureKey': 'capital',
                             'featureId': 'capital',
                             'params': {'price': 'stockVWAP',
                                        'fees': 'fees',
                                        'capitalReqPercent': 0.95}}
        benchmarkDict = {'featureKey': 'benchmark',
                     'featureId': 'benchmark_PnL',
                     'params': {'pnlKey': 'pnl'}}
        scoreDict = {'featureKey': 'score',
                     'featureId': 'ratio',
                     'params': {'featureName1': 'pnl',
                                'featureName2':'benchmark'}}

        stockFeatureConfigs = self.__tradingFunctions.getInstrumentFeatureConfigDicts()


        return {INSTRUMENT_TYPE_STOCK: stockFeatureConfigs + [predictionDict,
         feesConfigDict,profitlossConfigDict,capitalConfigDict,benchmarkDict, scoreDict]}

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
                     'featureId': 'score_ll',
                     'params': {'featureName': self.getPriceFeatureKey(),
                                'instrument_score_feature': 'score'}}
        return [scoreDict]


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
                                 longLimit=1,
                                 shortLimit=1,
                                 capitalUsageLimit=0.10 * self.getStartingCapital(),
                                 lotSize=1)

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
        return 120


    def getPriceFeatureKey(self):
        return 'stockVWAP'

    def getDataSetId(self):
        return self.__dataSetId

    def setDataSetId(self, dataSetId):
        self.__dataSetId = dataSetId

    def getInstrumentsIds(self):
        return self.__instrumentIds


class TrainingPredictionFeature(Feature):

    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        tf = MyTradingFunctions()
        t= MyTradingParams(tf)
        return t.getPrediction(time, updateNum, instrumentManager)

class FeesCalculator(Feature):

    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()

        priceData = instrumentLookbackData.getFeatureDf('stockVWAP')
        fees = pd.Series(0.05,index = instrumentManager.getAllInstrumentsByInstrumentId())
        if len(priceData)>1:
            fees += 0.0001*priceData[-1]

        return fees



class BuyHoldPnL(Feature):
    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()

        priceData = instrumentLookbackData.getFeatureDf('stockVWAP')
        bhpnl = pd.Series(0,index = instrumentManager.getAllInstrumentsByInstrumentId())
        if len(priceData)>1:
            bhpnl += priceData[-1] - priceData[-2]

        return bhpnl


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