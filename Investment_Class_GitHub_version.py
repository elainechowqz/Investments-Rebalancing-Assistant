import pandas as pd
import pandas_datareader as pdr
import datetime
import numpy as np
import matplotlib.pyplot as plt

# A simple program that assists rebalancing and decision making for personal investments, especially for individual investors in Canada

# Ongoing project

# close('all') closes all the figure windows
plt.close('all')

# Part one: data preparation

# We need a spreadsheet with all the essential investment information. See the included spreadsheet for the basic format that this program uses(with the specific information to be filled in by individual users).

# The spreadsheet contains a first column titled "ETF/stock" which includes all the ETFs and stocks that we have invested in, as well as a collection of other columns. For each investment category, there is a unique column which records if a given ETF/stock belongs to this category or not (in terms of 0s and 1s)

# Read the spreadsheet with all the essential investment information and obtain a dataframe named "data"
data = pd.read_excel(r'')  # enter the filepath for the investment data file

# Remove the spaces at the end of some of the column names, and obtain a list of column names(without any extra space).
column_list = []
for column in data.columns:
    column_list.append(column.rstrip())
data.columns = column_list

# USD to CAD conversion rate
currency_rate =  # enter the current conversion rate here

# time period for rebalancing considerations
start_date = datetime.date(  # year, month, date)
end_date=datetime.date(  # year, month, date)

# current total value of assets in CAD
total_asset=# enter the amount of total asset

# Prepare to get pricing info for each ETF/Stock during the given time period
volatility_list=[]
percent_change_list=[]
start_price_list=[]
end_price_list=[]
current_value_list=[]

# Iterate over each row of the dataframe named "data"
for index, rows in data.iterrows():
    price=pdr.get_data_yahoo(rows['ETF/Stock'], start_date, end_date)
    volatility=price['Adj Close'].std()
    volatility_list.append(volatility)
    start_price=price.iloc[0, -1]
    start_price_list.append(start_price)
    end_price=price.iloc[-1, -1]
    end_price_list.append(end_price)
    percent_change=(end_price - start_price)/start_price
    percent_change_list.append(percent_change)
    shares=rows['No. of Shares Purchased']
     # ETFs/Stocks in CAD
    if '.TO' in rows['ETF/Stock']:
        value=shares*end_price
    # ETFs/Stocks in USD
    else:
        value=shares*end_price*currency_rate
    current_value_list.append(value)

data['Volatility']=volatility_list
data['Start_date_price']=start_price_list
data['End_date_price']=end_price_list
data['Percent_change']=percent_change_list
data['Current Value in CAD']=current_value_list

# Part two: build a Python class such that each instance of the class is a category for our personal investments, e.g. stocks, bonds, big cap, small cap and real estate, etc

class Investment_category:

    # Initialize basic attributes for any instance of the class.
    def __init__(self, name, ratio):
        # Obtain a Pandas data frame for the given investment category
        self.df=data[data[name] > 0][['ETF/Stock', 'No. of Shares Purchased', 'Full Name', 'MER', 'Summary',
            'Volatility', 'Start_date_price', 'End_date_price', 'Percent_change', 'Current Value in CAD']]
        # Ratio is the approximate percentage of the total assets that should be invested in the given category
        self.ratio=ratio

    # a method for a given investment class that calculates the amount of rebalancing that's needed on the end_date
    def rebalancing(self):

        current_total=self.df['Current Value in CAD'].sum()

        rebalancing_amount=total_asset*self.ratio - current_total
        return rebalancing_amount

    # some plotting methods for each investment category that include features like MER, recent pricing trends, etc for each ETF/stock in this category
    def MER_plot(self):
        plot_1=self.df.plot.bar(x='ETF/Stock', y='MER',
                                color='Blue', label='MER_plot')

    def Volatility_plot(self):
        plot_2=self.df.plot.bar(
            x='ETF/Stock', y='Volatility', color='Green', label='Volatility_plot')

    def PercentChange_plot(self):
        plot_3=self.df.plot.bar(
            x='ETF/Stock', y='Percent_change', color='Red', label='PercentChange_plot')

    def CurrentValue_plot(self):
        plot_4=self.df['Current Value in CAD'].plot.pie(
            figsize=(6, 6), label='CurrentValue_pie_plot')
        plot_5=self.df.plot.bar(
            x='ETF/Stock', y='Current Value in CAD', color='Orange', label='PercentChange_plot')

# Part Three: figure out how much to rebalance for each investment category on the end date specified above

# Create a nested list of all the investment classes and their corresponding amounts to be rebalanced on the end date. Inclusion relations between some investment classes are reflected in the nesting structures of the sublists.

# A nested list can be produced by first creating an instance of the Investment_Category class for each investment category, and then calling the rebalancing method for each category

# Let p denote percentage (to be entered by the user)

rebalance=[]

Bonds=Investment_category('Bonds?',  # p)
rebalance.append(['Bonds', Bonds.rebalancing()])

Stocks=Investment_category('Stocks?',  # p)
rebalance.append(['Stocks', Stocks.rebalancing()])

Canadian_Stocks=Investment_category('Canadian Stocks?',  # p)
rebalance[-1].append(['Canadian Stocks', Canadian_Stocks.rebalancing()])

USA_Stocks=Investment_category('USA Stocks?',  # p)
rebalance[-1].append(['USA Stocks', USA_Stocks.rebalancing()])

USA_totalmarket_Stocks=Investment_category('USA Total Market?',  # p)
rebalance[-1][-1].append(['USA total market Stocks',
                         USA_totalmarket_Stocks.rebalancing()])

USA_bigcap_Stocks=Investment_category('USA Big Cap?',  # p)
rebalance[-1][-1].append(['USA big cap Stocks',
                         USA_bigcap_Stocks.rebalancing()])

USA_smallcap_Stocks=Investment_category('USA Small Cap?',  # p)
rebalance[-1][-1].append(['USA small Stocks',
                         USA_smallcap_Stocks.rebalancing()])

International_Stocks=Investment_category('International Stocks?',  # p)
rebalance[-1].append(['International Stocks',
                     International_Stocks.rebalancing()])

International_allmarkets_Stocks=Investment_category('International All Markets Stocks?',  # p)
rebalance[-1][-1].append(['International all markets Stocks',
                         International_allmarkets_Stocks.rebalancing()])

International_developedmarkets_Stocks=Investment_category('International Developed Markets Stocks?',  # p)
rebalance[-1][-1].append(['International developed markets Stocks',
                         International_developedmarkets_Stocks.rebalancing()])

International_emergingmarkets_Stocks=Investment_category('International Emerging Markets Stocks?',  # p)
rebalance[-1][-1].append(['International emerging markets Stocks',
                         International_emergingmarkets_Stocks.rebalancing()])

Environmental_Stocks=Investment_category('Environmental/ESG Stocks?',  # p)
rebalance[-1].append(['Environmental Stocks',
                     Environmental_Stocks.rebalancing()])

Preciousmetal_Stocks=Investment_category('Precious Metal Stocks?',  # p)
rebalance[-1].append(['Precious Metal Stocks',
                     Preciousmetal_Stocks.rebalancing()])

REIT_Stocks=Investment_category('REIT Stocks?',  # p)
rebalance[-1].append(['REIT Stocks', REIT_Stocks.rebalancing()])

# Possible future improvements: due to the inclusion relations between some investment classes, consider implementing tree structures and claases with inheritence.
