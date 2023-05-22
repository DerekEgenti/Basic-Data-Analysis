import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns

   ##Read the csv file and save the variable name as df
df = pd.read_csv("UK-HPI-full-file-2017-01.csv")

   ##Then used the df.head function to show the first 5 observations

print(df.head())

   ##Then used the df.tail function to show the last 5 observations

print(df.tail())

   ##Used df.shape to get the shape of the dataset

print(df.shape)

   ##Used df.info to get the list and datatypes of all the columns

print(df.info())

##The date column is then seperated into months and years for easier analysis
   ##Date column is converted from object to datetime datatype

df['Date'] =  pd.to_datetime(df['Date'], format='%d/%m/%Y')

   ##Then the data column is split into days, months and years
df['Month'] = df['Date'].dt.month
df['Year'] = df['Date'].dt.year
df['Day'] = df['Date'].dt.weekday

   ##The months and weekdays columns datatype is then changed to words for easy visualization

Months = {1:'Jan',2:'Feb',3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}
Weekday = {0:"Mon", 1:"Tue", 2:"Wed", 3:"Thu", 4:"Fri", 5:"Sat", 6:"Sun"}


df['Day'].replace(Weekday, inplace=True)
df['Month'].replace(Months, inplace=True)

   ##Start the data cleaning process by checking for duplictes in the dataset

print(df.duplicated().sum())

   ##After checking the info and the duplicates, it is discovered that there is a high percentage
   ##of missing values in some columns but no duplicates in the data.
   ##We will check for the missing values below

for col in df.columns:
    if df[col].isnull().values.any():
        print(col)
        print(df[col].isnull().sum())
        
        
    ##Now delete columns with significantly missing values
    
df.drop(['IndexSA', 'CashPrice', 'CashIndex', 'Cash1m%Change', 'Cash12m%Change', 'MortgagePrice', 'MortgageIndex', 'Mortgage1m%Change', 
         'Mortgage12m%Change', 'FTBPrice', 'FTBIndex', 'FTB1m%Change', 'FTB12m%Change', 'FOOPrice', 'FOOIndex', 
         'FOO1m%Change', 'FOO12m%Change'],   axis=1, inplace=True)
     
   ##Now we check the percentage of entries available

total_missing = df.isnull().sum().sort_values(ascending=False)
ratio_missing = (df.isnull().sum()/df.isnull().count()).sort_values(ascending=False)
missing_data = pd.concat([total_missing, ratio_missing], axis=1, keys=['Total', 'Ratio'])
missing_data['Type'] = df[missing_data.index].dtypes
missing_data = missing_data[(missing_data['Total'] > 0)]
print(missing_data)

##Then find unique values in a certain column

print(df['RegionName'].unique())

plt.figure(figsize = (17,10))

sns.barplot(data=df, x="Year", y="SalesVolume", color='g').set_title("Sales Volume per Year")
plt.show()

##Find the Mean of the Average Price

print(df.AveragePrice.describe())

   ##The Mean of the Average price is 150,337.5 so we find the year with the closest to this value
   
ax = sns.barplot(x="Year", y="AveragePrice", data=df, color='r',)
ax.set_ylabel('Average Price in £')
ax.set_title("Average Prices per Year")
ax.get_yaxis().set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))
plt.show()

 ##The month with the most sales across the dataset
sns.stripplot(data=df, x="Month", y="SalesVolume", color='b').set_title("Months With The Highest Sales Across All Years")
plt.show()

##Average price for 2006 for all regions 
   
selected = df[pd.to_datetime(df.Date).dt.year == 2006]
selected_mean = selected.groupby('RegionName')['AveragePrice'].mean()
print(selected_mean)

##Top 10 Regions with the highest average price in 2006 visuals
   
ax1 = selected_mean.sort_values(ascending=False).head(10).plot(kind='bar')
ax1.get_yaxis().set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))
ax1.set_ylabel('Average Price in £')
ax1.set_title("Top 10 Regions with the Highest Average Price in 2006")
plt.xticks(rotation=60)
plt.rcParams['figure.figsize'] = (15, 7)
plt.show()

##Bottom 10 regions with the lowest average price in 2006 visuals
   
ax2 = selected_mean.sort_values().head(10).plot(kind='bar')
ax2.get_yaxis().set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))
ax2.set_ylabel('Average Price in £')
ax2.set_title("Top 10 Regions with the Lowest Average Price in 2006")
plt.xticks(rotation=60)
plt.show()

   ##The month with the highest average price across the dataset (to find out which month is closer to the mean value in price
   ##to know the most favorable month to buy or when people normally buy at the mean price)
   
ax3 = sns.lineplot(data=df, x="Month", y="AveragePrice", color='r', ci=None,)
ax3.set_ylabel('Average Price in £')
ax3.set_title("Months With The Highest Average Price Across the Dataset")
ax3.get_yaxis().set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))
plt.show()

##Heatmap
sns.heatmap(df.corr(), annot=True)
plt.show()

   ##From the heatmap, there is a correlation between House Type Prices vs Average price SA
   ##So we plot them 
   
sns.color_palette("Spectral", as_cmap=True)
ax4 = sns.scatterplot(data=df, x="AveragePriceSA", y="DetachedPrice", hue="Year")
ax4.set_ylabel('Detached Price in £')
ax4.set_xlabel('Average Price SA in £')
ax4.set_title("Average Price SA vs Detached Price")
ax4.get_xaxis().set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))
ax4.get_yaxis().set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))

plt.show()

ax5 = sns.scatterplot(data=df, x="AveragePriceSA", y="SemiDetachedPrice", hue="Year")
ax5.set_ylabel('SemiDetached Price in £')
ax5.set_xlabel('Average Price SA in £')
ax5.set_title("Average Price SA vs SemiDetached Price")
ax5.get_xaxis().set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))
ax5.get_yaxis().set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))
plt.show()

ax6 = sns.scatterplot(data=df, x="AveragePriceSA", y="TerracedPrice", hue="Year")
ax6.set_ylabel('Terraced Price in £')
ax6.set_xlabel('Average Price SA in £')
ax6.set_title("Average Price SA vs Terraced Price")
ax6.get_xaxis().set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))
ax6.get_yaxis().set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))
plt.show()

ax7 = sns.scatterplot(data=df, x="AveragePriceSA", y="FlatPrice", hue="Year")
ax7.set_ylabel('Flat Price in £')
ax7.set_xlabel('Average Price SA in £')
ax7.set_title("Average Price SA vs Flat Price")
ax7.get_xaxis().set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))
ax7.get_yaxis().set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))
plt.show()








