import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model, preprocessing
    
norm = lambda df: preprocessing.MinMaxScaler().fit_transform(np.array(df, dtype="float64").reshape(-1, 1))
    
def trend(data, index, countries, years):
    '''
    Generates a trend graph for a given index in a given period of time for any set of countries
    
    Parameters:
    -----------
    
        data -> dataframe of data
        index -> index string
        countries -> list with indexes strings
        years -> list with integers indicating the start and end year for the analysis
        
    Return:
    -------
        
        matplotlib.pyplot.plot with the trend graph
    
    Example:
    --------
    
        trend(data, 'GDP per capita (current US$)', ['Afghanistan', 'Brazil'], [2000, 2017]) 
    '''
    
    fig = plt.figure(figsize=(10, 5))
    
    for country in countries:
        plt.plot(data.loc[(index, country), [str(year) for year in range(years[0], years[1] + 1)]])
    
    plt.title('Tendency')
    plt.legend(countries)
    plt.xlabel('Years')
    plt.ylabel(index)
    plt.setp(plt.xticks()[1], rotation=60)
    plt.show()
    
def xsml(data, indexes, years, X):
    '''
    Generates a bar graph with the X smallest, the X medium, and the X largest values of an index or two charts with comparison
between two indices in their respective years
    
    Parameters:
    -----------
    
        data -> dataframe of data
        indexes -> index string or list with indexes strings
        years -> integer or list with integers indicating the year(s) for analysis
        X -> integer indicating the number of countries for the analyze 
        
    Return:
    -------
        
        matplotlib.pyplot.plot with the bar graph(s)
        
    Examples:
    ---------
    
        xsml(data,  'Economic freedom', 2017, 3)
        
        xsml(data,  ['Economic freedom', 'GDP per capita (current US$)'], 2017, 3)
    '''
    
    if type(indexes) == str:
        df = data.loc[indexes].drop('World')[str(years)].dropna().sort_values()
        fig = plt.figure(figsize=(10, 5))
        
        amount = int(df.shape[0]/2)-int(X/2)
        df.iloc[list(range(0,X))+list(range(amount, amount+X))+list(range(-X,0))].plot(kind="bar")
        plt.title('Bar graph')
        plt.xlabel('Country')
        plt.ylabel(indexes)
        plt.show()
        
    else:
        df1 = data.loc[indexes[0]].drop('World')[str(years[0])]
        df2 = data.loc[indexes[1]].drop('World')[str(years[1])]
        df = pd.DataFrame(df1).rename(columns=lambda x: "0").join(df2).dropna()
        df['0'] = norm(df['0'])
        df[str(years[1])] = norm(df[str(years[1])])
        amount = int(df.shape[0]/2)-int(X/2)
        bar1 = df.sort_values('0').iloc[list(range(0,X))+list(range(amount, amount+X))+list(range(-X,0))]
        bar2 = df.sort_values(str(years[1])).iloc[list(range(0,X))+list(range(amount, amount+X))+list(range(-X,0))]
        
        fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(15, 5))
        bar1.plot(kind='bar', ax=axes[0])
        bar2.plot(kind='bar', ax=axes[1])
        axes[0].set(xlabel = 'Country', ylabel = 'Normalized values',
                    title = 'xsml {} \n'.format(indexes[0]))
        axes[1].set(xlabel = 'Country', ylabel = 'Normalized values',
                    title = 'xsml {} \n'.format(indexes[1]))
        axes[0].legend(indexes)
        axes[1].legend(indexes)
        plt.show()
    
def trend_years(data, indexes, country, years, plot=True):
    '''
    Generates a trend graph for a given country and time period of any set of indexes or an index with its trend line. Or a tuple with the details of the trend line
    
    Parameters:
    -----------
    
        data -> dataframe of data
        indexes ->  indice string or list with indexes strings
        country -> country string
        years -> list with integers indicating the start and end year for the analysis
        plot -> boolean indicating whether the return will be a graph (True) or a tuple with the details of the trend line (False and indexes as an index string)
        
    Return:
    -------
        
        matplotlib.pyplot.plot with the trend graph or a tuple with R-Square, trend line coefficient and the number of countries in the analysis
        
    Examples:
    ---------
    
        trend_years(data, ['Economic freedom', 'GDP per capita (current US$)'], 'World', [2000, 2017])
        
        trend_years(data, 'Economic freedom', 'World', [2000, 2017])
        
        trend_years(data, 'Economic freedom', 'World', [2000, 2017], False)
    '''
    
    df = data.loc[(indexes, country), [str(year) for year in range(years[0], years[1] + 1)]]
    fig = plt.figure(figsize=(10, 5))
    
    if type(indexes) == str:
        df = df.dropna()
        x = norm(df.index)
        y = norm(df.values)
        model = linear_model.LinearRegression().fit(x, y)
        
        if plot:
            plt.plot(x, model.predict(x), color='red', linewidth=2.)
            plt.plot(x, y)
            plt.title('Trend graph and trend line')
            plt.legend(["R2 = {:0.4}".format(model.score(x, y)), "Coef = {:0.4}".format(model.coef_[0][0])])
            plt.setp(plt.xticks()[1], rotation=60)
            plt.xlabel('Normalized years')
            plt.ylabel('Normalized values')
            plt.show()

        else:
            return model.score(x, y), model.coef_[0][0], x.shape[0]
        
    else:
        df = df.dropna(1)
        for ind in indexes:
            plt.plot(df.columns, norm(df.loc[ind]))
            
        plt.title('Trend graphs')
        plt.legend(indexes)
        plt.setp(plt.xticks()[1], rotation=60)
        plt.xlabel('Years')
        plt.ylabel('Normalized values')
        plt.show() 