def analyze(data, ageorcountryorind, indice=False, rm=True, log=False, disp=False):
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    from sklearn import linear_model
    countries = [i.replace("\n", "") for i in open("countries.txt")]
    
    if type(ageorcountryorind) == int:
        country = pd.DataFrame(data[0][str(ageorcountryorind)], columns=[data[0]['Indicator Name'][0]])
        for k,i in enumerate(data[1:]):
            country = country.join(pd.Series(i[str(ageorcountryorind)], name=data[k+1]["Indicator Name"][0]), how="outer")
        df = country.reindex(countries) if rm else country
    
    elif ageorcountryorind[0:2] == "c-":
        ages = pd.DataFrame(data[0].T[ageorcountryorind[2:]][4:], columns=[data[0]["Indicator Name"][0]])
        for k,i in enumerate(data[1:]):
            ages = ages.join(pd.Series(i.T[ageorcountryorind[2:]][4:], name=data[k+1]["Indicator Name"][0]), how="outer")
        df = ages
        
    else:
        for i in data:
            if i['Indicator Name'][0] == ageorcountryorind:
                saida = i.drop("Indicator Name", axis=1)
                break
        df = saida.reindex(countries) if rm else saida

    if indice==False:
        return df.dropna(how='all')
    elif log:
        df = np.log(df[indice].dropna()) 
        if disp:
            y = np.array(df[indice[0]]).reshape(-1, 1)
            x = np.array(df[indice[1]]).reshape(-1, 1)
            model = linear_model.LinearRegression().fit(x, y)
            plt.plot(x, model.predict(x), color='red', linewidth=2.)
            plt.scatter(y=y, x=x, color='blue', s=50, alpha=.5)
            plt.title('Reta ajustada log-log')
            plt.xlabel(indice[0])
            plt.ylabel(indice[1])
            plt.show()
        else:
            return df
    else:
        df = df[indice].dropna()
        if disp:
            y = df[indice[0]]
            x = df[indice[1]]
            plt.scatter(y=y, x=x, color='blue', s=50, alpha=.5)
            plt.title('Gráfico de dispersao')
            plt.xlabel(indice[0])
            plt.ylabel(indice[1])
            plt.show()
        else:
            return df
        