import pandas as pd
import numpy as np
import functools as f

def clean_tb(df,min_data=0,criteria=None):
    '''\n
    Cleans and organizes a given pandas.DataFrame df, removing the columns without
    data and filtering the countries with a criterion.
    Parameters:
    -----------
    df : pandas.Dataframe 
        A table to be cleaned.
    min_data : int
        Minimum number of data a country must have to be kept in the Dataframe.
    criteria : string
        If the criterion is 'count', the criterion to be used to filter 
        countries will be the number of years that the country contains
        non-zero data. If it is 'sequence', the criterion will be the largest 
        non-null data sequence in the country. If it is 'lasts', the criterion 
        used will be the sequence from the last year.
    To simply organize the table (without filtering the countries) just pass only the DataFrame.'''
    def longest_seq_data(data):
        '''\nReturns a pandas.Series containing the countries and the largest non-null data sequence length of each.
        Parameters:
        -----------
        data : pandas.DataFrame
            A table with the data to be counted.'''
        import numpy as np
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
    if all([type(i)==str for i in df.columns]) == True:
        df.columns = [int(i) if i.isnumeric() else i for i in df.columns]
    if all([bool(criteria),type(min_data)==int]):
        if criteria == 'count':
            df = df.dropna(thresh = min_data+4)
        elif criteria == 'sequence':
            l_sequence = longest_seq_data(df)
            df = df.drop(index=[country for country in l_sequence.index if l_sequence(country) < min_data])
        elif criteria == 'lasts':
            last_year = max([i for i in df.columns if type(i) == int])
            lasts = df[list(range(last_year-min_data+1,last_year+1))]
            remain_index = lasts.dropna(how='any').index
            df = df.drop(index = list(set(df.index) - set(remain_index)))
        
    df.index = list(df['Country Name'])
    df = df.drop(['Country Name'],axis=1)
    return df
