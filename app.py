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
with open('./custom.css') as f:
    css = f.read()

st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

# Titulo
st.header('Acidentes de trânsito no estado da Bahia - 2017 - 2021')

# Colunas
col1, col2, col3 = st.columns([3, 1, 1])

df = pd.read_csv("acidentes_por_ano_ba.csv", on_bad_lines="skip", sep=";")

total_acidentes = df["Total"][0]

df_anos = df.loc[:0, '2017' : '2021'].columns
df_vitimas = df.loc[:0, '2017' : '2021'].values

df_t = df.loc[:0, '2017' : '2021'].melt(var_name='Ano', value_name='Valor')

# col1.bar_chart(df_t, x='Ano', y='Valor')

# fig = px.bar(df_t, x='Ano', y='Valor', text='Valor',
#              title='Dados por Ano - Bahia',
#              labels={'Ano': 'Ano', 'Valor': 'Valor'},
#              color='Ano', barmode='group')
# # Atualizando o layout para melhorar a apresentação do gráfico
# fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
# fig.update_layout(uniformtext_minsize=4, title_x=0.7, bargroupgap=0.1, funnelgap=0.1)

# st.plotly_chart(fig)

grafico = go.Figure(
            data=[
              go.Bar(
                x=df_t.Ano,
                y=df_t.Valor,
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

