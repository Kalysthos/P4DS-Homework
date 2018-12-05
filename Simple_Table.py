import pandas as pd
def simple_table(indicator):
    '''
    Gera um Data Frame com ano, indicador e países como colunas para facilitar o uso de pacotes de visualização como altair e plotly.
    
    Parameters:
    -----------
    
        Indicator: Nome do indicador que deseja fazer a tabela que deve estar incluído na lista de nomes oficiais do banco mundial, que encontra.-se no módulo indexes
        
    Return:
    -------
        
         DataFrame com três colunas (Year, Contry, Indicator), excluindo valores NA.
    
    Example:
    --------
    
        simple_table('GDP per capita (current US$)')
    '''

    #UTILIZANDO O MÓDULO data.pickle PARA ABRIR DADOS DO PIB PER CAPITA DOS PAÍSES NOS ANOS DE 1975 A 2015:
    indicator_df=pd.read_pickle('New/data.pickle').loc[indicator][[str(num) for num in range(1975,2015)]]

    #EXCLUINDO CÉDULAS VAZIAS:
    cols = []
    for i in range(1975,2015):
        cols.append(str(i))
    indicator_df = indicator_df[cols].dropna()

    #ADAPTANDO A TABELA DE MODO A FACILITAR O USO DO PLOTLY:
    indicator_table=pd.DataFrame()
    for i in indicator_df.index:
            x=pd.DataFrame({'Year':indicator_df.columns,'Country':[i]*len(indicator_df.columns),indicator:indicator_df.T[i]})
            indicator_table=pd.concat([indicator_table,x])
    indicator_table=indicator_table.fillna(0)
    return indicator_table