# Autor : Rafael Gonçalves

import pandas as pd
import streamlit as st

import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
   page_title="Acidentes de Trânsito App",
   page_icon="🚦",
   layout="centered"
)

# alternativa para add css
styler_width = """
      <style>
        .block-container {
          text-align: -webkit-center;
          max-width: 60rem;
        }
      </style>
"""
st.markdown(styler_width, unsafe_allow_html=True)

# Titulo
st.header('Acidentes de trânsito no estado da Bahia - 2017 - 2021')

# Colunas
col1, col2, col3 = st.columns([3, 1, 1])

# df = pd.read_csv("acidentes_por_ano_ba.csv", on_bad_lines="skip", sep=";")
dg = pd.read_csv("acidentes_por_sexo_por_ano.csv", on_bad_lines="skip", sep=";")

total_acidentes = dg['Total'][3]

dg_totais = dg.loc[3:, '2017' : '2021'].melt(var_name='Ano', value_name='Valor')

dg_anos = dg_totais.Ano  # Anos
dg_vitimas = dg_totais.Valor  # Totais

# dg_anos = dg.loc[:0, '2017' : '2021'].columns  # Anos
# dg_vitimas = dg.loc[3, '2017' : '2021'].values  # Totais

# col1.bar_chart(df_t, x='Ano', y='Valor')

grafico = go.Figure(
            data=[
              go.Bar(
                x=dg_anos,
                y=dg_vitimas,
                marker_color='#A777F1',
                insidetextfont=go.bar.Insidetextfont(color='#f5f9e9', family='Droid Sans', size=14)
              )
            ],
            layout=go.Layout( 
              title=go.layout.Title(text='Dados por Ano - Bahia'),
              xaxis=go.layout.XAxis(title='Ano'),
              yaxis=go.layout.YAxis(title='Óbitos')
            )
)

grafico.update_traces(
  textposition='inside',
  texttemplate='%{y:4.2s}',
)

grafico.update_layout(
  xaxis_rangeslider_visible=False,
  template='plotly_white'
)

st.plotly_chart(grafico)

## Segundo Gráfico
# dg = pd.read_csv("acidentes_por_sexo_por_ano.csv", on_bad_lines="skip", sep=";")

total_masc = dg.loc[0, 'Total']
total_fem = dg.loc[1, 'Total']
total_ign = dg.loc[2, 'Total']

dg_sav = dg.loc[:2, 'Sexo' : '2021'].melt(id_vars='Sexo', var_name='Ano', value_name='Valor')

# grafico2 = go.Figure()
# grafico2.add_trace(go.Bar(
#     y=[ dg_t[dg_t['Sexo'] == 'Masc'][['Sexo']], dg_t[dg_t['Sexo'] == 'Masc'][['Ano']] ],
#     x=dg_t[dg_t['Sexo'] == 'Masc'][['Valor']],
#     name='Masc',
#     orientation='h',
#     marker=dict(
#         color='rgba(246, 78, 139, 0.6)',
#         line=dict(color='rgba(246, 78, 139, 1.0)', width=3)
#     )
# ))
# grafico2.add_trace(go.Bar(
#     y=[ dg_t[dg_t['Sexo'] == 'Fem'][['Sexo']], dg_t[dg_t['Sexo'] == 'Fem'][['Ano']] ],
#     x=dg_t[dg_t['Sexo'] == 'Fem'][['Valor']],
#     name='Fem',
#     orientation='h',
#     marker=dict(
#         color='rgba(58, 71, 80, 0.6)',
#         line=dict(color='rgba(58, 71, 80, 1.0)', width=3)
#     )
# ))

# grafico2.update_layout(
#   # xaxis_rangeslider_visible=False,
#   # template='plotly_white',
#   barmode='stack'
# )

import plotly.express as px

# dx_t = dg.loc[:2, 'Sexo' : '2021'].melt(id_vars='Sexo', var_name='Ano', value_name='Valor')

# Criando o gráfico de barras empilhadas (stacked)
grafico2 = px.bar(dg_sav, y='Ano', x='Valor', color='Sexo', barmode='stack', orientation="h",
             title='Dados por Sexo e Ano',
             labels={'Ano': 'Ano', 'Valor': 'Óbitos por Sexo', 'Sexo': 'Sexo'})

# Exibindo o gráfico
st.plotly_chart(grafico2)

dc = dg.loc[:2, 'Sexo' : '2021']
# Definindo as barras do gráfico
fig = go.Figure()

# Personalizando as cores da barra
cores = { 'Masc': dict(
                    color='rgb(0, 98, 196)', 
                    line=dict(color='rgba(0, 0, 153, 0.5)', 
                    width=0.6 )), 
          'Fem': dict(
                    color='RGB(255, 174, 223)', 
                    line=dict(color='rgba(255, 137, 186, 0.5)', 
                    width=0.6 )), 
          'Ign': dict(
                    color='rgb(75, 40, 64)', 
                    line=dict(color='rgba(78, 78, 78, 0.8)', 
                    width=0.6 ))
        }

# marker=dict(
#           color='rgba(246, 78, 139, 0.6)',
#           line=dict(color='rgba(246, 78, 139, 1.0)', width=1)

# Adicionando as barras para cada sexo
for sexo in dc['Sexo']:
    fig.add_trace(go.Bar(
        y=dc.columns[1:],  # Anos
        x=dc[dc['Sexo'] == sexo].values.tolist()[0][1:],  # Valores por ano para o sexo específico
        name=sexo,
        orientation='h',
        marker=cores[sexo]
        )
    )

# Atualizando layout do gráfico
fig.update_layout(
    title='Dados por Sexo e Ano',
    xaxis=dict(title='Óbitos por Sexo'),
    yaxis=dict(title='Ano'),
    template='plotly_white',
    barmode='stack'
)

# Exibindo o gráfico
st.plotly_chart(fig)