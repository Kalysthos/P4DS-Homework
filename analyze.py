def analyze(data, parameter='GDP per capita (current US$)', nocountries=True):
    '''Dataframe of data from year (integer), index (name) or country (name with "c-" at start)'''

    import pandas as pd
    countries = [i.replace("\n", "") for i in open("countries.txt")]
    
    if type(parameter) == int:
        country = pd.DataFrame(data[0][str(parameter)]).rename(columns=lambda x: data[0]['Indicator Name'][0])
        for k,i in enumerate(data[1:]):
            country = country.join(pd.Series(i[str(parameter)], name=data[k+1]["Indicator Name"][0]))
        return country.reindex(countries).dropna(how='all') if nocountries else country.dropna(how='all')
    
    elif parameter[0:2] == "c-":
        ages = pd.DataFrame(data[0].T[parameter[2:]][4:]).rename(columns=lambda x: data[0]["Indicator Name"][0])
        for k,i in enumerate(data[1:]):
            ages = ages.join(pd.Series(i.T[parameter[2:]][4:], name=data[k+1]["Indicator Name"][0]))
        return ages.dropna(how='all')
        
    else:
        for i in data:
            if i['Indicator Name'][0] == parameter:
                return i.drop("Indicator Name", axis=1).reindex(countries).dropna(how='all') if nocountries else i.drop("Indicator Name", axis=1).dropna(how='all')

