"""
Acidentes de Trânsito Dashboard

@author: Rafael Gonçalves
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Configurações da página
st.set_page_config(page_title="Acidentes de Trânsito App", page_icon="🚦", layout="centered")

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
st.header("Acidentes de trânsito no estado da Bahia - 2017 - 2021")

# Leitura dos arquivos
df_sex = pd.read_csv("acidentes_por_sexo_por_ano.csv", on_bad_lines="skip", sep=";")
df_cor = pd.read_csv("acidentes_por_ano_segundo_cor_raca.csv", on_bad_lines="skip", sep=";")
df_eta = pd.read_csv("acidentes_por_faixa_etaria_ops_por_ano.csv", on_bad_lines="skip", sep=";")

# Tratamento dos dados
df_cor.rename(columns={"Cor/raça": "Cor_raca"}, inplace=True)

# Agrupamento das faixas etárias menores de 15 anos
wd = df_eta.loc[
    (df_eta["Faixa Etária OPS"] == ("Menor 1 ano"))
    | (df_eta["Faixa Etária OPS"] == ("1 a 4 anos"))
    | (df_eta["Faixa Etária OPS"] == ("5 a 14 anos")),
    "2017":"2021",
].sum(axis=0)

# Incluindo a faixa etária com 'menos de 15 anos'
df_eta = pd.concat([df_eta, wd.to_frame().T], axis=0, ignore_index=True)
df_eta.loc[12, "Faixa Etária OPS"] = "Menos de 15 anos"
df_eta.loc[12, "Total"] = wd.sum()

# Removendo as linhas das faixas etárias menores de 15
df_eta = df_eta.drop([7, 8, 10]).reset_index(drop=True)
# Ordenando o DataFrame pela Faixa Etária OPS
df_eta.sort_values(by="Faixa Etária OPS", ascending=True, ignore_index=True, inplace=True)

# Transforma DataFrame
dsex_t = df_sex.iloc[:-1, :-1].melt(id_vars="Sexo", var_name="Anos", value_name="Valor")
dcor_t = df_cor.iloc[:-1, :-1].melt(id_vars="Cor_raca", var_name="Anos", value_name="Valor")
dfx = df_eta.iloc[:-1, :-1].melt(id_vars="Faixa Etária OPS", var_name="Anos", value_name="Valor")

# Definindo o índice como 'Cor/raça' e 'Sexo'
df_sex.set_index("Sexo", inplace=True)
df_cor.set_index("Cor_raca", inplace=True)

# Transpondo os DataFrames
df_sexT = df_sex.T
df_corT = df_cor.T

# total de vitimas no periodo 2017 - 2021
total_acidentes = df_corT.iloc[-1, -1]

# Dataframe Totais por Ano
df_totais_ano = df_corT.iloc[:-1, -1]

df_anos = df_totais_ano.index  # Anos
df_vitimas = df_totais_ano.values  # Totais

dc = df_sex.loc["Masc":"Ign", "2017":"2021"]


# Primeiro gráfico
def first_graph():
    """
    Gráfico - Total de mortalidade por acidentes de trânsito no estado da Bahia
    """
    grafico = go.Figure(
        data=[
            go.Bar(
                x=df_anos,
                y=df_vitimas,
                marker_color="#A777F1",
                insidetextfont=go.bar.Insidetextfont(color="#f5f9e9", family="Droid Sans", size=14),
            )
        ],
        layout=go.Layout(
            title=go.layout.Title(text="Óbitos por acidentes de transporte por Ano - Bahia"),
            xaxis=go.layout.XAxis(title="Anos"),
            yaxis=go.layout.YAxis(title="Total de Óbitos"),
        ),
    )

    grafico.update_traces(
        textposition="inside",
        texttemplate="%{y:4f}",
    )

    grafico.update_layout(title_x=0.3, xaxis_rangeslider_visible=False, template="plotly_white")

    return grafico


## Metricas
def metrics():
    """
    Indicadores dos totais de óbitos em acidentes de trânsito por sexo.
    """
    # Colunas
    col1, col2, col3, col4 = st.columns(4)

    # segmentado por sexo
    total_masc = df_sex.loc["Masc", "Total"]
    total_fem = df_sex.loc["Fem", "Total"]
    total_ign = df_sex.loc["Ign", "Total"]

    with col1:
        st.metric("Total de Óbitos ⚰️", total_acidentes)  # type: ignore

    with col2:
        st.metric("Total Masculino 👨", total_masc)  # type: ignore

    with col3:
        st.metric("Total Feminino 👩", total_fem)  # type: ignore

    with col4:
        st.metric("Total Ignorado 🧑", total_ign)  # type: ignore


# Segundo gráfico
def second_graph():
    """
    Gráfico - Mortalidade por acidentes segundo o sexo.
    """
    # Criando o gráfico de barras empilhadas (stacked)
    grafico2 = (
        px.line(x=df_anos, y=df_vitimas)
        .update_traces(showlegend=True, line_color="#9a4c95", name="Total")
        .add_traces(
            # Adicionando as barras para cada sexo
            px.bar(
                dsex_t,
                x="Anos",
                y="Valor",
                color="Sexo",
                barmode="stack",
                orientation="v",
                labels={"Anos": "Ano", "Valor": "Óbitos por Sexo", "Sexo": "Sexo"},
            ).data
        )
    )

    # Atualizando layout do gráfico
    grafico2.update_layout(
        title="Dados por Gênero e Ano",
        xaxis_title="Anos",
        yaxis_title="Total de Óbitos por Sexo",
    )

    return grafico2


# Terceiro gráfico
def third_graph():
    """
    Gráfico - Óbitos por acidentes de transporte por cor/raça.
    """
    # Personalizando as cores da barra
    cores = {
        "Parda": dict(color="#4C78A8", line=dict(color="rgba(0, 0, 153, 0.5)", width=0.3)),
        "Branca": dict(color="#F58518", line=dict(color="rgba(255, 137, 186, 0.5)", width=0.3)),
        "Preta": dict(color="#E45756", line=dict(color="rgba(78, 78, 78, 0.8)", width=0.3)),
        "Ignorado": dict(color="#72B7B2", line=dict(color="rgba(78, 78, 78, 0.8)", width=0.3)),
        "Amarela": dict(color="#54A24B", line=dict(color="rgba(78, 78, 78, 0.8)", width=0.3)),
        "Indígena": dict(color="#B279A2", line=dict(color="rgba(78, 78, 78, 0.8)", width=0.3)),
    }

    # Definindo as barras do gráfico
    fig = go.Figure()

    # Adicionando as barras para cada cor/raça
    for cor in df_cor.index[:-1]:
        fig.add_trace(
            go.Bar(
                y=dc.columns,  # Anos
                x=df_cor.loc[cor].values[:-1],  # Valores por ano para o cor/raça específico
                name=cor,
                orientation="h",
                marker=cores[cor],
            )
        )

    # Atualizando layout do gráfico
    fig.update_layout(
        title="Dados por Ano e Cor/Raça",
        xaxis=dict(title="Total de Óbitos por cor/raça", range=[1400, None]),
        yaxis=dict(title="Anos"),
        legend_title="Cor/Raça",
        template="plotly_white",
        barmode="stack",
    )

    return fig


## Quarto gráfico
def quarter_graph():
    """
    Gráfico - Óbitos por acidentes de transporte por Faixa Etária OPS
    """
    # Definindo o gráfico
    qq = px.area(
        dfx,
        x="Anos",
        y="Valor",
        color="Faixa Etária OPS",
        color_discrete_sequence=px.colors.qualitative.Prism,
        groupnorm="percent",
        custom_data=["Faixa Etária OPS", "Valor"],
    )

    ## Dados
    qq.update_traces(
        hovertemplate="Faixa Etária OPS: <b>%{customdata[0]}</b> <br><br>Ano: %{x} <br>Proporção: %{y:4.2f}% <br>Valor Absoluto: %{customdata[1]}<extra></extra>"
    )

    # Atualizando eixos do gráfico
    qq.update_yaxes(title="Total de Óbitos")
    qq.update_xaxes(showgrid=True)

    qq.update_layout(
        title={"text": "Total de Óbitos por Faixa Etária OPS*", "x": 0.3},
        legend_title_text="Faixa Etária OPS",
    )
    qq.update_layout(yaxis_ticksuffix="%")

    qq.add_annotation(
        text=("* Faixa etária do falecido, no padrão da Organização Pan-Americana de Saúde (OPS)"),
        showarrow=False,
        x=0,
        y=-0.20,
        xref="paper",
        yref="paper",
        xanchor="left",
        yanchor="bottom",
        xshift=-1,
        yshift=-5,
        font=dict(size=10, color="grey"),
        align="left",
    )

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

    st.markdown(
        "**Fonte:** MS/SVS/CGIAE - Sistema de Informações sobre Mortalidade - SIM / DATASUS"
    )


if __name__ == "__main__":
    main()
