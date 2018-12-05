P4DS-Homework

Este repositório trata-se de uma análise de indicadores econômicos e sua influência no PIB percapita. Nós faremos uma análise de longo e curto prazo e já contamos com as primeiras análises. 
Vamos ao que você precisa para entender nosso trabalho:

0. De antemão os módulos serão utilizados são:

pandas
numpy
seaborn
matplotlib.pyplot
geopandas
altair
os
sklearn

1. Os dados foram todos do Banco Mundial, o banco mundial possui um relatório para cada indicador com argumentos gerais que justificam porque um indicador pode ser importante para o desenvolvimento, a partir de sua indcação da importância do mercado de capitais, começamos nossa análise estudando esse indicador. Na nossa primeira análise chegamos a conclusão que no curto prazo taxa de juros real americana possui forte relação negativa com o PIB Mundial que pode ser explicado pela teoria econômica, você conferir nosso trabalho em Análise e Visualização - PartialProject.ipynb. Cada passagem está descrita no código e as variáveis foram nomeadas de forma que você consiga entender o código. 
2. As primeiras linhas do código é a importação dos pacotes e dados que serão utilizados, pode ser que demore um pouco pois a quantidades de dados é grande, não se preocupe. 
3. As funções de limpeza são : 

•	Indicators (indices escolhidos para análise):
Link: https://github.com/Kalysthos/P4DS-Homework/blob/master/Indicators.txt  

•	 Data e Data2(extração dos dados automática):
Link para Data: https://github.com/Kalysthos/P4DS-Homework/blob/master/data.py  
(O date2 é uma variação de data menos trabalhosa)

•	Clean_Data(Limpeza e Organização das Tabelas): 
Link: https://github.com/Kalysthos/P4DS-Homework/blob/master/clean_data.py  

•	Analyze (Função para facilitar a seleção de dados para objetivos específicos):
Link: https://github.com/Kalysthos/P4DS-Homework/blob/master/analyze.py  

•	 Countries(Arquivo com nomes de países - para separar países dos blocos):
Link: https://github.com/Kalysthos/P4DS-Homework/blob/master/countries.txt   
Em outros módulos você também encontra o trabalho fragmentado. 
Nossa apresentação em slides se encontra em: P4DS - GDP - PowerPoint.pptx.
