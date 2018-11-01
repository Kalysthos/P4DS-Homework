from Fnames import names
import pandas as pd
import os

gdp = pd.read_excel("http://api.worldbank.org/v2/en/indicator/NY.GDP.PCAP.CD?downloadformat=excel", Sheet_name='Data',header=3)['Country Name']
table_xls = os.listdir('Freedom')
freedom = pd.DataFrame(pd.read_excel('Freedom/'+table_xls[0])[table_xls[0][5:9]+" Score"].append(pd.Series([0]), ignore_index=True).loc[:185])
freedom.columns = [2013]
for k,i in enumerate(table_xls[1:]):
    ind = pd.DataFrame(pd.read_excel('Freedom/'+i)[i[5:9]+" Score"].append(pd.Series([0]), ignore_index=True).loc[:185])
    ind.columns=[2014+k]
    freedom = freedom.join(ind)
freedom.index = names
freedom = freedom.reindex(gdp).dropna(how='all')
