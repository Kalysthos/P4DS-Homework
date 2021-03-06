def data_search(data,by,key):
    '''\nReturns a table with specific data for a given year, country, or index.
        Parameters
        -----------
        data : list
            The list of DataFrames with the data.
        by : {'year','index','country'}
            Specifies the type of key to be used.
        key : string
            The keyword that must be used to find the data.'''
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
    def search_by_index(list_tables,index):
        for i in list_tables:
            if index == i['Indicator Name'][0]:
                return i

    if by == 'country':
        return search_by_country(data,key)
    elif by == 'year':
        return search_by_year(data,key)
    elif by == 'index':
        return search_by_index(data,key)
        
