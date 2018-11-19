import pandas as pd

def analyze(data, parameter='GDP per capita (current US$)'):
    '''Generates the Dataframe of data(list of Dataframes) from year (int), index (str) or country (str with "c-" at start)'''
    
    if type(parameter) == int:
        country = pd.DataFrame(data[0][str(parameter)]).rename(columns=lambda x: data[0]['Indicator Name'][0])
        for k,i in enumerate(data[1:]):
            country = country.join(pd.Series(i[str(parameter)], name=data[k+1]["Indicator Name"][0]))
        return country.dropna(how='all') 
    
    elif parameter[0:2] == "c-":
        years = pd.DataFrame(data[0].T[parameter[2:]][4:]).rename(columns=lambda x: data[0]["Indicator Name"][0])
        for k,i in enumerate(data[1:]):
            years = years.join(pd.Series(i.T[parameter[2:]][4:], name=data[k+1]["Indicator Name"][0]))
        return years.dropna(how='all')
        
    else:
        for i in data:
            if i['Indicator Name'][0] == parameter:
                return i.drop("Indicator Name", axis=1).dropna(how='all') 
