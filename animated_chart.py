from sklearn import linear_model, preprocessing
import numpy as np
from Continents import Continents
import numpy as np
import matplotlib.pyplot as plt
import plotly.plotly as py
from plotly.grid_objs import Grid, Column
from plotly.tools import FigureFactory as FF 
import pandas as pd
import time
import plotly
plotly.tools.set_credentials_file(username='Felvc027', api_key='j63ixa5dFTZ9Crf97maA')

def animated_chart(merged_df):
    '''
    Gera um plot animado. O eixo x merged_df.columns[3], sendo o eixo y merged_df.columns[2], a legenda sendo os continentes, o tamanho dos circulos sendo merged_df.columns[4] e o controle deslizante é a variação dos anos de 1975 a 2014.
    
    Parameters:
    -----------
    
        merged_df -> dataframe de 5 colunas, a configuração do gráfico exige formatação correta da coluna:
        eixo x merged_df.columns[3], 
        sendo o eixo y merged_df.columns[2], 
        A legenda sendo os continentes, 
        O tamanho dos circulos sendo merged_df.columns[4] 
        O controle deslizante é a variação dos anos de 1975 a 2014.
        
    Return:
    -------
        
        Um gráfico animado.
    
    Example:
    --------
    
        animated_chart(merged_df)     
    '''
    #Normalizando os dados para impedir problemas de escala:
    norm = lambda df: preprocessing.MinMaxScaler().fit_transform(np.array(df, dtype="float64").reshape(-1, 1))
    for i in merged_df.columns[2:-1]:
        merged_df[i] = norm(merged_df[i])
   
    #Criando lista de anos e continentes para usar na legenda e controle deslizante: 
    List_of_years = list(range(1975,2015))

    List_Of_Continents = list(set(Continents.values()))

    merged_df['Year']=merged_df['Year'].apply(int)

    columns = []
    # Fazendo o grid:
    for year in List_of_years:
        for continent in List_Of_Continents:
            dataset_by_year = merged_df[merged_df['Year'] == int(year)]
            dataset_by_year_and_cont = dataset_by_year[dataset_by_year['Continents'] == continent]
            for col_name in dataset_by_year_and_cont:
                column_name = '{year}_{continent}_{header}_gapminder_grid'.format(
                    year=year, continent=continent, header=col_name
                )
                a_column = Column(list(dataset_by_year_and_cont[col_name]), column_name)
                columns.append(a_column)

    grid = Grid(columns)
    url = py.grid_ops.upload(grid, 'GDP.rateplot'+str(time.time()), auto_open=False)
    url

    #Criando a figura:

    figure1 = {
        'data': [],
        'layout': {},
        'frames': [],
        'config': {'scrollzoom': True}
    }

    figure1['layout']['xaxis'] = {'title': list(merged_df.columns)[3], 'gridcolor': '#FFFFFF'}
    figure1['layout']['yaxis'] = {'title': list(merged_df.columns)[2], 'type': 'log', 'gridcolor': '#FFFFFF'}
    figure1['layout']['hovermode'] = 'closest'
    figure1['layout']['plot_bgcolor'] = 'rgb(223, 232, 243)'

    #Criando Controle Deslizante:

    sliders_dict = {
        'active': 0,
        'yanchor': 'top',
        'xanchor': 'left',
        'currentvalue': {
            'font': {'size': 20},
            'prefix': 'Year:',
            'visible': True,
            'xanchor': 'right'
        },
        'transition': {'duration': 300, 'easing': 'cubic-in-out'},
        'pad': {'b': 10, 't': 50},
        'len': 0.9,
        'x': 0.1,
        'y': 0,
        'steps': []
    }

    #Criando legendas:

    figure1['layout']['updatemenus'] = [
        {
            'buttons': [
                {
                    'args': [None, {'frame': {'duration': 500, 'redraw': False},
                             'fromcurrent': True, 'transition': {'duration': 300, 'easing': 'quadratic-in-out'}}],
                    'label': 'Play',
                    'method': 'animate'
                },
                {
                    'args': [[None], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate',
                    'transition': {'duration': 0}}],
                    'label': 'Pause',
                    'method': 'animate'
                }
            ],
            'direction': 'left',
            'pad': {'r': 10, 't': 87},
            'showactive': False,
            'type': 'buttons',
            'x': 0.1,
            'xanchor': 'right',
            'y': 0,
            'yanchor': 'top'
        }
    ]

    custom_colors = {
        'East Asia & Pacific': 'rgb(171, 99, 250)',
        'Europe & Central Asia': 'rgb(230, 99, 250)',
        'Africa': 'rgb(99, 110, 250)',
        'Latin America & Caribbean': 'rgb(25, 211, 243)',
        'Middle East & North Africa': 'rgb(50, 170, 255)',
        'North America':'rgb(215,20,20)',
        'South Asia':'rgb(20,215,20)',
        'Sub-Saharan Africa':'rgb(0,0,0)',
    }
    #Criando layout da figura:
    col_name_template = '{year}_{continent}_{header}_gapminder_grid'
    year = 1975
    for continent in List_Of_Continents:
        data_dict = {
            'xsrc': grid.get_column_reference(col_name_template.format(
                year=year, continent=continent, header=list(merged_df.columns)[3]
            )),
            'ysrc': grid.get_column_reference(col_name_template.format(
                year=year, continent=continent, header=list(merged_df.columns)[2]
            )),
            'mode': 'markers',
            'textsrc': grid.get_column_reference(col_name_template.format(
                year=year, continent=continent, header='Country'
            )),
            'marker': {
                'sizemode': 'area',
                'sizeref': 0.005,
                'sizesrc': grid.get_column_reference(col_name_template.format(
                     year=year, continent=continent, header=list(merged_df.columns)[4]
                )),
                'color': custom_colors[continent]
            },
            'name': continent
        }
        figure1['data'].append(data_dict)
    for year in List_of_years:
        frame = {'data': [], 'name': str(year)}
        for continent in List_Of_Continents:
            data_dict = {
                'xsrc': grid.get_column_reference(col_name_template.format(
                    year=year, continent=continent, header=list(merged_df.columns)[3]
                )),
                'ysrc': grid.get_column_reference(col_name_template.format(
                    year=year, continent=continent, header=list(merged_df.columns)[2]
                )),
                'mode': 'markers',
                'textsrc': grid.get_column_reference(col_name_template.format(
                    year=year, continent=continent, header='Country'
                )),
                'marker': {
                    'sizemode': 'area',
                    'sizeref': 0.005,
                    'sizesrc': grid.get_column_reference(col_name_template.format(
                         year=year, continent=continent, header=list(merged_df.columns)[4]
                    )),
                    'color': custom_colors[continent]
             },
            'name': continent
            }
            frame['data'].append(data_dict)

        figure1['frames'].append(frame)
        slider_step = {'args': [
            [year],
            {'frame': {'duration': 300, 'redraw': False},
             'mode': 'immediate',
           'transition': {'duration': 300}}
         ],
         'label': year,
         'method': 'animate'}
        sliders_dict['steps'].append(slider_step)

    figure1['layout']['sliders'] = [sliders_dict]
    
    #Plotando:
    return py.icreate_animations(figure1, 'Plot1CreditGDP'+str(time.time()))