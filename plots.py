import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from analyze import analyze 
from sklearn import linear_model
    
def scatter(data, age, index1, index2):
    '''Generates scatter plot and trend line in comparison between two indices in a given year'''

    df = np.log(analyze(data, 2017)[[index1]+[index2]].dropna())
    y = np.array(df[index1]).reshape(-1, 1)
    x = np.array(df[index2]).reshape(-1, 1)
    model = linear_model.LinearRegression().fit(x, y)
    plt.plot(x, model.predict(x), color='red', linewidth=2.)
    plt.scatter(y=y, x=x, color='blue', s=50, alpha=.5)
    plt.title('Tendency line log-log')
    plt.xlabel(index1)
    plt.ylabel(index2)
    plt.show()
    
def trend(data, country, index, start, end):
    '''Fenerates the trend line over the years (start and end) of the requested indices'''

    for i in country:
        df = analyze(data, "c-"+i, nocountries=True)[index].loc[[str(i) for i in range(start, end+1)]]
        plt.plot(df)
    plt.title('Tendency line')
    plt.legend(country)
    plt.xlabel('Age')
    plt.ylabel(index)
    plt.show
    
def lmh(data, age, index, x):
    '''Get the x lowest, middle and highest values'''
    
    df = analyze(data, age)[index].dropna().sort_values()
    amount = int(len(df)/2)-int(x/2)
    df.iloc[list(range(0,x))+list(range(amount, amount+x))+list(range(-x,0))].plot(kind="bar")
    plt.title('Bar plot')
    plt.xlabel('Country')
    plt.ylabel(index)
    plt.show()