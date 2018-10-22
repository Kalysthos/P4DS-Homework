import pandas as pd
import numpy as np
import functools as f

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
    
        
    df.index = list(df['Country Name'])
    df = df.drop(['Country Name'],axis=1)
    return df            

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

def data_search(data,by,key):
    if by == 'country':
        return search_by_country(data,key)
    elif by == 'year':
        return search_by_country(data,key)
