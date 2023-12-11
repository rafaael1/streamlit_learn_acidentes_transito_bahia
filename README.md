[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Plotly](https://img.shields.io/badge/plotly-5.18.0-green--ligth)](https://pypi.org/project/plotly/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.29.0-%23ff4b4c)](https://pypi.org/project/streamlit/)

## 📊 Dashboard com Python e Streamlit

## 📋 Sobre

Dashboard criado com Python e Streamlit para visualização de dados de um dataset de acidentes de trânsito no estado da Bahia entre 2017 e 2021.

> Streamlit é uma biblioteca Python de código aberto que facilita a criação e o compartilhamento de belos aplicativos da web personalizados para aprendizado de máquina e ciência de dados. Em apenas alguns minutos você pode criar e implantar aplicativos de dados poderosos. (@Ronald Kanyepi)

## 🚀 Tecnologias utilizadas

-   Pandas
-   Plotly
-   Python
-   Streamlit

## ⛲ Fonte

- MS/SVS/CGIAE - Sistema de Informações sobre Mortalidade - SIM
- Departamento de Informática do Sistema Único de Saúde (DATASUS)

## 🔥 Deploy!!

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://acidentes-transito-bahia.streamlit.app)

## Como executar esse streamlit web app em sua máquina local

1. Clone o repositório:
```
$ git clone https://github.com/rafaael1/streamlit_learn_acidentes_transito_bahia.git
$ cd streamlit_learn_acidentes_transito_bahia
```
2. Abra seu shell ou terminal e instale os pacotes relevantes usando o comando abaixo:
```
$ pip install -r requirements.txt
```
3. Inicie o aplicativo:
```
$ streamlit run app.py
```

Provavelmente, seu navegador abrirá com a URL http://localhost:8501.

### Estrutura de Pastas

```
streamlit_learn_acidentes_transito_bahia/
┣━━ 📂 assets               # Public assets
┃ ┣━━ acidentes_por_ano_segundo_cor_raca.csv
┃ ┣━━ acidentes_por_faixa_etaria_ops_por_ano.csv
┃ ┗━━ acidentes_por_sexo_por_ano.csv
┣━━ .gitignore
┣━━ .pre-commit-config.yaml
┣━━ LICENSE
┣━━ README.md
┣━━ app.py 
┗━━ requirements.txt 
```