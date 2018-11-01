import pandas as pd

table_links = [i for i in open('Indicators.txt').read().split() if i.startswith('htt')]
data = [None]*len(table_links)
for k,i in enumerate(table_links):
    ind = pd.read_excel(i, Sheet_name='Data',header=3).drop(["Country Code", "Indicator Code"], 1)
    ind.index = ind["Country Name"]
    data[k] = ind.drop("Country Name",1)
    
