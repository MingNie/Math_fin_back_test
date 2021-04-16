import numpy as np
import pandas as pd

class back_test_bot(object):
    '''
    :parameter
    this class is for back test of trading strategies
    instrument: the financial instrument you are trading, string
    data: the time series data of the equity

    Author: Ming NIE
    All Rights Reserved
    '''
    def __init__(self, instrument, data):
        self.instrument = instrument
        # eliminate all na data
        self.data = data.dropna()

    def strategy_init_(self, range1, range2, strategy, smoothing = 2):
        '''
        :parameter
        range1: shorter range day number
        range2: longer range day number

        Strategy: 1 for EMA
        Strategy: 0 for SMA
        you can also add more strategies as you wish

        smoothing = 2, param for EMA
        '''
        self.range1 = range1
        self.range2 = range2
        self.strategy = strategy

        if self.strategy == 0:
            # SMA trading strategy
            print("---user choice : moving ave strategy, shorter moving range " + str(range1) + " longer moving range: " + str(range2))
            self.data["range1"] = self.data['Adj Close'].rolling(range1).mean()
            self.data["range2"] = self.data['Adj Close'].rolling(range2).mean()

            # can change the last number to -1 for short position
            self.data['Position'] = np.where(self.data['range1'] > self.data['range2'], 1, 0)
            print("---portfolio position established ...")

            self.data['Returns'] = np.log(self.data['Adj Close'] / self.data['Adj Close'].shift(1))
            print("---market returns calculated ...")
            self.data['Strategy'] = self.data['Position'].shift(1) * self.data['Returns']
            print("---strategy returns calculate ...")

            self.data.dropna(inplace=True)

            self.sum = np.exp(self.data[['Returns', 'Strategy']].sum())

            # using 252 trading days
            self.std = self.data[['Returns', 'Strategy']].std() * 252 ** 0.5

            print("---Congrats!!! all result generated, find daily data in results, find stats data in sum and std")

        if self.strategy == 1:
            # EMA trading strategy
            print("---user choice : moving EMA strategy, shorter moving range " + str(range1) + " longer moving range: " + str(range2))

            ema1 = [None]*(range1-1)
            ema2 = [None]*(range2-1)

            ema1.append(sum(self.data['Adj Close'][:range1]) / range1)
            for price in self.data['Adj Close'][range1:]:
                ema1.append((price * (smoothing / (1 + range1))) + ema1[-1] * (1 - (smoothing / (1 + range1))))
            self.data["EMA1"]= ema1

            ema2.append(sum(self.data['Adj Close'][:range2]) / range2)
            for price in self.data['Adj Close'][range2:]:
                ema2.append((price * (smoothing / (1 + range2))) + ema2[-1] * (1 - (smoothing / (1 + range2))))
            self.data["EMA2"] = ema2

            # can change the last number to -1 for short position
            self.data['Position'] = np.where(self.data['EMA1'] > self.data['EMA2'], 1, 0)

            print("---portfolio position established ...")

            self.data['Returns'] = np.log(self.data['Adj Close'] / self.data['Adj Close'].shift(1))
            print("---market returns calculated ...")
            self.data['Strategy'] = self.data['Position'].shift(1) * self.data['Returns']
            print("---strategy returns calculate ...")

            self.data.dropna(inplace=True)

            self.sum = np.exp(self.data[['Returns', 'Strategy']].sum())

            # using 252 trading days
            self.std = self.data[['Returns', 'Strategy']].std() * 252 ** 0.5

            print("---Congrats!!! all result generated, find daily data in results, find stats data in sum and std")


        if self.strategy == 0:
            # SMA trading strategy
            print("---user choice : moving ave strategy, shorter moving range " + str(range1) + " longer moving range: " + str(range2))
            self.data["range1"] = self.data['Adj Close'].rolling(range1).mean()
            self.data["range2"] = self.data['Adj Close'].rolling(range2).mean()

            # can change the last number to -1 for short position
            self.data['Position'] = np.where(self.data['range1'] > self.data['range2'], 1, 0)
            print("---portfolio position established ...")

            self.data['Returns'] = self.data['Adj Close'] - self.data['Adj Close'].shift(1)
            print("---market returns calculated ...")
            self.data['Strategy'] = self.data['Position'].shift(1) * self.data['Returns']
            print("---strategy returns calculate ...")

            self.data.dropna(inplace=True)

            self.sum = np.exp(self.data[['Returns', 'Strategy']].sum())

            # using 252 trading days
            self.std = self.data[['Returns', 'Strategy']].std() * 252 ** 0.5

            print("---Congrats!!! all result generated, find daily data in results, find stats data in sum and std")



    def plot1(self):
        if self.strategy == 0:
            print("---plot1: SMA moving average and price lines")
            self.data[["Adj Close","range1","range2"]].plot(figsize=(10, 6))
        if self.strategy == 1:
            print("---plot1: EMA moving average and price lines")
            self.data[["Adj Close", "EMA1", "EMA2"]].plot(figsize=(10, 6))


    def plot2(self):
        if self.strategy == 0:
            print("---plot2: SMA with positions")
            ax = self.data[["Adj Close", "range1", "range2", "Position"]].plot(secondary_y='Position', figsize=(10, 6))
            ax.get_legend().set_bbox_to_anchor((0.25, 0.85))
        if self.strategy == 1:
            print("---plot2: EMA with positions")
            ax = self.data[["Adj Close", "EMA1", "EMA2", "Position"]].plot(secondary_y='Position', figsize=(10, 6))
            ax.get_legend().set_bbox_to_anchor((0.25, 0.85))


    def plot3(self):
        if self.strategy == 0:
            print("---plot3: SMA strategy returns compared to the market")
            ax = self.data[['Returns', 'Strategy']].cumsum().apply(np.exp).plot(figsize=(10, 6))
            self.data['Position'].plot(ax=ax, secondary_y='Position', style='--')
            ax.get_legend().set_bbox_to_anchor((0.25, 0.85))
        if self.strategy == 1:
            print("---plot3: EMA strategy returns compared to the market")
            ax = self.data[['Returns', 'Strategy']].cumsum().apply(np.exp).plot(figsize=(10, 6))
            self.data['Position'].plot(ax=ax, secondary_y='Position', style='--')
            ax.get_legend().set_bbox_to_anchor((0.25, 0.85))


    def summary(self, year = 4):
        if self.strategy == 0:
            print("---- SMA: Sums up the returns for the strategy and the market")
            print(self.sum/year)
            print("---The annualized volatility for the strategy and the market")
            print(self.std)
        if self.strategy == 1:
            print("---- EMA: Sums up the returns for the strategy and the market")
            print(self.sum/year)
            print("---The annualized volatility for the strategy and the market")
            print(self.std)











