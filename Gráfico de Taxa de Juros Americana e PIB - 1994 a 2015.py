#Importando Pacotes:
import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt
import geopandas as gpd
import altair as alt
import os as os
#Importando Módulos:
from freedom import freedom
from analyze import analyze
from data2 import data2
#Importando Mais Limpeza de dados:
import clean_data as cd

#Gerando Dados do PIB Mundial
gdp_world = cd.clean_tb(data2[0]).T['World']
gdp_world = pd.DataFrame({'Year':gdp_world.index[3:],'Gdp_World':gdp_world[3:]})
gdp_world=gdp_world[3:-1]
gdp_world

#Gerando dados da Taxa de Juros Real americana
from data import data 
real_rate = analyze(data,"c-United States",['Real interest rate (%)'])
real_rate.reset_index(level=0, inplace=True)
real_rate.columns=['Year','Real_rate_us']
real_rate.index=gdp_world.index
real_rate

#Plotando Gráficos
join = pd.DataFrame(gdp_world).join(real_rate['Real_rate_us'])
alt.renderers.enable('notebook')
brush = alt.selection(type='interval', encodings=['x'])

real_rate_chart = alt.Chart(join).mark_line().encode(
  x=alt.X('Year:N'),
  y=alt.Y('Real_rate_us:Q')
).properties(
  title='Taxa Real de Juros Americana'
).add_selection(
    brush
)


gdp_world_chart = alt.Chart(join).mark_line().encode(
  x=alt.X('Year:N', scale=alt.Scale(zero=False)),
  y=alt.Y('Gdp_World:Q', scale=alt.Scale(zero=False)),
).properties(
  title='PIB Mundial percapita'
).transform_filter(
  brush
)


real_rate_chart | gdp_world_chart
