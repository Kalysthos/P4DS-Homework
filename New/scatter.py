import numpy as np
from sklearn import linear_model, preprocessing

norm = lambda x: preprocessing.MinMaxScaler().fit_transform(x)
cube = lambda x: x**(1/3) if x >= 0 else -abs(x)**(1/3)

class divid:
    def __init__(self, x, n):
        self.x, self.cut = x, [None]*n
        for i in range(n):
            self.cut[i] = x//n*i + np.arange(x//n + 1 if x%n - i > 0 else x//n)     
    def split(self, n):
        return np.setdiff1d(np.arange(self.x), self.cut[n])
    
def findlinear(x, y, div=10):
    np.random.seed(0)
    order = np.random.permutation(x.shape[0])
    x, y = x[order], y[order]
    split = divid(x.shape[0], div)
    r2 = 0
    for i in range(div):
        index = split.split(i)
        xtest, ytest = x[index], y[index]
        modeltest = linear_model.LinearRegression().fit(xtest, ytest)
        r2test = modeltest.score(xtest,ytest)
        if r2test > r2:
            r2, model = r2test, modeltest
    return model

def remove_outliers(x, y, percent=2.5):
    model = findlinear(x, y)
    dist = abs(y - model.predict(x))
    desv = abs(dist - dist.mean())/np.std(dist) if np.std(dist).dtype == 'float64' and np.std(dist) != 0 else dist - dist
    part = (100-percent)/100*x.shape[0]
    for m in np.arange(2., 5., 0.25):
        std = desv < m 
        if std.sum() > part:
            return std
    
def scatter(data, years, indexes, plot=False):
    
    df = data.loc[(indexes[0]), [str(years[0])]].rename(columns = lambda x: '0').join(data.loc[indexes[1]][str(years[1])]).dropna()
    
    if df.shape[0] < 20:
        raise ValueError('Without enough data')
        
    x = np.array(df['0']).reshape(-1, 1)
    y = np.array(df[str(years[1])]).reshape(-1, 1)
    xlist = [(norm(np.log(x)), "log(x)"), (norm(x), "x")] if x.min() > 0 else [(norm(cube(x)), "x**(1/3)"), (norm(x), "x")]
    ylist = [(norm(np.log(y)), "log(y)"), (norm(y), "y")] if y.min() > 0 else [(norm(cube(y)), "y**(1/3)"), (norm(y), "y")]
    r2 = 0
    for i in xlist:
        for k in ylist:
            stdtest = remove_outliers(i[0], k[0])
            xin, yin = i[0][stdtest].reshape(-1, 1), k[0][stdtest].reshape(-1, 1)
            modeltest = linear_model.LinearRegression().fit(xin, yin)
            r2test = modeltest.score(xin, yin)
            if r2test >= r2:
                std = stdtest
                x, y = i[0], k[0]
                leix, leiy = i[1], k[1]
                model, r2 = modeltest, r2test
                    
    if plot:
        import plotly.plotly as py
        import plotly.graph_objs as go
        
        trace = go.Scatter(
            name = 'Inliers',
            x = x[std],
            y = y[std],
            text = np.array(df.index).reshape(-1, 1)[std],
            mode = 'markers',
            marker = dict(
                size = 10,
                color = 'blue',
                opacity = 0.5,
            )
        )
        
        outliers = go.Scatter(
            name = 'Outliers',
            x = x[~std],
            y = y[~std],
            text = np.array(df.index).reshape(-1, 1)[~std],
            mode = 'markers',
            marker = dict(
                size = 10,
                color = 'orange',
                opacity = 0.5,
            )
        )
        
        scale = np.array([x.min(), x.max()]).reshape(-1, 1)
        line = go.Scatter(
            name = 'Trend line',
            x = scale,
            y = model.predict(scale),
            mode='lines',
            line=dict(color = 'red', width = 2.5,
            )
        )
        
        layout = go.Layout(
            title = 'Tendency line {} - {}'.format(leix, leiy), 
            xaxis = dict(title = '{} - Normalized - {}'.format(leix, indexes[0])),
            yaxis = dict(title = '{} - Normalized - {}'.format(leiy, indexes[1]))
        )
        
        return py.iplot(go.Figure(data= [trace, outliers, line], layout=layout))
        
    else:
        return r2, model.coef_[0][0], std.sum(), '{} - {}'.format(leix, leiy)