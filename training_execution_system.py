from backtester.executionSystem.base_execution_system import BaseExecutionSystem, InstrumentExection
from backtester.logger import *
import numpy as np
import pandas as pd


class TrainingExecutionSystem(SimpleExecutionSystem):
    def __init__(self, enter_threshold=0.7, exit_threshold=0.55, longLimit=10,
                 shortLimit=10, capitalUsageLimit=0, enterlotSize=1, exitlotSize = 1, limitType='L', price=''):
        super(TrainingExecutionSystem, self).__init__(enter_threshold=enter_threshold,
                                                    exit_threshold=exit_threshold,
                                                    longLimit=longLimit, shortLimit=shortLimit,
                                                    capitalUsageLimit=capitalUsageLimit,
                                                    enterlotSize=enterlotSize, exitlotSize=exitlotSize, 
                                                    limitType=limitType, price=price)


''' If you want to use FairValue Based execution, use the below Class definition
class TrainingExecutionSystem(SimpleExecutionSystemWithFairValue):
    def __init__(self, enter_threshold=0.2, exit_threshold=0.05, longLimit=10,
                 shortLimit=10, capitalUsageLimit=0, enterlotSize=1, exitlotSize = 1, limitType='L', price=''):
        super(TrainingExecutionSystem, self).__init__(enter_threshold_deviation=enter_threshold,
                                                   exit_threshold_deviation=exit_threshold,
                                                   longLimit=longLimit, shortLimit=shortLimit,
                                                    capitalUsageLimit=capitalUsageLimit,
                                                    enterlotSize=enterlotSize, exitlotSize=exitlotSize, 
                                                    limitType=limitType, price=price)

        '''

        self.params = {}

    '''The following functions are implemented in base class. 
        The arguments they take are also mentioned.
        You can write your custom implementation here if you like.

    ## getLongLimit(self, instrumentIds, price):
    ##      returns a pandas series with longlimit for each intrument

    ## getShortLimit(self, instrumentIds, price):
    ##      returns a pandas series with shortlimit for each intrument
    
    ## getEnterLotSize(self, instrumentIds, price):
    ##      returns a pandas series with TradingLotSize for each intrument

    ## getExitLotSize(self, instrumentIds, price):

    ## convertLimit(self, df, price):
    ##      converts limits, lotsizes etc from dollar terms to position terms if they are in dollar terms

    ## exitPosition(self, time, instrumentsManager, currentPredictions, closeAllPositions=False):
    ##      return execution where exit and hack condition is met
    ##      executions is a series with stocknames as index and positions to execute as column (-10 means sell 10)


    ## enterPosition(self, time, instrumentsManager, currentPredictions, capital):
    ##      return execution where enter condition is met

    ## atPositionLimit(self, capital, positionData, price):
    ##      check if we are at any position limit

    ## getExecutions(self, time, instrumentsManager, capital):
    ##      return the sum of all enter and exit executions
        

    ## getExecutionsAtClose(self, time, instrumentsManager):
    ##      close leftover positions at the end of Trading

    '''

    ##### IMPLEMENT THE FUNCTIONS BELOW ###

    def getBuySell(self, currentPredictions, instrumentsManager):
        ''' returns the sign of enter trade'''
        
        return np.sign(currentPredictions - 0.5)

    def enterCondition(self, currentPredictions, instrumentsManager):
        '''Checks if enter condition is met'''

        return (currentPredictions - 0.5).abs() > (self.enter_threshold - 0.5)

    def exitCondition(self, currentPredictions, instrumentsManager):
        '''Checks if exit condition is met'''
        
        return (currentPredictions - 0.5).abs() < (self.exit_threshold - 0.5)

    def hackCondition(self, currentPredictions, instrumentsManager):
        '''Checks if hackcondition is met'''

        return pd.Series(False, index=currentPredictions.index)
