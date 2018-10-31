import pandas as pd
import os
table_links = [i for i in open('Indicators.txt').read().split() if i.startswith('htt')]
data = [pd.read_excel(i, Sheet_name='Data',header=3).drop(["Country Code", "Indicator Code"], axis=1) for i in table_links]
freedom = [pd.read_excel('Freedom/'+i)[["Country Name", i[5:9]+" Score"]] for i in os.listdir('Freedom')]
