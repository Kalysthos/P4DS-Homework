import pandas as pd
ind = [i for i  in open('Indicators.txt').read().split() if i[:4] == 'http']
data, = [None]*len(ind), 
for k, i in enumerate(ind):
    data[k] = pd.read_excel(i, sheet_name='Data', header=3)