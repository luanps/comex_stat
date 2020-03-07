# Análise da base de dados do Comércio exterior brasileiro

Este repositório tem como finalidade analisar os dados públicos de importação e 
exportação do Brasil fornecidos pelo
[Ministério da Economia](http://www.mdic.gov.br/index.php/comercio-exterior/estatisticas-de-comercio-exterior/base-de-dados-do-comercio-exterior-brasileiro-arquivos-para-download)


## Instalação

*use python >= 3.6*
```
pip3 install -r requirements.txt
```

## Download e extração da base de dados utilizada 
```
wget http://www.mdic.gov.br/balanca/bd/comexstat-bd/ncm/EXP_COMPLETA.zip
wget http://www.mdic.gov.br/balanca/bd/comexstat-bd/ncm/IMP_COMPLETA.zip
unzip EXP_COMPLETA.zip
unzip IMP_COMPLETA.zip
mv EXP_COMPLETA.csv IMP_COMPLETA.csv ata/
mkdir models
```

## Como executar
```
python3 main.py
```

## Definições de modelagem

#### Como foi a definição da sua estratégia de modelagem?

Inicialmente foi realizado uma análise exploratória no conjunto de dados, 
removendo aquelas que julguei não serem necessárias para a condução deste estudo.
Em seguida, foram verificadas as propriedades de cada variável restante,
tais como seu o
[tipo](https://github.com/luanps/airbnb/blob/a15943ce4c7eaba434b775322d7ae1a801222a8a/log.txt#L7-L118),
[descrição](https://github.com/luanps/airbnb/blob/a15943ce4c7eaba434b775322d7ae1a801222a8a/log.txt#L120-L725),
quantidade de dados nulos (
[1](https://github.com/luanps/airbnb/blob/a15943ce4c7eaba434b775322d7ae1a801222a8a/log.txt#L727-L834),
[2](https://github.com/luanps/airbnb/blob/a15943ce4c7eaba434b775322d7ae1a801222a8a/log.txt#L840-L841),
[3](https://github.com/luanps/airbnb/blob/a15943ce4c7eaba434b775322d7ae1a801222a8a/log.txt#L843-L844)
),
[exemplo](https://github.com/luanps/airbnb/blob/a15943ce4c7eaba434b775322d7ae1a801222a8a/log.txt#L846-L1081)
de itens existentes em cada variável,
bem como a identificação de variáveis que possuem 
[apenas um label](https://github.com/luanps/airbnb/blob/a15943ce4c7eaba434b775322d7ae1a801222a8a/log.txt#L1083-L1084).

Após esse contato inicial com a base de dados, foram utilizadas as seguintes
rotinas de pré-processamento:

* Tratamento textual de variáveis categóricas para 
[transformá-las em numéricas](https://github.com/luanps/airbnb/blob/a15943ce4c7eaba434b775322d7ae1a801222a8a/log.txt#L1089-L1090)  
(ex.: `'$500,00'` para `float(500.00)`)

* Agrupamento de variáveis numéricas para 
[transformá-las em categóricas](https://github.com/luanps/airbnb/blob/a15943ce4c7eaba434b775322d7ae1a801222a8a/log.txt#L1092-L1095)  
(ex.: `'$1.500,00'` para `500.00`)

* Contagem de palavras existentes em variáveis de texto para 
[transformá-las em variáveis numéricas](https://github.com/luanps/airbnb/blob/a15943ce4c7eaba434b775322d7ae1a801222a8a/log.txt#L1097-L1099)  
(ex.: `'lindo APTO em Copacabana'` para `4`).

Para cada variável numérica, foram gerados seus respectivos gráficos de
[histograma e boxplot](https://github.com/luanps/airbnb/tree/master/plots/before_outlier_removal),
possibilitando identificar visualmente casos aonde existem
distribuição assimétrica dos dados e outliers.
A variável `price`, por exemplo, apresenta uma 
[assimetria à direita](https://github.com/luanps/airbnb/blob/master/plots/before_outlier_removal/hist_boxplot_price.png),
ou seja, tem uma concentração de valores baixos, mas sua média é influenciada
em função da cauda longa com valores mais altos.
Em seu gráfico boxplot é possível visualizar a presença de outliers.

A partir da interpretação gráfica, auxiliado pela análise descritiva de cada
variável feita anteriormente, foi aplicado uma 
[remoção de outliers](https://github.com/luanps/airbnb/blob/a15943ce4c7eaba434b775322d7ae1a801222a8a/log.txt#L1103-L1106)
da base de dados, a qual consistiu em normalizar os dados de dada variável 
e excluir suas entradas que estivessem acima de 3 desvios padrões 
(`-3 > z-score > 3`).

A variável dependente `price` foi 
[transformada em log](https://github.com/luanps/airbnb/blob/a15943ce4c7eaba434b775322d7ae1a801222a8a/log.txt#L1108),
facilitando a conversão
do modelo de regressão a ser aplicado.

Os gráficos de histograma e boxplot foram então
[gerados novamente](https://github.com/luanps/airbnb/tree/master/plots/after_outlier_removal),
possibilitando identificar as distribuições atualizadas após o processo
de remoção de outliers, bem como todas as rotinas de exploração de dados, 
as quais foram
[recomputadas](https://github.com/luanps/airbnb/blob/a15943ce4c7eaba434b775322d7ae1a801222a8a/log.txt#L1114-L1489)
para análise.


#### Como foi definida a função de custo utilizada?
Foi empregada a métrica de ajuste o RMSE *(Root Mean Square Error)*, que 
consiste em aferir a diferença entre o valor estimado por dado modelo de 
regressão e o valor real. 
Por elevar o erro ao quadrado, esta é uma métrica sensível à outliers, o que
pode ser um indicadivo para iterar a análise e filtragem dos dados.

Outro fator que favoreceu o uso desta métrica é que,
por se tratar de uma avaliação universal, permite comparar o 
resultado de diferentes modelos empregados.

#### Qual foi o critério utilizado na seleção do modelo final?
Uma vez separado o conjunto de dados em treino (70%) e validação (30%),
o modelo final foi aquele que alcançou o menor erro RMSE no conjunto de 
validação, que neste caso foi utilizando o método  *Gradient Boosting*.

#### Qual foi o critério utilizado para validação do modelo?
Foram empregados no total cinco métodos distintos de regressão, 
sendo três abordagens lineares 
[Ridge](https://github.com/luanps/airbnb/blob/a15943ce4c7eaba434b775322d7ae1a801222a8a/log.txt#L1492-L1497),
[Lasso](https://github.com/luanps/airbnb/blob/a15943ce4c7eaba434b775322d7ae1a801222a8a/log.txt#L1499-L1504) e
[ElasticNet](https://github.com/luanps/airbnb/blob/a15943ce4c7eaba434b775322d7ae1a801222a8a/log.txt#L1506-L1512)
,
a regressão não-linear
[SVR](https://github.com/luanps/airbnb/blob/a15943ce4c7eaba434b775322d7ae1a801222a8a/log.txt#L1514-L1518)
e o modelo
[Gradient Boosting](https://github.com/luanps/airbnb/blob/a15943ce4c7eaba434b775322d7ae1a801222a8a/log.txt#L1520-L1524).

Para todos os casos foram testados diferentes combinações de hiperparâmetros,
além da avaliação cruzada, buscando o melhor ajuste possível para o
conjunto de dados existente.

#### Por que escolheu utilizar este método?
Visto que a variável dependente `price` é contínua, esta tarefa teve a
necessidade de utilização de uma abordagem de regressão. 
Neste sentido, foi decidido utilizar modelos mais simples e de baixa complexidade,
tanto em sua implementação como na otimização de hiperparâmetros, 
possibilitando agregar resultados consistentes em pouco tempo.

#### Quais evidências você possui de que seu modelo é suficientemente bom?
O modelo de regressão escolhido apresentou ser mais robusto frente aos demais
no benchmark desenvolvido neste estudo, sendo suficiente para dada tarefa.
