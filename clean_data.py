import pandas as pd
import numpy as np
import functools as f

def longest_seq_data(data):
    max_s = []
    for i in data.T:
        index = data.T[i].isnull()
        nans = data.T[index].index.values
        fnans = np.concatenate((np.array([-1]),nans-1960))
        lnans = np.concatenate((nans-1960,np.array([len(data.columns)-3])))
        seq = lnans-fnans-1
        if len(nans)==0:
            max_s.append(len(data.columns)-3)
        else:
            max_s.append(max(seq))
    return pd.Series(max_s,index=data.index)

def clean_tb(df,crt,by_count=True):
    '''\nDocstring for clear_tb
    Parameters:
    -----------
    df : pandas Dataframe 
        A table to be cleaned
    data_critery_years : int
        Minimum number of data a contry must have to be kept in the Dataframe'''
    col = [df[i][2] for i in df.columns]
    df.columns = [int(i) if type(i) == np.float64 else i for i in col]
    df = df.drop([0,1,2])
    df = df.dropna(axis = 1,how = 'all')
    if by_count:
        df = df.dropna(thresh = crt)
    else:
        l_sequence = longest_seq_data(df)
        df = df.drop(index=[country for country in l_sequence.index if l_sequence(country) < crt])
    df.index = list(df['Country Name'])
    df = df.drop(['Country Name'],axis=1)
    return df          

def data_search(data,by,key):
    def search_by_year(list_tables,year):
        l = []
        labels = []

        for i in list_tables:
            if year in i.columns:
                l.append(pd.DataFrame(i[year]))
                df = f.reduce(lambda a,b: a.join(b,how='outer',rsuffix=i['Indicator Code'][0]),l)
                l = [df]
                labels.append(i['Indicator Name'][0])
        df.columns = labels
        return df
    
    def search_by_country(list_tables,country):
        l = []
        labels = []
        for i in list_tables:
            if country in i.index:
                l.append(pd.DataFrame(i.T[country]))
                df = f.reduce(lambda a,b: a.join(b,how='outer',rsuffix=i['Indicator Code'][0]),l)
                l = [df]
                labels.append(i['Indicator Name'][0])
        df.columns = labels
        return df.drop(['Country Code','Indicator Name','Indicator Code'])

    if by == 'country':
        return search_by_country(data,key)
    elif by == 'year':
        return search_by_country(data,key)
