def analise(age,index=False, gdp=False, regression=False):
    import scipy as sp
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import statsmodels.formula.api as sm
    import indic
    if age==False:
        print(indic.indices.replace("_", " ").replace(".xls",""))
        return
    ind = indic.indices.split()
    lista, k = [None]*len(ind), 0
    for i in ind:
        lista[k] = pd.read_excel(i, sheet_name='Data', header=3)
        k+=1
    data,k,indices = pd.DataFrame(lista[0]['Country Name']),0, ['Country']
    for i in lista:
        indices += [ind[k].replace("_"," ").replace(".xls","")]
        data = data.join(i[str(age)])
        data.columns = indices
        k+=1
    data.index = data["Country"]
    data = data.drop("Country",1)
    if index == False:
        return data
    elif gdp == False:
        return data[index]
    elif regression == False:
        return data[[index,'GDP per capita']].dropna()
    else:
        comp = data[[index,'GDP per capita']].dropna()
        var, comp.columns = 0, ["x","y"]
        for i in np.arange(0.01,5.01,0.01):
            reg = sm.ols(formula='y~pow(x,{})'.format(i), data=comp).fit()
            if reg.rsquared > var:
                var = reg.rsquared
                k = i
        reg = sm.ols(formula='y~pow(x,{})'.format(k), data=comp).fit()
        if regression == "analise":
            return (reg.rsquared, reg.params)
        elif regression == "plot":
            print(reg.params)
            print("r**2: {}".format(reg.rsquared))
            print("Country: {}".format(len(comp)))
            plt.scatter(y=comp['y'], x=comp['x'], color='blue', s=50, alpha=.5)
            X_plot = sp.linspace(min(comp['x']), max(comp['x']), len(comp['x']))
            plt.plot(X_plot, (X_plot**k)*reg.params[1] + reg.params[0], color='r')
            plt.title('Curva Ajustada')
            plt.xlabel(index)
            plt.ylabel("GDP per capita")
            plt.show()
        else:
            return reg.summary()