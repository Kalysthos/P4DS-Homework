def analyze(data, ageorcountryorind, indice=False, rm=True, log=False, disp=False):
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    from sklearn import linear_model
    countries = [i.replace("\n", "") for i in open("countries.txt")]
    if type(ageorcountryorind) == int:
        country,indices = pd.DataFrame(data[0]['Country Name']), ['Country']    
        for k,i in enumerate(data):
            indices += [data[k]['Indicator Name'][0]]
            country = country.join(i[str(ageorcountryorind)])
            country.columns = indices
        country.index = country["Country"]
        country = country.drop("Country",1)
        df = country.reindex(countries) if rm else country
    
    elif ageorcountryorind[0:2] == "c-":
        ages = data[0]
        coun = ages["Country Name"]
        ages.index = coun
        ages = ages.drop("Country Name",1)
        ages, indic = pd.DataFrame(ages.T[ageorcountryorind[2:]][4:]), [data[0]["Indicator Name"][0]]
        for k,i in enumerate(data[1:]):
            ages.columns = indic
            i.index = coun
            i = i.drop("Country Name",1)
            indic += [data[k+1]["Indicator Name"][0]]
            ages = ages.join(i.T[ageorcountryorind[2:]][4:])
        df = ages.reindex(countries) if rm else ages
        
    else:
        for i in data:
            if i['Indicator Name'][0] == ageorcountryorind:
                saida = i.drop(["Country Code", "Indicator Name", "Indicator Code"], axis=1)
                saida.index = i['Country Name']
                break
        df = saida.drop("Country Name",1).reindex(countries) if rm else saida

    if indice==False:
        return df
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
        