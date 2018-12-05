'''Generate list of dataframes of World Bank data'''

import pandas as pd

table_links = [i for i in open('Indicators.txt').read().split() if i.startswith('htt')]
table_links = ['http://api.worldbank.org/v2/en/indicator/NY.GDP.PCAP.CD?downloadformat=excel', 'http://api.worldbank.org/v2/en/indicator/EN.ATM.CO2E.PC?downloadformat=excel']
data = [pd.read_excel(i, Sheet_name='Data',header=3) for i in table_links]
