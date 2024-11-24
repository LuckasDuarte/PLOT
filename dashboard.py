import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(layout="wide")

# Título da página
st.markdown("# Análises de Atividades Logísticas - Relatório de Movimentações")

# Sidebar melhorada
st.sidebar.markdown("# Filtros de Análise")

# Carregar o arquivo Excel
df = pd.read_excel("BASE_MOVIMENTACOES.xlsx")

# Garantir que a coluna 'DATA' seja convertida para datetime, se não for
df["DATA"] = pd.to_datetime(df["DATA"])

# Criar uma coluna "MES" com formato 'YYYY-MM'
df["MES"] = df["DATA"].dt.to_period("M").astype(str)

# Ordenar os dados por data
df_sorted = df.sort_values(by="DATA", ascending=True)

# Filtro de seleção do mês
mes = st.sidebar.selectbox("Selecione o Mês", df_sorted["MES"].unique())

# Filtro adicional para selecionar o tipo de atividade
atividade = st.sidebar.multiselect(
    "Selecione o Tipo de Atividade",
    options=df["AÇÃO"].unique(),
    default=df["AÇÃO"].unique()
)

# Filtro adicional para selecionar o intervalo de data
data_inicio = st.sidebar.date_input("Data de Início", df["DATA"].min())
data_fim = st.sidebar.date_input("Data de Fim", df["DATA"].max())

# Filtrar os dados de acordo com os filtros selecionados
df_filtered = df_sorted[
    (df_sorted["MES"] == mes) &
    (df_sorted["AÇÃO"].isin(atividade)) &
    (df_sorted["DATA"] >= pd.to_datetime(data_inicio)) &
    (df_sorted["DATA"] <= pd.to_datetime(data_fim))
]

# Exibição de gráficos
col1, col2 = st.columns(2)
col3, col4, col5 = st.columns(3)

# 1. **Quantidade de Atividades Realizadas** por tipo
atividade_contagem = df_filtered["AÇÃO"].value_counts().reset_index()
atividade_contagem.columns = ["Ação", "Quantidade"]
fig_atividade_contagem = px.bar(atividade_contagem, x="Ação", y="Quantidade", title="Total de Atividades Realizadas por Tipo")
fig_atividade_contagem.update_layout(margin=dict(l=40, r=40, t=40, b=40))  # Ajustando margens
col1.plotly_chart(fig_atividade_contagem, use_container_width=True)

# Adicionando espaçamento entre os gráficos
st.markdown("<br><br>", unsafe_allow_html=True)

# 2. **Volume de Atividades por Data**
df_filtered["Dia"] = df_filtered["DATA"].dt.day
volume_dia = df_filtered.groupby("Dia").size().reset_index(name="Volume")
fig_volume_dia = px.line(volume_dia, x="Dia", y="Volume", title="Volume de Atividades por Dia")
fig_volume_dia.update_layout(margin=dict(l=40, r=40, t=40, b=40))  # Ajustando margens
col2.plotly_chart(fig_volume_dia, use_container_width=True)

# Adicionando espaçamento entre os gráficos
st.markdown("<br><br>", unsafe_allow_html=True)

# 3. **Volume de Atividades por Hora do Dia**
df_filtered["Hora"] = df_filtered["DATA"].dt.hour
atividade_por_hora = df_filtered.groupby("Hora").size().reset_index(name="Volume")
fig_atividade_por_hora = px.bar(atividade_por_hora, x="Hora", y="Volume", title="Atividades Realizadas por Hora")
fig_atividade_por_hora.update_layout(margin=dict(l=40, r=40, t=40, b=40))  # Ajustando margens
col3.plotly_chart(fig_atividade_por_hora, use_container_width=True)

# Adicionando espaçamento entre os gráficos
st.markdown("<br><br>", unsafe_allow_html=True)
