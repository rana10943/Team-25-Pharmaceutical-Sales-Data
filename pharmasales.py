# -*- coding: utf-8 -*-
"""pharmasales.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/13T-nbkVSW9zrlBL1ypMw42LHIIH7LT7z
"""

# Pandas - Data manipulation and analysis library
import pandas as pd
# NumPy - mathematical functions on multi-dimensional arrays and matrices
import numpy as np
# Matplotlib - plotting library to create graphs and charts
import matplotlib.pyplot as plt
# Re - regular expression module for Python
import re
# Calendar - Python functions related to the calendar
import calendar

# Manipulating dates and times for Python
from datetime import datetime

# Scikit-learn algorithms and functions
from sklearn import linear_model
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import PolynomialFeatures
from sklearn.svm import SVR
from sklearn.ensemble import VotingRegressor

# Settings for Matplotlib graphs and charts
from pylab import rcParams
rcParams['figure.figsize'] = 12, 8

import seaborn as sns
sns.set()

"""### **On which day of the week is the second drug (M01AE) most often sold?**

---



---


"""

# Loading our sales daily data set from csv file using Pandas.
df = pd.read_csv("salesdaily.csv")

from google.colab import drive
drive.mount('/content/drive')

df.head()

file = r'/drive/MyDrive/Colab Notebooks/archive/salesdaily.csv'

"""**Grouping the second drug sales by weekday name.**

---

**Let's look at the data.**
"""

df = df[['M01AE', 'Weekday Name']]
result = df.groupby(['Weekday Name'], as_index=False).sum().sort_values('M01AE', ascending=False)

"""Taking the weekday name with most sales and the volume of sales from the result"""

resultDay = result.iloc[0,0]
resultValue = round(result.iloc[0,1], 2)

"""Printing the result"""

print('The second drug, M01AE, was most often sold on ' + str(resultDay))
print('with the volume of ' + str(resultValue))

"""### **Pandas Profiling **"""

! pip install pip install https://github.com/pandas-profiling/pandas-profiling/archive/master.zip



import numpy as np
import pandas as pd
from pandas_profiling import ProfileReport

df = pd.read_csv('salesdaily.csv')
print(df)

#Generate a report 
profile = ProfileReport(df)
profile.to_file(output_file="salesdaily.html")



"""### **Which three drugs have the highest sales in Jan 2015, Jul 2016, Sep 2017**
Loading monthly sales data set from csv file using Pandas.
"""

df = pd.read_csv("salesmonthly.csv")

"""Let's look at the data."""

df.head()

"""Because we will be repeating the same calculations for different months and years it is a good idea to write a function"""

def top3byMonth(month, year):
    """
    given a month and a year
    find top 3 drugs sold
    """
    month = str(month) if (month > 9) else '0'+str(month)
    year = str(year)
    # filter by date
    sales = df.loc[df['datum'].str.contains('^'+year+'\-'+month+'', flags=re.I, regex=True)]
    # reset index
    sales = sales.reset_index()
    # filter relevant columns
    topSales = sales[['M01AB', 'M01AE', 'N02BA', 'N02BE', 'N05B', 'N05C', 'R03', 'R06']]
    # sort values horizontally
    topSales = topSales.sort_values(by=0, ascending=False, axis=1)
    # print results
    print('Top 3 drugs by sale in '+calendar.month_name[int(month)]+' '+year)
    for field in topSales.columns.values[0:3]:
        print(' - Product: ' + str(field) + ', Volume sold: ' + str(round(topSales[field].iloc[0], 2)))
    print("\n")

"""We are now calling the function fir different months and years and printing results"""

# top3 drugs by sale in January 2015
top3byMonth(1, 2015)

# top3 drugs by sale in July 2016
top3byMonth(7, 2016)

# top3 drugs by sale in September 2017
top3byMonth(9, 2017)

"""### **Which drug has sold most often on Mondays in 2017?**
Loading our sales daily data set from csv file using Pandas.
"""

df = pd.read_csv("salesdaily.csv")

"""Let's look at the data."""

df.head()

"""Filtering out from the data everything else apart from yar 2017 and Monday"""

df = df.loc[df['datum'].str.contains('2017', flags=re.I, regex=True) & (df['Weekday Name'] == 'Monday')]

"""Groupping by weekday name and summarising"""

df = df.groupby(['Weekday Name'], as_index=False).sum()

"""Filtering only relevant columns and sorting values of most sold drugs horizontally to achieve the most often sold drug on the left"""

df = df[['M01AB', 'M01AE', 'N02BA', 'N02BE', 'N05B', 'N05C', 'R03', 'R06']]
result = df.sort_values(by=0, ascending=False, axis=1)

"""Displaying results"""

for field in result.columns.values[0:1]:
    print('The drug most often sold on Mondays in 2017 is ' + str(field))
    print('with the volume of ' + str(round(result[field].iloc[0], 2)))

"""### **What medicine sales may be in January 2020?**
Defining the scattering function that will display scattered sales data on the chart
"""

def scatterData(X_train, y_train, X_test, y_test, title):
    plt.title('Prediction using ' + title)
    plt.xlabel('Month sequence', fontsize=20)
    plt.ylabel('Sales', fontsize=20)

    # Use Matplotlib Scatter Plot
    plt.scatter(X_train, y_train, color='blue', label='Training observation points')
    plt.scatter(X_test, y_test, color='cyan', label='Testing observation points')

"""Defining predict sales and display Linear Regression model function"""

def predictLinearRegression(X_train, y_train, X_test, y_test):

    y_train = y_train.reshape(-1, 1)
    y_test = y_test.reshape(-1, 1)

    scatterData(X_train, y_train, X_test, y_test, 'Linear Regression')

    reg = linear_model.LinearRegression()
    reg.fit(X_train, y_train)
    plt.plot(X_train, reg.predict(X_train), color='red', label='Linear regressor')
    plt.legend()
    plt.show()

    # LINEAR REGRESSION - Predict/Test model
    y_predict_linear = reg.predict(X_test)

    # LINEAR REGRESSION - Predict for January 2020
    linear_predict = reg.predict([[predictFor]])
    # linear_predict = reg.predict([[predictFor]])[0]

    # LINEAR REGRESSION - Accuracy
    accuracy = reg.score(X_train, y_train)

    # LINEAR REGRESSION - Error
    # error = round(np.mean((y_predict_linear-y_test)**2), 2)
    
    # Results
    print('Linear Regression: ' + str(linear_predict) + ' (Accuracy: ' + str(round(accuracy*100)) + '%)')

    return {'regressor':reg, 'values':linear_predict}

"""Defining predict sales and display Polynomial Regression model function"""

def predictPolynomialRegression(X_train, y_train, X_test, y_test):

    y_train = y_train.reshape(-1, 1)
    y_test = y_test.reshape(-1, 1)

    scatterData(X_train, y_train, X_test, y_test, 'Polynomial Regression')
    
    poly_reg = PolynomialFeatures(degree = 2)
    X_poly = poly_reg.fit_transform(X_train)
    poly_reg_model = linear_model.LinearRegression()
    poly_reg_model.fit(X_poly, y_train)
    plt.plot(X_train, poly_reg_model.predict(poly_reg.fit_transform(X_train)), color='green', label='Polynomial regressor')
    plt.legend()
    plt.show()

    # Polynomial Regression - Predict/Test model
    y_predict_polynomial = poly_reg_model.predict(X_poly)

    # Polynomial Regression - Predict for January 2020
    polynomial_predict = poly_reg_model.predict(poly_reg.fit_transform([[predictFor]]))

    # Polynomial Regression - Accuracy
    # X_poly_test = poly_reg.fit_transform(X_test)
    accuracy = poly_reg_model.score(X_poly, y_train)

    # Polynomial Regression - Error
    # error = round(np.mean((y_predict_polynomial-y_train)**2), 2)

    # Result
    print('Polynomial Regression: ' + str(polynomial_predict) + ' (Accuracy: ' + str(round(accuracy*100)) + '%)')
    return {'regressor':poly_reg_model, 'values':polynomial_predict}

"""Defining predict sales and display Simple Vector Regression (SVR) function"""

def predictSVR(X_train, y_train, X_test, y_test):

    y_train = y_train.reshape(-1, 1)
    y_test = y_test.reshape(-1, 1)

    scatterData(X_train, y_train, X_test, y_test, 'Simple Vector Regression (SVR)')

    svr_regressor = SVR(kernel='rbf', gamma='auto')
    svr_regressor.fit(X_train, y_train.ravel())

    # plt.scatter(X_train, y_train, color='red', label='Actual observation points')
    plt.plot(X_train, svr_regressor.predict(X_train), label='SVR regressor')
    plt.legend()
    plt.show()

    # Simple Vector Regression (SVR) - Predict/Test model
    y_predict_svr = svr_regressor.predict(X_test)

    # Simple Vector Regression (SVR) - Predict for January 2020
    svr_predict = svr_regressor.predict([[predictFor]])

    # Simple Vector Regression (SVR) - Accuracy
    accuracy = svr_regressor.score(X_train, y_train)

    # Simple Vector Regression (SVR) - Error
    # error = round(np.mean((y_predict_svr-y_train)**2), 2)
    
    # Result
    print('Simple Vector Regression (SVR): ' + str(svr_predict) + ' (Accuracy: ' + str(round(accuracy*100)) + '%)')
    return {'regressor':svr_regressor, 'values':svr_predict}

"""We are defining a product that we will be predicting the January 2020 sales for. We can change it to a differnt one and use the same calculations for a different product."""

product = 'N02BA'

"""For storing all regression results"""

regResults = pd.DataFrame(columns=('Linear', 'Polynomial', 'SVR', 'Voting Regressor'), index=[product])

"""To display a larger graph than a default with specify some additional parameters for Matplotlib library."""

rcParams['figure.figsize'] = 12, 8

"""We will be using monthly data for our predictions"""

df = pd.read_csv("salesmonthly.csv")

"""We will use monthly sales data from 2017, 2018, 2019. We could also use just 2019 for that."""

df = df.loc[df['datum'].str.contains("2014") | df['datum'].str.contains("2015") | df['datum'].str.contains("2016") | df['datum'].str.contains("2017") | df['datum'].str.contains("2018") | df['datum'].str.contains("2019")]
df = df.reset_index()

"""It is always a good practice to look at the data often"""

df

"""We are adding a sequence number for each month as an independent variable

"""

df['datumNumber'] = 1
for index, row in df.iterrows():
    df.loc[index, 'datumNumber'] = index+1

"""Removing the first and the last incompleted record from Pandas Data Frame"""

# the first and the last available month is quite low which may indicate that it might be incomplete
# and skewing results so we're dropping it
df.drop(df.head(1).index,inplace=True)
df.drop(df.tail(1).index,inplace=True)

"""Cleaning up any rows with the product value = 0."""

df = df[df[product] != 0]

"""Let's look at the data again."""

df.head()

"""What value we predict for? January 2020. Because we have data until August 2019 we're predicting for 5 months ahead"""

predictFor = len(df)+5
print('Predictions for the product ' + str(product) + ' sales in January 2020')

regValues = {}

"""Preparing training and testing data by using train_test_split function. 70% for training and 30% for testing."""

dfSplit = df[['datumNumber', product]]

# We are going to keep 30% of the dataset in test dataset
train, test = train_test_split(dfSplit, test_size=3/10, random_state=0)

trainSorted = train.sort_values('datumNumber', ascending=True)
testSorted = test.sort_values('datumNumber', ascending=True)

X_train = trainSorted[['datumNumber']].values
y_train = trainSorted[product].values
X_test = testSorted[['datumNumber']].values
y_test = testSorted[product].values

"""Performing feature scaling. Scaling the feature will improve the performance of the model.

"""

# scale_X = StandardScaler()
# scale_y = StandardScaler()

# X_train = scale_X.fit_transform(X_train)
# y_train = scale_y.fit_transform(y_train.reshape(-1, 1))

# X_test = scale_X.fit_transform(X_test)
# y_test = scale_y.fit_transform(y_test.reshape(-1, 1))

"""Performing and saving results for Linear Regression"""

# LINEAR REGRESSION
linearResult = predictLinearRegression(X_train, y_train, X_test, y_test)
reg = linearResult['regressor']
regValues['Linear'] = round(linearResult['values'][0][0])

"""Performing and saving results for Polynomial Regression"""

# POLYNOMIAL REGRESSION
polynomialResult = predictPolynomialRegression(X_train, y_train, X_test, y_test)
polynomial_regressor = polynomialResult['regressor']
regValues['Polynomial'] = round(polynomialResult['values'][0][0])

"""Performing and saving results for Simple Vector Regression (SVR)"""

# SIMPLE VECTOR REGRESSION (SVR)
svrResult = predictSVR(X_train, y_train, X_test, y_test)
svr_regressor = svrResult['regressor']
regValues['SVR'] = round(svrResult['values'][0])

"""Voting Regressor"""

vRegressor = VotingRegressor(estimators=[('reg', reg), ('polynomial_regressor', polynomial_regressor), ('svr_regressor', svr_regressor)])

vRegressorRes = vRegressor.fit(X_train, y_train.ravel())

# VotingRegressor - Predict for January 2020
vRegressor_predict = vRegressor.predict([[predictFor]])
regValues['Voting Regressor'] = round(vRegressor_predict[0])
print('Voting Regressor January 2020 predicted value: ' + str(round(vRegressor_predict[0])))
regResults.loc[product] = regValues

"""Displaying all results"""

regResults

"""














# **Pharma Sales Time Series Analysis**"""

#import libraries
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

#reading the data
hourly = pd.read_csv('saleshourly.csv')
daily = pd.read_csv('salesdaily.csv')
weekly = pd.read_csv('salesweekly.csv')
monthly = pd.read_csv('salesmonthly.csv')

"""# **Analysing Data Stucture**"""

#function to print shape of a given data
def print_shape(data):
    print('Rows : ',data.shape[0])
    print('Columns : ',data.shape[1])

print_shape(hourly)
print_shape(daily)
print_shape(weekly)
print_shape(monthly)

"""From the shape of monthly dataframe, we see that the data is of 70 months."""

hourly.head(2)

daily.head(2)

weekly.head(2)

monthly.head(2)

"""**Notice that the format of datum column is different in hourly and monthly data and same in daily and weekly data.**"""

#copy the data
hourly_original = hourly.copy()
daily_original = daily.copy()
weekly_original = weekly.copy()

"""**Let us now convert data type of datum column from object to datetime**"""

#converting datatype of dates from object to Datetime
monthly['datum'] = pd.to_datetime(monthly['datum'], format= '%Y-%m-%d')
weekly['datum'] = pd.to_datetime(weekly['datum'], format= '%m/%d/%Y')
daily['datum'] = pd.to_datetime(daily['datum'], format= '%m/%d/%Y')
hourly['datum'] = pd.to_datetime(hourly['datum'], format= '%m/%d/%Y %H:%M')

"""### **Analysing Monthly Series**
Firstly, let us analyse the monthly data and see what inferences can we draw from this data.
"""

#import datetime for dates and time realted calculations
import datetime as dt

"""**Seperate year, month and day from the datum column**"""

#extracting year from dates
monthly['year'] = monthly['datum'].dt.year

#extracting month from dates
monthly['month'] = monthly['datum'].dt.month

#extracting day from dates
monthly['day'] = monthly['datum'].dt.day

#set index equal to the dates which will help us in visualising the time series
monthly.set_index(monthly['datum'], inplace= True)

monthly.head(2)

"""## **Data distribution analysis**
Chart with daily sales for different categories of interest is shown below. N02BE and N05B charts, though showing the similar trends, are suppresed because of the larger scale which makes the other illustrations less readable.
"""

dfatch=pd.read_csv('saleshourly.csv')
dfatch['datum']= pd.to_datetime(dfatch['datum']) 

grp1=dfatch.groupby(dfatch.datum.dt.hour)['M01AB'].mean()
grp2=dfatch.groupby(dfatch.datum.dt.hour)['M01AE'].mean()
grp3=dfatch.groupby(dfatch.datum.dt.hour)['N02BA'].mean()
grp6=dfatch.groupby(dfatch.datum.dt.hour)['N05C'].mean()
grp7=dfatch.groupby(dfatch.datum.dt.hour)['R03'].mean()
grp8=dfatch.groupby(dfatch.datum.dt.hour)['R06'].mean()

plt.title('Daily average sales')
plt.xlabel('Time of day')
plt.ylabel('Quantity of sale')

grp1.plot(figsize=(8,6))
grp2.plot(figsize=(8,6))
grp3.plot(figsize=(8,6))
grp6.plot(figsize=(8,6))
grp7.plot(figsize=(8,6))
grp8.plot(figsize=(8,6))

plt.legend(['M01AB', 'M01AE', 'N02BA', 'N05C', 'R03', 'R06'], loc='upper left')

plt.show()

#define a function to plot yearly sales of every category of drug.
def plot_yearly_sales(column):
    monthly.groupby('year')[column].mean().plot.bar()#calculating yearly sales using groupby
    plt.title(f'Yearly sales of {column}')
    plt.xlabel('Year')
    plt.ylabel('Sales')
    plt.show()

#plotting yearly sales of each drug category
for i in monthly.columns[1:9]:#drug categories are from 1 to 8 index

    plot_yearly_sales(i)

"""**Analysing the above yearly sales graphs, we can conclude that:**


*   The year 2017 has seen a major dip in the sales of drugs. This need digging. Lets do it



"""

#lets see some statistics related to the data
monthly.describe()

"""Here, we see that the minimum value of sale of majority of drugs is 0 while that of drug N05B is 1. This is the reason why year 2017 has lowest sales."""

#plot line curve to analyse monthly sales
def plot_line_curve(series):
    plt.figure(figsize= (15,5))
    series.plot(kind= 'line')
    plt.title(f'Monthly Sales of Drug : {col}')
    plt.show()

for col in monthly.columns[1:9]:
    plot_line_curve(monthly[col])

"""From the above graphs, we can infer that the sales for first month of 2017 is 0. This means that we have missing values for the first month. Let us analyse this from daily data.
But first let us preprocess daily data also.
"""

daily.columns

#extracting days from date
daily['day'] = daily['datum'].dt.day

#set dates as index
daily.set_index(daily['datum'], inplace= True)

#looking at sales data from 1st Jan, 2017 to 1st Feb, 2019
for col in daily.columns[1:9]:
    plot_line_curve(daily[col].loc['1/1/2017':'2/1/2017'])

"""From these graphs, we can say say that the data is not missing. Instead, the sales of drugs on 2nd January, 2017 is low rather there is no sale on 2nd Feb.

# **Analysing total sales of drug**
"""

#calculating total sales
monthly['total_sales'] = monthly['M01AB']
for cols in monthly.columns[2:9]:
    monthly['total_sales'] = monthly['total_sales']+monthly[cols]

monthly.groupby('month')['total_sales'].plot.bar(rot=45)
plt.xlabel('Date Time')
plt.ylabel('Total Sales')
plt.title('Total Sales of Drugs')
plt.show()

"""From above diagram we can hence validate that the sales of drugs have been lowest in the year 2017."""

