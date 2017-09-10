# Official Page for  [Quant Quest Competition](http://quant-quest.auquan.com) hosted by Auquan.

## Trading Problem Overview ##
This problem requires a mix of statistics and data analysis skills to create a predictive model using financial data. We will provide you with a toolbox and historical data to develop and test your strategy for the competition.

[TOC]

## Quick Startup Guide ##
### Install Python and dependent packages ### 
You need Python 2.7 (Python 3 will be supported later) to run this toolbox. For an easy installation process, we recommend Anaconda since it will reliably install all the necessary dependencies. Download [Anaconda](http://continuum.io/downloads) and follow the instructions on the [installation page](http://docs.continuum.io/anaconda/install).   Once you have Python, you can then install the toolbox.

### Get the Quant Quest Toolbox ###
There are multiple ways to install the toolbox for the competition.

The easiest way and the most recommended way is via pip. Just run the following command:
`pip install -U auquan_toolbox`
If we publish any updates to the toolbox, the same command `pip install -U auquan_toolbox` will also automatically get the new version of the toolbox. 

### Download [Problem1.py] (https://github.com/Auquan/quant-quest-2/blob/master/problem1.py) 
Run the following command to make sure everything is setup properly

        python problem1.py

### Make your changes
Use *problem1.py* as a template which contains skeleton functions (with explanation) that need to be filled in to create your own trading strategy. You need to fill in the getFairValue function for problem 1. 

## How does the toolbox work? ##

The data for the competition is provided here. The toolbox autodownloads and loads the data for you. You then need to create features and combine them in the prediction function to generate your predictions. 

Features and predictions are explained below. The toolbox also provides extensive functionality and customization. While not required for the competition,you can read more about the toolbox [here](https://bitbucket.org/auquan/auquantoolbox/wiki/Home)

### Creating Features ##
Features can be called by specifying config dictionaries. Create one dictionary per feature and return them in a dictionary as market features or instrument features.
Instrument features are calculated per instrument (for example position, fees, moving average of instrument price) and market features are calculated for whole trading system (for example portfolio value, total pnl)

Feature config Dictionary has the following keys:
  > *featureId:* a string representing the type of feature you want to use  
  > *featureKey:* {optional} a string representing the key you will use to access the value of this feature  
  >            If not present, will just use featureId  
  > *params:* {optional} A dictionary with which contains other optional params if needed by the feature  
        
Full list of features is available [here](https://bitbucket.org/auquan/auquantoolbox/src/master/backtester/features/README.md).

To use your own custom features(you need to create them separately using this [template](https://bitbucket.org/auquan/auquantoolbox/src/master/my_custom_feature.py), return a dictionary where
  > *key:* featureId to access this feature (Make sure this doesnt conflict with any of the pre defined feature Ids)  
  > *value:* Your custom Class which computes this feature. The class should be an instance of Feature  
  > Eg. if your custom class is MyCustomFeature, and you want to access this via featureId='my_custom_feature',  
  > you will import that class, and return this function as {'my_custom_feature': MyCustomFeature}  

### Prediction Function ###
Combine all the features to create the desired prediction function. For problem 1, your prediction function should output the predicted FairValue(expected average of future values) over the next 5 minutes. Output of the prediction function is used by the toolbox to make further trading decisions.

## **Available Feature Guide** ##

Features can be called by specifying config dictionaries. Create one dictionary per feature and return them in a dictionary as market features or instrument features.

Feature config Dictionary has the following keys:
  > *featureId:* a string representing the type of feature you want to use  
  > *featureKey:* {optional} a string representing the key you will use to access the value of this feature  
  >            If not present, will just use featureId  
  > *params:* {optional} A dictionary with which contains other optional params if needed by the feature 


Feature ID  | Parameters | Description
:-------------: | ------------- | -------------  
*moving_average*  | 'featureName', 'period' | calculate rolling average of *featureName* over *period* 
*moving_correlation* | 'period', 'series1', 'series2' | calculate rolling correlation of *series1* and *series2* over *period* 
*moving_max* | 'featureName', 'period' | calculate rolling max of *featureName* over *period* 
*moving_min* | 'featureName', 'period' | calculate rolling min of *featureName* over *period* 
*moving_sdev*  | 'featureName', 'period' | calculate moving standard deviation of *featureName* over *period*
*moving_sum* | 'featureName', 'period' | calculate moving sum of *featureName* over *period* 
*exponential_moving_average*  | 'featureName', 'period' | calculate exp. weighted moving average of *featureName* with *period* as half life 
*argmax* | 'featureName', 'period' | Returns the index where *featureName* is maximum over *period*
*argmin* | 'featureName', 'period' | Returns the index where *featureName* is minimum over *period*
*delay* | 'featureName', 'period' | Returns the value of *featureName* with a delay of *period*
*difference* | 'featureName', 'period' | Returns the difference of *featureName* with it's value *period* before
*rank* | 'featureName', 'period' | Ranks last *period* values of *featureName* on a scale of 0 to 1  
*scale* | 'featureName', 'period', 'scale' | Resale last *period* values of *featureName* on a scale of 0 to *scale*
*ratio*  | 'featureName', 'instrumentId1', 'instrumentId2' | ratio of feature values of instrumentID1 / instrumentID2
*momentum*  | 'featureName', 'period' | calculate momentum in *featureName* over *period* as featureValue(now) -  featureValue(now - period)
*bollinger_bands*  | 'featureName', 'period' | upper and lower bollinger bands as average(period) - sdev(period), average(period) + sdev(period)
*cross_sectional_momentum* | 'featureName', 'period', 'instrumentIds' | Returns Cross-Section Momentum of 'instrumentIds' in *featureName* over *period* 
*macd*  | 'featureName', 'period1', 'period2' | moving average convergence divergence as average(period1) - average(period2)
*rsi*  | 'featureName', 'period' | Relative Strength Index - ratio of average profits / average losses over period
*vwap*  | - | calculated from book data as *bid price x ask volume + ask price x bid volume / (ask volume + bid volume)*
***fees***  | - |fees to trade, always calculated
***position***  | - | instrument position, always calculated
***pnl***  | - | Profit/Loss, always calculated
***capital***  | -| Spare capital not in use, always calculated
***portfolio_value***  | - | Total value of trading system, always calculated
