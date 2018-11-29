import numpy as np
from sklearn import linear_model

class divid:
    def __init__(self, x, n):
        self.x, self.cut = x, [None]*n
        for i in range(n):
            self.cut[i] = x//n*i + np.arange(x//n + 1 if x%n - i > 0 else x//n)     
    def split(self, n):
        return np.setdiff1d(np.arange(self.x), self.cut[n])
    
def findlinear(x, y, div=10):
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

def remove_outliers(x, y, percent=5):
    model = findlinear(x, y)
    dist = abs(y - model.predict(x))
    desv = abs(dist - dist.mean())/np.std(dist) if np.std(dist).dtype == 'float64' and np.std(dist) != 0 else dist - dist
    part = (100-percent)/100*x.shape[0]
    for m in np.arange(2., 5., 0.25):
        std = desv < m 
        if std.sum() > part:
            return x[std].reshape(-1, 1), y[std].reshape(-1, 1)
    
def scatter(data, years, indexes, plot=False):
    
    df = np.append(np.array(data.loc[(indexes[0]), [str(years[0])]]).reshape(-1, 1), np.array(data.loc[indexes[1]][str(years[1])]).reshape(-1, 1), axis=1)
    df = df[~np.any(np.isnan(df), axis=1), :]
    
    if df.shape[0] < 20:
        raise ValueError('Without enough data')
        
    x = df[:,0].reshape(-1, 1)
    y = df[:,1].reshape(-1, 1)
    xlist = [(np.log(x), "log(x)"), (x, "x")] if x.min() > 0 else [(x, "x")]
    ylist = [(np.log(y), "log(y)"), (y, "y")] if y.min() > 0 else [(y, "y")]
    r2 = 0
    for i in xlist:
        for k in ylist:
            try:
                xin, yin = remove_outliers(i[0], k[0])
            except:
                xin, yin = i[0], k[0]
            modeltest = linear_model.LinearRegression().fit(xin, yin)
            r2test = modeltest.score(xin, yin)
            if r2test >= r2:
                x, y = xin, yin
                leix, leiy = i[1], k[1]
                model, r2 = modeltest, r2test
                    
    if plot:
        import matplotlib.pyplot as plt
        plt.scatter(x, y, color='blue', s=50, alpha=.5)
        plt.plot(x, model.predict(x), color='red', linewidth=2.)
        plt.legend(["R**2 = {:0.4}".format(r2)])
        plt.title('Tendency line {} - {}'.format(leix, leiy))
        plt.xlabel(indexes[0])
        plt.ylabel(indexes[1])
        plt.show()
        
    else:
        return r2, model.coef_[0][0], x.shape[0], '{} - {}'.format(leix, leiy)