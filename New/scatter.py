import numpy as np
from sklearn import linear_model, preprocessing

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

def remove_outliers(x, y, percent=2.5, parts = 10):
    '''Remove possible outliers'''
    
    model = findlinear(x, y, parts)
    distance = abs(y - model.predict(x))
    distance.dtype = 'float64'
    deviation = abs(distance - distance.mean())/np.std(distance) if np.std(distance) != 0 else distance*0
    part = (100-percent)/100*x.shape[0]
    for multiplier in np.arange(2., 5., 0.25):
        std = deviation < multiplier 
        if std.sum() >= part:
            return std
    
def scatter(data, years, indexes, plot=False):
    
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
            stdtest = remove_outliers(xitem[0], yitem[0])
            xin, yin = xitem[0][stdtest].reshape(-1, 1), yitem[0][stdtest].reshape(-1, 1)
            modeltest = linear_model.LinearRegression().fit(xin, yin)
            r2test = modeltest.score(xin, yin)
            if r2test >= r2:
                std = stdtest
                x, leix = xitem
                y, leiy = yitem
                model, r2 = modeltest, r2test
                    
    if plot:
        import plotly.plotly as py
        import plotly.graph_objs as go
        
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
        
        scale = np.array([x.min(), x.max()]).reshape(-1, 1)
        line = go.Scatter(
            name = 'Trend line',
            x = scale, y = model.predict(scale),
            mode='lines',
            line=dict(color = 'red', width = 2.5)
        )
        
        layout = go.Layout(
            title = 'Tendency line {} - {}'.format(leix, leiy), 
            xaxis = dict(title = '{} - Normalized - {}'.format(leix, indexes[0])),
            yaxis = dict(title = '{} - Normalized - {}'.format(leiy, indexes[1]))
        )
        
        return py.iplot(go.Figure(data= [trace, outliers, line], layout=layout))
        
    else:
        return r2, model.coef_[0][0], std.sum(), '{} - {}'.format(leix, leiy)