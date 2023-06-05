![https://user-images.githubusercontent.com/68928802/137392417-f320ce54-6198-475a-9e15-ec0f3d4b162d.jpg](https://user-images.githubusercontent.com/68928802/137392417-f320ce54-6198-475a-9e15-ec0f3d4b162d.jpg)

# Rossmann Store Sales Prediction

### Disclaimer 1

Este é um contexto fictício criado para portifólio. Todos os personagens foram criados assim como o problema de negócio.

### Disclaimer 2

Os dados foram publicados em uma [competição do kaggle](https://www.kaggle.com/c/rossmann-store-sales/overview).

### Disclaimer 3

O projeto é parte da [Comunidade DS](https://sejaumdatascientist.com/inscricao-lives-comunidade-ds).

<<<<<<< HEAD
---
=======
But, after the kick-off meeting with the CEO where more questions about the problem were made we agreed that a full year prediction do not give us time to react to bad news. And also, the results will be reported quarterly, what makes a full year prediction useless. Therefore, was decided that a 6 weeks prediction will fit better into this scenario. It will be possible to notice significant variances and act to minimize the loss if necessary.
>>>>>>> d4485b9 (final commit - telegram bot online)

## Contexto

<<<<<<< HEAD
A Rossmann é uma das maiores redes de drogarias na Europa com mais de 50k+ funcionários e 4k+ lojas.
Contudo, o crescimento mostrado durante a reunião anual onde os gerentes regionais apresentam ao CEO o plano de vendas para o próximo ano não é compatível com a grandeza da Rossmann. Então, para estabelecer uma nova métrica para medir a performance das vendas, o CEO pediu aos gerentes uma previsão de vendas para o próximo trimestre. Atualmente, o crescimento projetado pelos times de vendas é apenas uma média semanal das vendas passadas.
=======
So, from now on a challenge is settled, create this prediction to be used as a guideline to the annual sales plan. It will not only avoid loss but also increase the gain with early decisions.
>>>>>>> d4485b9 (final commit - telegram bot online)

Mas, após a reunião inicial com o CEO onde mais questões sobre o problema foram levantadas, houve um concenso de que a previsão de um trimestre inteiro não dá tempo de reação perante más notícias já que os resultados são reportados a cada trimestre. Portanto, foi decidido que uma previsão de 6 semanas se encaixará melhor neste cenário. Assim, será possível notar variações significativas e agir para minimizar perdas caso necessário.

## Solução

Então, a partir de agora o desafio foi lançado, criar um modelo de previsão para ser usado como guia para o plano de vendas anual. Este modelo não só evitará perdas como também aumentará o ganho com tomadas de decisões mais cedo.

### Planejamento

### Entrada

Três datasets (conjunto de dados):

- train.csv -> dados históricos de vendas
- store.csv -> informação complementar das lojas
- test.csv -> informação sobre os próximos dias das lojas

### Saída

Informação com formatação simples e direta contendo a previsão para as próximas 6 semanas.
Essa saída será providenciada através de um [bot no telegram](https://github.com/daSpinelli/Rossmann-Prediction-API) que consome uma [API](https://github.com/daSpinelli/Rossmann-Prediction-API) desenvolvida em Python e hospedada em um aplicativo na núvem.

### Tarefas

1. Descrição dos dados:
- Algumas informações básicas sobre o conjunto de dados como dimenões, tipos de dados e valores nulos
- Detecção de outliers
- Estatística descritiva
- Tratamento de valores nulos:
    
    ![https://user-images.githubusercontent.com/68928802/137227124-f107afed-948c-4700-918c-49482940499e.png](https://user-images.githubusercontent.com/68928802/137227124-f107afed-948c-4700-918c-49482940499e.png)
    
1. Feature engineering:
- Mapa mental de hipóteses
- Criação de features
1. Análise exploratória de dados:
- Univariada para checar a distribuição das features
- Bivariada, este passo permite checar o comportamento das features quando em função das vendas
    - Aqui também é possível validar as hipóteses criadas no mapa mental
    - Algumas hipóteses à destacar:

Lojas com competidores próximos vendem menos ->

**FALSO**

![https://user-images.githubusercontent.com/68928802/137230723-1d8568a2-df46-43af-a1e8-50b81dcb5a3d.png](https://user-images.githubusercontent.com/68928802/137230723-1d8568a2-df46-43af-a1e8-50b81dcb5a3d.png)

Lojas devem vender mais no segundo semestre do ano ->

**VERDADEIRO**

![https://user-images.githubusercontent.com/68928802/137230048-df39c14e-a605-4591-a13d-2caa03fddf8d.png](https://user-images.githubusercontent.com/68928802/137230048-df39c14e-a605-4591-a13d-2caa03fddf8d.png)

Lojas devem vender menos após o décimo dia de cada mês ->

**VERDADEIRO**

![https://user-images.githubusercontent.com/68928802/137230050-33aeb018-e2b9-4c96-861c-a2b3e4ce4163.png](https://user-images.githubusercontent.com/68928802/137230050-33aeb018-e2b9-4c96-861c-a2b3e4ce4163.png)

1. Preparação dos dados
- Rescala dos dados com o Robust e MinMax scaler, utilizando o pickle para evitar vazamento de dados na produção
- Label encoding
- Transformação de natureza das features de tempo
1. Seleção de feature
- Separação dos dados em blocos de 6 semanas para possibilitar a validação cruzada
- seleção de features com Botura
1. Modelos de machine learning
- Modelos testados:
    - Modele de média (baseline, praticado atualmente)
    - Regressão linear
    - Regressão linear regularizada (Lasso)
    - Random forest regressor
    - XGBoost regressor
- Métricas usadas para medir a perfomance dos modelos:
    - MAE
    - MAPE
    - RMSE

Embora a XGBoost não é o modelo que melhor performou, foi o escolhido por conta de sua flexibilidade quando se trata de hiperparametrização.

![https://user-images.githubusercontent.com/68928802/137232262-7f3066de-06a0-4996-98a3-656a341f7f33.png](https://user-images.githubusercontent.com/68928802/137232262-7f3066de-06a0-4996-98a3-656a341f7f33.png)

1. Fine Tunning
- Foi utilizado Random Search.

Resultado após a hiperparametrização

![https://user-images.githubusercontent.com/68928802/137233626-13a8b0b4-9207-4aa0-98f2-82e5ae1b32ee.png](https://user-images.githubusercontent.com/68928802/137233626-13a8b0b4-9207-4aa0-98f2-82e5ae1b32ee.png)

1. Tradução do erro
- Top 5 previsões

![https://user-images.githubusercontent.com/68928802/137318676-be260f4f-161e-4a32-85d7-0ebd68354295.png](https://user-images.githubusercontent.com/68928802/137318676-be260f4f-161e-4a32-85d7-0ebd68354295.png)

- Previsões de vendas x vendas ao longo das 6 semanas e índice de erro ao longo das 6 semanas onde eixo y = 1 é 0% de erro.

![https://user-images.githubusercontent.com/68928802/137318682-6d58e530-b50b-4049-849e-1fb8b0ec2f28.png](https://user-images.githubusercontent.com/68928802/137318682-6d58e530-b50b-4049-849e-1fb8b0ec2f28.png)

- Dispersão do erro absoluto

![https://user-images.githubusercontent.com/68928802/137318685-3c180e88-4b94-4798-9e96-e3762358f5bb.png](https://user-images.githubusercontent.com/68928802/137318685-3c180e88-4b94-4798-9e96-e3762358f5bb.png)

1. Bot no Telegram
- Para acessá-lo, ~~basta clicar abaixo~~ ***(Bot deactivated until the next cycle)***

[<img alt="Telegram" src="https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white"/>](https://t.me/das_rossmann_prediction_bot)

- Modo de usar:
    - Escolha um dos comandos abaixo e envie-o ao bot

![https://user-images.githubusercontent.com/68928802/137385998-b978c56b-4776-4599-993b-888aa8109a3d.png](https://user-images.githubusercontent.com/68928802/137385998-b978c56b-4776-4599-993b-888aa8109a3d.png)

## Próximos passos

- Algorítmo
    - No próximo ciclo novas features como "feriados" serão testadas.
    - Assim como a hiperparametrização de outros modelos, Random Forest Regressor é uma opção.
- Negócio
    - O CEO e os gerentes de vendas acompanharão de perto os números e agir de acordo com as variações dos números reais de vendas.

## Lições aprendidas

A principal lição aprendida com este projeto é que é muito importante planejar a solução passo a passo. Respeitando a ordem em que as coisas acontecem. Respirar fundo e entender o problema antes de iniciar a codificar é a chave.

Outra lição é que o projeto é feito em ciclos, a solução perfeita não será criada no primeiro ciclo.
Tecnicamente, eu aprendi a analisar e preparar os dados para a modelagem. Para fazer isso, utilizei bibliotecas como Pandas, Numpy, Matplotlib e Seaborn.

Modelar também precisa de atenção, podem ocorrer sobreajuste ou sobajuste do modelo se os erros não forem interpretados cuidadosamente.
Testar diferentes modelos permite compará-los para optar pelo mais adequado no momento. E já deixar uma ideia do que pode ser feito no próximo ciclo.
E por último mas não menos importante, publicar o modelo com aplicativos flask e o bot no telegram foi um modo satisfatório de terminar este bom projeto. Pois é uma forma simples e familiar ao usuário final de acessar a solução.

Bom, obrigado por ler este projeto.
Qualquer dúvida ou sugestão, só me contatar:

[<img alt="Denny Profile" src="https://img.shields.io/badge/-LinkedIn-blue?style=for-the-badge&logo=linkedin"/>](https://linkedin.com/in/dennydaspinelli)
