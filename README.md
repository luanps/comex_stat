# Análise de churn

Este repositório tem como finalidade realizar uma análise em
atributos relacionados ao *Churn* de clientes.  

## Instalação

*use python >= 3.6*
```
pip3 install -r requirements.txt
```

## Como executar

```
pip3 main.py
```

## Saída



### O que é churn
...
#### Exploração da base de dados
Neste estudo foi utilizado a base de dados |[Database.csv](data/Database.csv).
Esta base consiste de 7043 amostras (clientes) e 23 atributos distintos,
sendo estes:

```
customerID, gender , SeniorCitizen, Partner, Dependents, tenure, PhoneService,
MultipleLines, code, InternetService, OnlineSecurity, OnlineBackup,
DeviceProtection, TechSupport, StreamingTV, StreamingMovies, Contract, Hash,
PaperlessBilling, PaymentMethod, MonthlyCharges, TotalCharges, Churn
```

Foram identificados alguns atributos com dados faltantes, (campo vazio ou epaço
em branco ' '), que podem vir a ser removidos do estudo.

|atributo        |qtde de dados faltantes:|
| ---            | ---|
|customerID      |3459|
|OnlineSecurity  |34|
|TotalCharges    |11|

Por fim, uma amostra de quais informações são contidas em cada atributo,
sendo possível identificar que alguns campos possuem grafia diferente, porém
mesmo significado, podendo ser agrupados (ex.: [no,No,0] = 0).

Além disso, observando as colunas *Hash* e *code* pode se inferir que são uma
decomposição da coluna *customerID*, e tas três existem unicamente  para
identificar o usuário, não são elementos que implicam no resultado de Churn.

|Atributo | Amostra de dados |
| --- | --- |
|customerID |[nan '5575-GNVDE' '7795-CFOCW' '9237-HQITU' '6388-TABGU' '0280-XJGEX'|
| '5129-JLPIS' '3655-SNQYZ' '8191-XWSZG' '9959-WOFKT']|
|gender |['Female' 'Male']|
|SeniorCitizen |[0 1]|
|Partner |['Yes' 'No' 'no' 'yes' '0' '1']|
|Dependents |['No' 'Yes' 'no' 'yes' '0' '1']|
|tenure |[ 1 34  2 45  8 22 10 28 62 13]|
|PhoneService |['No' 'Yes' 'yes' 'no' '1' '0']|
|MultipleLines |['No phone service' 'No' 'Yes' 'no' 'yes' 'no phone service' '0' '1']|
|code |[7590 5575 3668 7795 9237 9305 1452 6713 7892 6388]|
|InternetService |['DSL' 'Fiber optic' 'No' 'no']|
|OnlineSecurity |['No' 'Yes' 'No internet service' 'yes' 'no internet service' 'no' nan '0'|
| '1']|
|OnlineBackup |['Yes' 'No' 'No internet service' 'no' 'no internet service' 'yes' '0' '1']|
|DeviceProtection |['No' 'Yes' 'No internet service' 'no' 'no internet service' 'yes' '0' '1']|
|TechSupport |['No' 'Yes' 'No internet service' 'no' 'no internet service' 'yes' '0' '1']|
|StreamingTV |['No' 'Yes' 'No internet service' 'no' 'no internet service' 'yes' '0' '1']|
|StreamingMovies |['No' 'Yes' 'No internet service' 'no' 'no internet service' 'yes' '1' '0']|
|Contract |['Month-to-month' 'One year' 'Two year']|
|Hash |['75VEG' 'GNVDE' 'QPYBK' 'CFOCW' 'HQITU' 'CDSKC' 'KIOVK' 'OKOMC' 'POOKP'|
| 'TABGU']|
|PaperlessBilling |['Yes' 'No' 'yes' 'no' '1' '0']|
|PaymentMethod |['Electronic check' 'Mailed check' 'Bank transfer (automatic)'|
| 'Credit card (automatic)']|
|MonthlyCharges |[ 29.85  56.95  53.85  42.3   70.7   99.65  89.1   29.75 104.8   56.15]|
|TotalCharges |['29.85' '1889.5' '108.15' '1840.75' '151.65' '820.5' '1949.4' '301.9'|
| '3046.05' '3487.95']|
|Churn |['No' 'Yes' 'yes' 'no' '0' '1']|


#### Pré-processamento


![img description](link)
