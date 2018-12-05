import plotly.offline as py
import plotly.graph_objs as go
import numpy as np
from sklearn import linear_model, preprocessing
py.init_notebook_mode(connected=True)

norm = lambda array: preprocessing.MinMaxScaler().fit_transform(array)
cuberoot = lambda array: np.array([value**(1/3) if value >= 0 else -abs(value)**(1/3) for value in array])

class divider:
    '''Create an object to get ordered parts of an array'''
    
    def __init__(self, length, parts):
        self.length, self.cut = length, [None]*parts
        for part in range(parts):
            self.cut[part] = length//parts*part + np.arange(length//parts + 1 if length%parts - part > 0 else length//parts)   
            
    def split(self, part):
        return np.setdiff1d(np.arange(self.length), self.cut[part])
    
def findlinear(x, y, parts):
    '''Find the model that best fits the data without a part'''
    
    np.random.seed(0)
    order = np.random.permutation(x.shape[0])
    x, y = x[order], y[order]
    split = divider(x.shape[0], parts)
    r2 = 0
    
    for part in range(parts):
        index = split.split(part)
        xtest, ytest = x[index], y[index]
        modeltest = linear_model.LinearRegression().fit(xtest, ytest)
        r2test = modeltest.score(xtest,ytest)
        if r2test >= r2:
            r2, model = r2test, modeltest
            
    return model

def remove_outliers(x, y, percent, parts):
    '''Remove possible outliers'''
    
    model = findlinear(x, y, parts)
    distance = abs(y - model.predict(x))
    distance.dtype = 'float64'
    deviation = abs(distance - distance.mean())/np.std(distance) if np.std(distance) != 0 else distance*0
    part = (100-percent)/100*x.shape[0]
    for multiplier in np.arange(2., 5., 0.5):
        std = deviation < multiplier 
        if std.sum() >= part:
            return std
    
def scatter(data, indexes, years, plot=True, percent=3, parts=10):
    '''
    Generates a trend graph of the correlation between two indices in their specific years or the trend line information between them
    
    Parameters:
    -----------
    
        data -> dataframe of data
        indexes ->  list with indexes strings
        years -> list with the integers indicating, respectively, the year in which each index will be analyzed
        plot -> boolean indicating whether the return will be a graph (True) or a tuple with the details of the trend line (False)
        percent -> percentage limit of the amount of outliers that will be withdrawn
        parts -> number of parts in which the data will be divided into findlinear
    
    Return:
    -------
        
        plotly.plotly.iplot with the scatter plot and the trend line or a tuple with R-Square, trend line coefficient, the number of countries in the analysis and the function that was applied in the data
        
    Examples:
    ---------
    
        scatter(data, [2014,2005], ['GDP per capita (current US$)', 'GDP growth (annual %)'])
        
        scatter(data, [2014,2005], ['GDP per capita (current US$)', 'GDP growth (annual %)'], True)
    '''
    
    df = data.loc[(indexes[0]), [str(years[0])]].rename(columns = lambda x: '0').join(data.loc[indexes[1]][str(years[1])]).dropna()
    
    if df.shape[0] < 20:
        raise ValueError('Without enough data')
        
    x = np.array(df['0']).reshape(-1, 1)
    y = np.array(df[str(years[1])]).reshape(-1, 1)
    xlist = [(norm(np.log(x)), "log(x)") if x.min() > 0 else (norm(cuberoot(x)), "x**(1/3)"), (norm(x), "x")]
    ylist = [(norm(np.log(y)), "log(y)") if y.min() > 0 else (norm(cuberoot(y)), "y**(1/3)"), (norm(y), "y")]
    r2 = 0
    
    for xitem in xlist:
        for yitem in ylist:
            stdtest = remove_outliers(xitem[0], yitem[0], percent, parts)
            xin, yin = xitem[0][stdtest].reshape(-1, 1), yitem[0][stdtest].reshape(-1, 1)
            modeltest = linear_model.LinearRegression().fit(xin, yin)
            r2test = modeltest.score(xin, yin)
            if r2test >= r2:
                std = stdtest
                x, leix = xitem
                y, leiy = yitem
                model, r2 = modeltest, r2test
                    
    if plot:
        
        trace = go.Scatter(
            name = 'Inliers',
            x = x[std], y = y[std],
            text = np.array(df.index).reshape(-1, 1)[std],
            mode = 'markers',
            marker = dict(
                size = 10,
                color = 'blue',
                opacity = 0.5
            )
        )
        
        outliers = go.Scatter(
            name = 'Outliers',
            x = x[~std], y = y[~std],
            text = np.array(df.index).reshape(-1, 1)[~std],
            mode = 'markers',
            marker = dict(
                size = 10,
                color = 'orange',
                opacity = 0.5
            )
        )
        
        scale = np.array([x[std].min(), x[std].max()]).reshape(-1, 1)
        line = go.Scatter(
            name = 'Trend line',
            x = scale.reshape(-1), y = model.predict(scale).reshape(-1),
            mode='lines',
            line=dict(color = 'red', width = 2.5)
        )
        
        layout = go.Layout(
            title = 'Tendency line {} - {}'.format(leix, leiy), 
            xaxis = dict(title = '{} - Normalized - {} - {}'.format(leix, years[0], indexes[0])),
            yaxis = dict(title = '{} - Normalized - {} - {}'.format(leiy, years[1], indexes[1])),
            annotations=[dict(x=-0.075, y=1.1, text='R2: {:0.4}'.format(r2), showarrow=False),
                        dict(x=-0.075, y=1.05, text='Coef: {:0.4}'.format(model.coef_[0][0]), showarrow=False)]
        )
        
        return py.iplot(go.Figure(data= [trace, outliers, line], layout=layout))
        
    else:
        return r2, model.coef_[0][0], std.sum(), '{} - {}'.format(leix, leiy)
    
def plotcorr(corr, r2min=0.75):
    '''
    Generates the correlation graph of GDP per capita of 2017 with all indexes in its years of highest r2
    
    Parameters:
    -----------
    
        data -> dataframe of correlation
        r2min -> minimum r2 value for filtering
    
    Return:
    -------
        
        plotly.plotly.iplot with the scatter plot of each index that went through the filtering
        
    Examples:
    ---------
    
        plotcorr(corr, 0.5)
    '''
    
    indices = list(set(corr.index.get_level_values(0)))
    years = list(set(corr.index.get_level_values(1)))
    r2, year, name = [], [], []
    for indice in indices:
        r2max = corr.loc[indice].sort_values('R2', ascending=False).iloc[0]
        if r2max[0] >= r2min:
            r2.append(r2max[0])
            year.append(r2max.name)
            name.append("{} <br>Coefficient: {:0.4} <br>Type of axis: {}".format(indice, r2max[1], r2max[3]))
    
    trace = go.Scatter(
        x = r2, y = year,
        text = name,
        mode = 'markers',
        marker = dict(
            size = 10,
            color = 'green',
            opacity = 0.5
        )
    )
    
    layout = go.Layout(
        title = 'Coefficient of determination (R2)', 
        xaxis = dict(title = 'R2'),
        yaxis = dict(title = 'Year')
    )

    return py.iplot(go.Figure(data= [trace], layout=layout))