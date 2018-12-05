import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model

def func1():
    f, ax = plt.subplots(figsize=(7.5, 5))
    x = np.arange(1,21).reshape(-1, 1)
    y = 2*x + 10
    ax.scatter(x, y)
    model = linear_model.LinearRegression().fit(x, y)
    ax.plot(x, model.predict(x), color='red', linewidth=2.)
    ax.legend(['Y = {}*X + {}'.format(int(model.coef_[0][0]), int(model.intercept_[0]))])
    ax.set(xlabel = 'X', ylabel = 'Y', title = "Curva linear")
    plt.show()
    
def func2():
    f, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
    x1 = np.arange(1,21).reshape(-1, 1)
    y1 = 10*2**x1
    ax1.scatter(x1, y1)
    ax1.legend(['Y = 10*2**X'])
    ax1.set(xlabel = 'X', ylabel = 'Y', title = "Curva exponencial")
    
    x2 = x1
    y2 = np.log(y1)
    ax2.scatter(x2, y2)
    model = linear_model.LinearRegression().fit(x2, y2)
    ax2.plot(x2, model.predict(x2), color='red', linewidth=2.)
    ax2.legend(['Y = {:0.4}*X + {}'.format(model.coef_[0][0], int(model.intercept_[0]))])
    ax2.set(xlabel = 'X', ylabel = 'log(Y)', title = "Curva linear")
    plt.show()
    
def func3():
    f, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
    x1 = np.arange(1,21).reshape(-1, 1)
    y1 = 5*x1**6
    ax1.scatter(x1, y1)
    ax1.legend(['Y = 5*X**6'])
    ax1.set(xlabel = 'X', ylabel = 'Y', title = "Curva de potência")

    x2 = np.log(x1)
    y2 = np.log(y1)
    ax2.scatter(x2, y2)
    model = linear_model.LinearRegression().fit(x2, y2)
    ax2.plot(x2, model.predict(x2), color='red', linewidth=2.)
    ax2.legend(['Y = {:0.4}*X + {}'.format(model.coef_[0][0], int(model.intercept_[0]))])
    ax2.set(xlabel = 'log(X)', ylabel = 'log(Y)', title = "Curva linear")
    plt.show()

    f, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
    x1 = np.arange(1,21).reshape(-1, 1)
    y1 = 2*x1**3 + x1**2 + 10
    ax1.scatter(x1, y1)
    ax1.legend(['Y = 2*X**2 + X**2 + 10'])
    ax1.set(xlabel = 'X', ylabel = 'Y', title = "Curva polinomial")

    x2 = np.log(x1)
    y2 = np.log(y1)
    ax2.scatter(x2, y2)
    model = linear_model.LinearRegression().fit(x2, y2)
    ax2.plot(x2, model.predict(x2), color='red', linewidth=2.)
    ax2.legend(['Y = {:0.4}*X + {}'.format(model.coef_[0][0], int(model.intercept_[0]))])
    ax2.set(xlabel = 'log(X)', ylabel = 'log(Y)', title = "Curva linear")
    plt.show()
    
def func4():
    f, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
    x1 = np.arange(1,21).reshape(-1, 1)
    y1 = 2*x1 + 3
    ax1.scatter(x1, y1)
    model = linear_model.LinearRegression().fit(x1, y1)
    ax1.plot(x1, model.predict(x1), color='red', linewidth=2.)
    ax1.set(xlabel = 'X', ylabel = 'Y', title = "Y = 2*X + 3")
    ax1.legend(["R2 = {:0.4}".format(model.score(x1, y1))])

    x2 = x1
    y2 = np.random.random(20)
    ax2.scatter(x2, y2)
    model = linear_model.LinearRegression().fit(x2, y2)
    ax2.plot(x2, model.predict(x2), color='red', linewidth=2.)
    ax2.legend(["R2 = {:0.4}".format(model.score(x2, y2))])
    ax2.set(xlabel = 'X', ylabel = 'Y', title = "Y = aleatório")
    plt.show()
    
def func5():
    f, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
    x = np.arange(1,10).reshape(-1, 1)
    y = np.append(2*x[:-1], [1])
    ax1.scatter(x, y)
    model = linear_model.LinearRegression().fit(x, y)
    ax1.set(xlabel = 'X', ylabel = 'Y', title = "Com o outlier")
    ax1.plot(x, model.predict(x), color='red', linewidth=2.)

    x2 = x
    y2 = 2*x[:-1]
    ax2.scatter(x2, np.append(y2, [1]))
    model = linear_model.LinearRegression().fit(x2[:-1], y2)
    ax2.set(xlabel = 'X', ylabel = 'Y', title = "Sem o outlier")
    ax2.plot(x2[:-1], model.predict(x2[:-1]), color='red', linewidth=2.)
    plt.show()
    
def func6():
    from searching_data import data_search
    from clean_data import clean_tb
    import numpy as np
    import pandas as pd
    from sklearn.preprocessing import MinMaxScaler
    import plotly.offline as py
    import plotly.graph_objs as go
    py.init_notebook_mode(connected=True)
    import matplotlib.pyplot as plt
    
    import data2 as d
    norm = lambda df: MinMaxScaler().fit_transform(np.array(df, dtype="float64").reshape(-1, 1))
    
    tbs = [clean_tb(df,17,'lasts') for df in d.data if len(clean_tb(df,17,'lasts').index) > 0]
    
    co2_emission=data_search(tbs,'index','CO2 emissions (metric tons per capita)').T[3:].dropna()
    
    gdp=data_search(tbs,'index','GDP per capita (current US$)').T[3:].dropna()
    
    co2_emission,gdp=co2_emission[4:-1],gdp[:-4]
    for col in co2_emission.columns:
        co2_emission[col] = norm(co2_emission[col])
    for col in gdp.columns:
        gdp[col]=norm(gdp[col])
    countries=[i for i in gdp.columns if i in co2_emission.columns]
    parameters={}
    As = {}
    bs = {}
    for country in countries:
        A = np.concatenate([co2_emission[country].values.reshape(-1,1).astype(float),
                            gdp[country][:-1].values.reshape(-1,1).astype(float),np.ones([12,1]).astype(float)],axis=1)
        b = gdp[country][1:].values.reshape(-1,1).astype(float)
        parameters[country]=np.linalg.solve(np.dot(A.T,A),np.dot(A.T,b))
        As[country]=A
        bs[country]=b
    real_gdp = data_search(tbs,'index','GDP per capita (current US$)').T[3:].dropna()
    maxis = dict(zip(countries,[real_gdp[i][:-4].max() for i in countries]))
    minis= dict(zip(countries,[real_gdp[i][:-4].min() for i in countries]))
    shots=[((np.dot(As[i],parameters[i])*(maxis[i]-minis[i]))+(minis[i])) for i in countries]
    
    err = [sum((real_gdp[countries[i]][1:-4].values.reshape(-1,1)-shots[i])**2)/len(shots[i]) for i in range(len(countries))]
    
    k=countries.index('Qatar')
    
    shots2014=[]
    for i in countries:
        min_tr=min(data_search(tbs,'index','CO2 emissions (metric tons per capita)').T[3:].dropna()[i][:-1])
        max_tr=max(data_search(tbs,'index','CO2 emissions (metric tons per capita)').T[3:].dropna()[i][:-1])
        co2_test=data_search(tbs,'index','CO2 emissions (metric tons per capita)').T[3:].dropna()[i][2014]
        co2_test-=min_tr
        co2_test/=(max_tr-min_tr)

        gdp_test=real_gdp[i][2013]
        min_gdps=min(data_search(tbs,'index','GDP per capita (current US$)').T[3:].dropna()[i][:-5])
        max_gdps=max(data_search(tbs,'index','GDP per capita (current US$)').T[3:].dropna()[i][:-5])
        gdp_test-=min_gdps
        gdp_test /= (max_gdps-min_gdps)
        shot2014=np.dot(np.array([co2_test,gdp_test,1]),parameters[i].reshape(3,1))
        shot2014 *= (max_gdps-min_gdps)
        shot2014 += min_gdps
        shots2014.append(shot2014)
        
    gdp2014 = data_search(tbs,'index','GDP per capita (current US$)').T[3:].dropna()[countries][-4:-3].T
    RealXModel = gdp2014.join(pd.DataFrame(shots2014,index=countries,columns=['Model Shot'])).sort_values('Model Shot')

    Real_GDP = go.Scatter(
        y = np.array(RealXModel[2014]), text = RealXModel.index,
        mode='lines',
        line=dict(color = 'red', width = 2)
    )

    trace2 = go.Scatter(
        y = np.array(RealXModel['Model Shot']), text = RealXModel.index,
        mode='lines',
        line = dict(color = 'blue', width = 2),
        name='Real GDP'
    )

    layout = go.Layout(
        title = 'Real GDP X Model Shot', 
        xaxis = dict(title = 'GDP'),
        yaxis = dict(title = 'GDP per capita'),
        name='Model Shot'
    )

    return py.iplot(go.Figure(data= [Real_GDP, trace2], layout=layout))
    
    