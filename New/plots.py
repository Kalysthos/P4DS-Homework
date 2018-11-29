import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model, preprocessing
    
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
    
def lmh(data, index, year, x):
    '''Generates the x (int) smaller, middle and higher values for the indicated year (int) and index (str)'''
    
    df = data.loc[index].drop('World')[str(year)].dropna().sort_values()
    
    amount = int(len(df)/2)-int(x/2)
    df.iloc[list(range(0,x))+list(range(amount, amount+x))+list(range(-x,0))].plot(kind="bar")
    plt.title('Bar plot')
    plt.xlabel('Country')
    plt.ylabel(index)
    plt.show()
    
def trend_years(data, indexes, country, years, plot=True):
    '''Generates the trend line or the r squared, coefficient and number of countries (plot=False) of the years (list of ints) of the country (str) and the requested index (str)'''
    
    df = data.loc[(indexes, country), [str(i) for i in range(years[0], years[1] + 1)]]
    
    if type(indexes) == str:
        df = df.dropna()
        x = np.array(df.index, dtype="float64").reshape(-1, 1)
        y = preprocessing.MinMaxScaler().fit_transform(np.array(df.values, dtype="float64").reshape(-1, 1))
        model = linear_model.LinearRegression().fit(x, y)
        
        if plot:
            plt.plot(df.index, model.predict(x), color='red', linewidth=2.)
            plt.plot(df.index, y)
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
            plt.plot(df.columns, preprocessing.MinMaxScaler().fit_transform(np.array(df.loc[ind], dtype="float64").reshape(-1, 1)))
        plt.legend(indexes)
        plt.setp(plt.xticks()[1], rotation=60)
        plt.show() 