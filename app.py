# Autor : Rafael Gonçalves

import pandas as pd
import streamlit as st

import plotly.graph_objects as go
from plotly.subplots import make_subplots

import plotly.express as px

# Configurações da página
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

# Titulo Principal
st.header('Acidentes de trânsito no estado da Bahia - 2017 - 2021')

# Leitura dos arquivos
# df = pd.read_csv("acidentes_por_ano_ba.csv", on_bad_lines="skip", sep=";")
dg = pd.read_csv("acidentes_por_sexo_por_ano.csv", on_bad_lines="skip", sep=";")
dcor = pd.read_csv("acidentes_por_ano_segundo_cor_raca.csv", on_bad_lines="skip", sep=";")

# Tratamento dos dados
dcor.rename(columns={'Cor/raça' : 'Cor_raca'}, inplace=True)

# Transforma DataFrame
dg_sav = dg.loc[:2, 'Sexo' : '2021'].melt(id_vars='Sexo', var_name='Ano', value_name='Valor')
dcor_t = dcor.loc[:5,  : '2021'].melt(id_vars='Cor_raca', var_name='Ano', value_name='Valor')

# total de vitimas no periodo 2017 - 2021
total_acidentes = dg['Total'][3]

dg_totais = dg.loc[3:, '2017' : '2021'].melt(var_name='Ano', value_name='Valor')

dg_anos = dg_totais.Ano  # Anos
dg_vitimas = dg_totais.Valor  # Totais por Ano

# dg_anos = dg.loc[:0, '2017' : '2021'].columns  # Anos
# dg_vitimas = dg.loc[3, '2017' : '2021'].values  # Totais

dc = dg.loc[:2, 'Sexo' : '2021']

# Primeiro gráfico
def first_graph():
    
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
      title=go.layout.Title(text='Óbitos por acidentes de transporte por Ano - Bahia'),
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
  
  return grafico

## Metricas
def metrics():
  # Colunas
  col1, col2, col3, col4 = st.columns(4)

  # segmentado por sexo
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

# Segundo gráfico
def second_graph() :

  # Criando o gráfico de barras empilhadas (stacked)
  grafico2 = px.line(x=dg_totais.Ano, y=dg_totais.Valor).update_traces(showlegend=True, line_color='#9a4c95', name="Total").add_traces(
  
  # Adicionando as barras para cada sexo
  px.bar(dg_sav, x='Ano', y='Valor', color='Sexo', 
      barmode='stack', 
      orientation="v", 
      labels={'Ano': 'Ano', 'Valor': 'Óbitos por Sexo', 'Sexo': 'Sexo'}
      ).data
  )

  # Atualizando layout do gráfico
  grafico2.update_layout(
    title='Dados por Gênero e Ano',
    xaxis_title='Anos',
    yaxis_title='Total de Óbitos por Sexo',
  )

  return grafico2

# Terceiro gráfico
def third_graph():
  #  Óbitos por acidentes de transporte por gênero
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

  # Definindo as barras do gráfico
  fig = go.Figure()

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
      title='Dados por Gênero e Ano',
      xaxis=dict(title='Total de Óbitos por gênero'),
      yaxis=dict(title='Anos'),
      template='plotly_white',
      barmode='stack'
  )

  return fig

## Quarto gráfico
def quarter_graph():
  # Definindo o gráfico
  qq = px.area(dcor_t, x='Ano', y='Valor', color='Cor_raca', color_discrete_sequence=px.colors.qualitative.Prism, groupnorm='percent', custom_data=['Cor_raca', 'Valor'] )

  ## Dados
  print(qq.data[0].hovertemplate)
  print(qq.data[0].customdata)
  qq.update_traces(hovertemplate='Cor/Raça: <b>%{customdata[0]}</b> <br><br>Ano: %{x} <br>Proporção: %{y:4.2f}% <br>Valor Absoluto: %{customdata[1]:4.s}<extra></extra>')
  

  # Atualizando eixos do gráfico
  qq.update_yaxes(title='Total de Óbitos')
  qq.update_xaxes(showgrid=True)
  qq.update_yaxes(range=[50, 100])

  qq.update_layout(title={
        'text' : 'Total de Óbitos por Cor/Raça',
        'x' : 0.3 
      }, legend_title_text='Cor/Raça')
  qq.update_layout(yaxis_ticksuffix = "%")

  return qq


def main():
  
  # Exibindo o gráfico 1
  st.plotly_chart(first_graph())

  # Métricas dos acidentes
  metrics()

  # Exibindo o gráfico 2
  st.plotly_chart(second_graph())

  # Exibindo o gráfico 3
  st.plotly_chart(third_graph())
  
  # Exibindo o gráfico 4
  st.plotly_chart(quarter_graph())

  st.markdown('Fonte: MS/SVS/CGIAE - Sistema de Informações sobre Mortalidade - SIM')
if __name__ == "__main__":
    main()