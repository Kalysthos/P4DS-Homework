import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model, preprocessing
    
norm = lambda x: preprocessing.MinMaxScaler().fit_transform(np.array(x, dtype="float64").reshape(-1, 1))
    
def trend(data, index, country, years):
    '''Generates the trend over the years (list of ints) of the countries (list of strs) and requested index (str)'''
    
    for i in country:
        plt.plot(data.loc[(index, i), [str(i) for i in range(years[0], years[1] + 1)]])
        
    plt.legend(country)
    plt.title('Tendency')
    plt.setp(plt.xticks()[1], rotation=60)
    plt.xlabel('Years')
    plt.ylabel(index)
    plt.show()
    
def lmh(data, indexes, year, x):
    '''Generates the x (int) smaller, middle and higher values for the indicated year (int) and index (str)'''
    
    if type(indexes) == str:
        df = data.loc[indexes].drop('World')[str(year)].dropna().sort_values()
        
        amount = int(len(df)/2)-int(x/2)
        df.iloc[list(range(0,x))+list(range(amount, amount+x))+list(range(-x,0))].plot(kind="bar")
        plt.title('Bar plot')
        plt.xlabel('Country')
        plt.ylabel(indexes)
        plt.show()
        
    else:
        df1 = data.loc[indexes[0]].drop('World')[str(year)]
        df2 = data.loc[indexes[1]].drop('World')[str(year)]
        df = pd.DataFrame(df1).rename(columns=lambda x: "0").join(df2).dropna().sort_values('0')
        df['0'] = norm(df['0'])
        df[str(year)] = norm(df[str(year)])
        
        amount = int(df.shape[0]/2)-int(x/2)
        bars = df.iloc[list(range(0,x))+list(range(amount, amount+x))+list(range(-x,0))]
        bars.plot(kind='bar')
        plt.legend(indexes)
        plt.title('Bar plot')
        plt.xlabel('Country')
        plt.show()
    
def trend_years(data, indexes, country, years, plot=True):
    '''Generates the trend line or the r squared, coefficient and number of countries (plot=False) of the years (list of ints) of the country (str) and the requested index (str)'''
    
    df = data.loc[(indexes, country), [str(i) for i in range(years[0], years[1] + 1)]]
    
    if type(indexes) == str:
        df = df.dropna()
        x = norm(df.index)
        y = norm(df.values)
        model = linear_model.LinearRegression().fit(x, y)
        
        if plot:
            plt.plot(x, model.predict(x), color='red', linewidth=2.)
            plt.plot(x, y)
            plt.legend(["R**2 = {:0.4}".format(model.score(x, y)), "Coef = {:0.4}".format(model.coef_[0][0])])
            plt.title('Tendency line')
            plt.setp(plt.xticks()[1], rotation=60)
            plt.xlabel('Years')
            plt.ylabel(indexes)
            plt.show()

        else:
            return model.score(x, y), model.coef_[0][0], len(x)
        
    else:
        df = df.dropna(1)
        for ind in indexes:
            plt.plot(df.columns, norm(df.loc[ind]))
        plt.legend(indexes)
        plt.setp(plt.xticks()[1], rotation=60)
        plt.show() 