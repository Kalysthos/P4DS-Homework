import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from analyze import analyze 
from sklearn import linear_model, preprocessing
    
def scatter(data, year, index1, index2, plot=True):
    '''Generates scatter plot and trend line or the r squared (plot=False) in comparison between two indices (str) in a given year (int)'''

    df = np.array(analyze(data, year)[[index1,index2]].dropna())
    df = np.log(df) if df.min() > 0 else np.log(df + 1 - df.min())
    y = df[:,0].reshape(-1, 1)
    x = df[:,1].reshape(-1, 1)
    model = linear_model.LinearRegression().fit(x, y)
    if plot:
        plt.plot(x, model.predict(x), color='red', linewidth=2.)
        plt.scatter(y=y, x=x, color='blue', s=50, alpha=.5)
        plt.legend(["R**2 = {:0.4}".format(model.score(x, y))])
        plt.title('Tendency line log-log')
        plt.xlabel(index1)
        plt.ylabel(index2)
        plt.show()
        
    else:
        return model.score(x, y), model.coef_[0][0], len(x)
    
def trend(data, country, index, start, end):
    '''Generates the trend over the years (start and end, both int) of the countries (list of strs) and requested index (str)'''
    
    for i in country:
        plt.plot(analyze(data, "c-"+i, False)[index].loc[[str(i) for i in range(start, end+1)]])
    plt.legend(country)
    plt.title('Tendency')
    plt.setp(plt.xticks()[1], rotation=90)
    plt.xlabel('Years')
    plt.ylabel(index)
    plt.show()
    
def lmh(data, year, index, x):
    '''Generates the x (int) smaller, middle and higher values for the indicated year (int) and index (str)'''
    
    df = analyze(data, year)[index].dropna().sort_values()
    amount = int(len(df)/2)-int(x/2)
    df.iloc[list(range(0,x))+list(range(amount, amount+x))+list(range(-x,0))].plot(kind="bar")
    plt.title('Bar plot')
    plt.xlabel('Country')
    plt.ylabel(index)
    plt.show()
    
def trend_scatter(data, country, index, start, end, plot=True):
    '''Generates the trend line or the coefficient (plot=False) of the years (start and end, both int) of the country (str) and the requested index (str)'''
    
    df = analyze(data, "c-"+country, False)[index].loc[[str(i) for i in range(start, end+1)]].dropna()
    x = np.array(df.index).reshape(-1, 1)
    y = preprocessing.MinMaxScaler().fit_transform(np.array(df.values, dtype="float64").reshape(-1, 1))
    model = linear_model.LinearRegression().fit(x, y)
    if plot:
        plt.plot([i[0] for i in x], model.predict(x),color='red', linewidth=2.)
        plt.plot([i[0] for i in x],[i[0] for i in y])
        plt.legend(["R**2 = {:0.4}".format(model.score(x, y)), "Coef = {:0.4}".format(model.coef_[0][0])])
        plt.title('Tendency line')
        plt.setp(plt.xticks()[1], rotation=90)
        plt.xlabel('Years')
        plt.ylabel(index)
        plt.show()
        
    else:
        return model.score(x, y), model.coef_[0][0], len(x)