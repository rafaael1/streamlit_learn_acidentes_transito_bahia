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
        .element-container label {
          display: inline-flex;
        }
      </style>
"""
st.markdown(styler_width, unsafe_allow_html=True)

# Titulo
st.header('Acidentes de trânsito no estado da Bahia - 2017 - 2021')

# df = pd.read_csv("acidentes_por_ano_ba.csv", on_bad_lines="skip", sep=";")
dg = pd.read_csv("acidentes_por_sexo_por_ano.csv", on_bad_lines="skip", sep=";")

total_acidentes = dg['Total'][3]

dg_totais = dg.loc[3:, '2017' : '2021'].melt(var_name='Ano', value_name='Valor')

dg_anos = dg_totais.Ano  # Anos
dg_vitimas = dg_totais.Valor  # Totais

# dg_anos = dg.loc[:0, '2017' : '2021'].columns  # Anos
# dg_vitimas = dg.loc[3, '2017' : '2021'].values  # Totais


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
              title=go.layout.Title(text='Total de Óbitos de acidentes por Ano - Bahia'),
              xaxis=go.layout.XAxis(title='Anos'),
              yaxis=go.layout.YAxis(title='Total de Óbitos')
            )
)

grafico.update_traces(
  textposition='inside',
  texttemplate='%{y:4.2s}',
)

grafico.update_layout(
  title_x=0.3,
  xaxis_rangeslider_visible=False,
  template='plotly_white'
)

st.plotly_chart(grafico)

## Metricas

# Colunas
# col1, col2, col3 = st.columns([3, 1, 1])
col1, col2, col3, col4 = st.columns(4)

total_masc = dg.loc[0, 'Total']
total_fem = dg.loc[1, 'Total']
total_ign = dg.loc[2, 'Total']

with col1:
    st.metric("Total Óbitos ⚰️", total_acidentes)

with col2:
    st.metric("Total Masc 👨", total_masc)

with col3:
    st.metric("Total Fem 👩", total_fem)

with col4:
    st.metric("Total Ign 🧑", total_ign)


## Segundo Gráfico
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

# Criando o gráfico de barras empilhadas (stacked)
grafico2 = px.line(x=dg_totais.Ano, y=dg_totais.Valor, ).update_traces(showlegend=True, name="Total").add_traces(
    
px.bar(dg_sav, x='Ano', y='Valor', color='Sexo', 
        barmode='stack', 
        orientation="v", 
        labels={'Ano': 'Ano', 'Valor': 'Óbitos por Sexo', 'Sexo': 'Sexo'}
      ).data
)

grafico2.update_layout(
    title='Dados por Sexo e Ano',
    xaxis_title='Anos',
    yaxis_title='Total de Óbitos por Sexo'
)

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
    xaxis=dict(title='Total de Óbitos por Sexo'),
    yaxis=dict(title='Anos'),
    template='plotly_white',
    barmode='stack'
)

# Exibindo o gráfico
st.plotly_chart(fig)

## Quarto gráfico
# Leitura do arquivo
dcor = pd.read_csv("acidentes_por_ano_segundo_cor_raca.csv", on_bad_lines="skip", sep=";")

dcor.rename(columns={'Cor/raça' : 'Cor_raca'}, inplace=True)

# Transforma DataFrame
dcor_t = dcor.loc[:5,  : '2021'].melt(id_vars='Cor_raca', var_name='Ano', value_name='Valor')

qq = px.area(dcor_t, x='Ano', y='Valor', color='Cor_raca', line_group='Cor_raca', category_orders=dict(Cor_raca=['Indígena', 'Amarela', 'Ignorado', 'Preta', 'Branca', 'Parda'] ) )

qq.update_yaxes(tick0=100, dtick=500)
qq.update_yaxes(range=[None, 2500], maxallowed=3200)

# Exibindo o gráfico
st.plotly_chart(qq)