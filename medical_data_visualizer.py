import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# le o arquivo
df = pd.read_csv('medical_examination.csv')

# calculo bmi é pegar o peso dividir pela altura e elevar ao quadrado
bmi = df['weight'] / ((df['height'] / 100) ** 2)
#calculo para alguem overweight é se o calculo de bmi for maior qu 25 o valor vira 1, se nao vira 0
df['overweight'] = np.where(bmi > 25, 1, 0)
# filtro do cholesterol onde se o cholesterol for maior que 1 o valor vira 1 , se nao vira 0
df['cholesterol'] = np.where(df['cholesterol'] > 1, 1, 0)
#mesma coisa pra glucose 
df['gluc'] = np.where(df['gluc'] > 1, 1, 0)

# funcao pro grafico
def draw_cat_plot():
    #funcao que derrete o dataframe? value_vars são as colunas que vao ser derretidas e transformadas em linhas
    df_cat = pd.melt(df, id_vars=['cardio'], value_vars=['active', 'smoke', 'cholesterol', 'gluc', 'overweight', 'alco'])

    #agrupa os dados para fazer a contagem de cada variavel, o name total no final é o nome da nova coluna que vai ser criada com a contagem
    df_cat = df_cat.groupby(['cardio', 'variable', 'value']).size().reset_index(name='total')

    # cria o grafico com a biblioteca seaborn, que e usada pra ajudar na visualizacao de dados, e ai define o tipo do grafico como bar por exemplo
    fig = sns.catplot(x='variable', y='total', hue='value', col='cardio', data=df_cat, kind='bar').fig

    # salva a imagem como png
    fig.savefig('catplot.png')
    return fig

# 10
def draw_heat_map():
    # o ap_lo tem que ser menor ou igual ao ap_hi,
    #a primeira linha do height fala que ele precisa ser maior ou igual que o o quartile de 2.5%, mas tambem menor ou igual que o quartile de 97.5%
    # a mesma logica pro weight
    df_heat = df[
        (df['ap_lo'] <= df['ap_hi']) &
        (df['height'] >= df['height'].quantile(0.025)) &
        (df['height'] <= df['height'].quantile(0.975)) &
        (df['weight'] >= df['weight'].quantile(0.025)) &
        (df['weight'] <= df['weight'].quantile(0.975))
    ]

    corr = df_heat.corr()

    #o numpy.triu e uma funcao que retorna a parte superior de um triangulo de uma matriz, esse triangulo é usado pra fazer a mascara do grafico
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # cria a figura com esse tamanho
    fig, ax = plt.subplots(figsize=(12, 8))

    # 15
    sns.heatmap(
        #o fmt é o formato dos numeros que vao aparecer no grafico que neses caso é uma casa decimal, 
        # o center define a escala das cores em 0, o vmax e vmin sao os valores maximos e minimos da escala de cores,
        #  o square deixa as celula quadradas e o linewidths é o tamaho das linhas que fica entre as celulas. 
        # o cbar_kws ajusta o tamanho da barra de cores
        corr, mask=mask, annot=True, fmt='.1f', center=0,
        vmax=0.3, vmin=-0.1, square=True, linewidths=0.5, cbar_kws={"shrink": 0.5},
        ax=ax
    )


    # salva a imgagem como png
    fig.savefig('heatmap.png')
    return fig