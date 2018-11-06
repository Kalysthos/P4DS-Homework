#Importando Pacotes:
import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt
import geopandas as gpd
import altair as alt
import os as os
alt.renderers.enable('notebook')
#Importando Módulos:
from freedom import freedom
from data import data
from analyze import analyze
#Importando Mais Limpeza de dados:
import clean_data

#Criando DataFrameResumido
market = analyze(data,"Market capitalization of listed domestic companies (current US$)")[[str(num) for num in range(1987,2018)]]
list_year= [str(num) for num in range(1987,2018)]
top_market=pd.DataFrame()
for i in list_year:
    market = pd.DataFrame(market[i])
    market = market[market[i]>0].sort_values(i)[-4:]
    top_market = pd.concat([top_market, market], axis=1, sort=False)
    market = analyze(data,"Market capitalization of listed domestic companies (current US$)")[[str(num) for num in range(1987,2018)]]
top_market=top_market.fillna(0)
top_market=market.T[top_market.index].T
top_market

#Organzizando de maneira a facilitar a construção do gráfico em altair:
top_market_chart=pd.DataFrame()
for i in top_market.index:
        x=pd.DataFrame({'year':top_market.columns,'Country':[i]*len(top_market.columns),'Market Capitalization':top_market.T[i]})
        top_market_chart=pd.concat([top_market_chart,x])
top_market_chart=top_market_chart.fillna(0)
top_market_chart

#Plotagem do Gráfico
chart=alt.Chart(top_market_chart).mark_area().encode(
    x='year:T',
    y='Market Capitalization:Q',
    color='Country:N'
)
chart
