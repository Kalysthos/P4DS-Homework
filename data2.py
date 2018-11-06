import pandas as pd

table_links = [i for i in open('Indicators.txt').read().split() if i.startswith('htt')]
data2 = [pd.read_excel(i, Sheet_name='Data',header=3) for i in table_links]
