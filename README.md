# Projeto Lojas Rossmann - Ferramenta de Previsão de Vendas para Lojas Farmacêuticas

![alt text](https://github.com/willianmenegatt/Projeto_Rossmann/blob/main/img.jpg?raw=true)

A Rossmann é uma empresa farmacêutica e possui mais de 1000 lojas espalhadas pela Europa. Todos os dias, o gerente de cada loja contabiliza suas vendas e tem o papel de enviar em um prazo determinado seus resultados. As vendas podem ser impactadas por diversos fatores, como promoções, feriados, sazonalidade e localidade.
Outro papel dos gerentes é tentar prever as vendas de suas lojas nas próximas 6 semanas por questões orçamentárias.

As bases de dados foram retiradas do site kaggle: https://www.kaggle.com/c/rossmann-store-sales

## Problema de Negócio

Todo final de mês existe uma reunião com todos os gerentes das lojas Rossmann, com o objetivo de discutir resultados, dificuldades e metas. Em especial no último mês, o CFO pediu para que todos os gerentes de lojas, fizessem uma predição das próximas 6 semanas de vendas de cada uma de suas lojas. 

Como cientista de dados, após conversar com algumas pessoas, incluindo o CFO, descobriu-se que o mesmo está com dificuldade em definir o Budget para a reforma das lojas Rossmann. Baseado nessa dificuldade o CFO pretende entender quanto de receita as lojas farão nas próximas semanas para conseguir definir esse orçamento.

As dificuldades em estipular o Budget previamente incluem:
- A forma como realizam atualmente a predição apresenta divergências. Por vários meses as lojas erraram muito sua predição.
- O processo de predição de vendas é baseado em experiências passadas, não existe um método científico. 
- Toda previsão é realizada manualmente.
- Existe um prazo para que todas as lojas enviem essa previsão, porém nem todo gerente cumpre o prazo. 

## Objetivo 

Construir um modelo, que fará a previsão de vendas para todas as 1115 lojas nas próximas 6 semanas. De maneira automática, esses dados chegarão em um único lugar e no mesmo instante para o CFO. 

## Estratégia de Solução 


**1**. Coletar os dados e consolidar dataset
- Checar e tratar valores faltantes;
- Estatística descritiva dos dados;

**2**. Feature Engineering
- Mapa mental de hipóteses.
- Lista final de hipóteses.

**3**. Filtragem de variáveis

**4**. Análise Exploratória de Dados
- Validação das hipóteses.
- Análise univariada.
- Análise bivariada.
- Análise multivariada.
    
**5**. Preparação dos dados
- Normalização.
- Redimensionamento.
- Transformações.
    
**6**. Seleção de variáveis
- Boruta como seletor de variáveis.
    
**7**. Modelo de Machine Learning
- Escolher entre modelos: Linear Regression, Linear Regression Regularized - Lasso, Random Forests & XGBoosts.
- Cross-validação  - TimeSeries.

**8**. Ajuste fino de hiperparâmetros
- Random Search.
- Modelo Final.

**9**. Tradução e interpretação do erro
- Business performance.
- Performance do modelo.

**10**. Deploy do modelo via API
- Salvar modelo.
- Criação de arquivo handler (Flask).
- Criação de API.

