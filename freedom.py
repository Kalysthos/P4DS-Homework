from Fnames import names
import pandas as pd
import os

gdp = pd.read_excel("http://api.worldbank.org/v2/en/indicator/NY.GDP.PCAP.CD?downloadformat=excel", Sheet_name='Data',header=3)['Country Name']
table_xls = os.listdir('Freedom')
freedom = [None]*len(table_xls)
for k,i in enumerate(table_xls):
    ind = pd.read_excel('Freedom/'+i)[i[5:9]+" Score"].append(pd.Series([0]), ignore_index=True).loc[:185]
    ind.index = names
    freedom[k] = ind.reindex(gdp)

    