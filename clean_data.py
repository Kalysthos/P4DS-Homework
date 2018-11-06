import pandas as pd
import numpy as np
import functools as f

def clean_tb(df,crt,by_count=True):
    '''\nCleans and organizes a given pandas.DataFrame df, removing the columns without data and filtering
    the countries with a criterion.
    Parameters:
    -----------
    df : pandas.Dataframe 
        A table to be cleaned.
    data_critery_years : int
        Minimum number of data a contry must have to be kept in the Dataframe.
    by_count : bool
        If by_count is True, the criteria to be used to filter countries will be the number of years
        that country contains non-null data. If it is False, the criterion will be the largest non-null 
        data string in the country.'''
    def longest_seq_data(data):
        '''\nReturns a pandas.Series containing the countries and the largest non-null data sequence length of each.
        Parameters:
        -----------
        data : pandas.DataFrame
            A table with the data to be counted.'''

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
    df = df.dropna(axis = 1,how = 'all')
    if by_count:
        df = df.dropna(thresh = crt+3)
    else:
        l_sequence = longest_seq_data(df)
        df = df.drop(index=[country for country in l_sequence.index if l_sequence(country) < crt])
        
    df.index = list(df['Country Name'])
    df = df.drop(['Country Name'],axis=1)
    return df
