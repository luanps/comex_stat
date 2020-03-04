# Análise de preço de estadia no AirBnB-Rio de Janeiro

Este repositório tem como finalidade estimar o valor de estadia 
no Rio de Janeiro analisando dados do [AirBnB](http://insideairbnb.com/get-the-data.html)


## Instalação

*use python >= 3.6*
```
pip3 install -r requirements.txt
```

## Como executar

```
python3 main.py
```

#### Como foi a definição da sua estratégia de modelagem?

Inicialmente foi realizado uma análise exploratória no conjunto de dados, 
verificando as propriedades de cada variável existente, tais como seu o
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
A variável *price*, por exemplo, apresenta uma 
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
possibilitando identificar as distribuições atualizadas após a o processo
de remoção de outliers, bem como todas as rotinas de exploração de dados, 
as quais foram
[re-computadas](https://github.com/luanps/airbnb/blob/a15943ce4c7eaba434b775322d7ae1a801222a8a/log.txt#L1114-L1489)
para análise.


#### Como foi definida a função de custo utilizada?
#### Qual foi o critério utilizado na seleção do modelo final?
#### Qual foi o critério utilizado para validação do modelo?
#### Por que escolheu utilizar este método?
#### Quais evidências você possui de que seu modelo é suficientemente bom?
