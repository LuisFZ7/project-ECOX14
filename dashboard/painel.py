import streamlit as st
import consultas
import altair as alt
import pandas as pd

st.set_page_config(
    page_title="Indicador de Jogos",
    page_icon="🎮",
    layout="wide",
)

st.title("Indicador por gênero")

generos = consultas.generos()
names = consultas.names()

genero = st.sidebar.selectbox("Genero", generos["genero"])

dados = consultas.jogos_por_genero(genero)

total_vendas_genero = dados["vendas_totais"].sum()
dados["total_vendas_genero"] = total_vendas_genero

tabela_inteira = consultas.todos_jogos()

col1, col2, col3 = st.columns(3)

with col3:
    st.subheader(f"Totais de vendas de {genero}")

    st.metric(
        label="Vendas totais",
        value=f"{total_vendas_genero:,.0f}"
    )

with col2:
    st.dataframe(dados, hide_index=True)

with col1:
    st.subheader(f"Top 10 jogos de {genero} por vendas")

    dados_top10 = (
        dados.sort_values("vendas_totais", ascending=False)
        .head(10)
    )

    grafico = alt.Chart(dados_top10).mark_bar(
        color="#D96F2C"
    ).encode(
        x=alt.X(
            "nome:N",
            sort=alt.SortField(
                field="vendas_totais",
                order="descending"
            ),
            title="Jogo"
        ),
        y=alt.Y(
            "vendas_totais:Q",
            title="Vendas totais"
        ),
        tooltip=["nome", "vendas_totais"]
    ).properties(height=400)

    st.altair_chart(grafico, use_container_width=True)

st.divider()

st.subheader(f"Top 10 generos por vendas")

dados_top10_vendas = consultas.top10_generos()

grafico2 = alt.Chart(dados_top10_vendas).mark_bar(
        color="#5E25CC"
    ).encode(
        x=alt.X(
            "genero:N",
            sort=alt.SortField(
                field="total_vendas",
                order="descending"
            ),
            title="Genero"
        ),
        y=alt.Y(
            "total_vendas:Q",
            title="Vendas totais"
        ),
        tooltip=["genero", "total_vendas"]
    ).properties(height=400)

st.altair_chart(grafico2, use_container_width=True)

st.divider()

st.subheader("Base completa dos jogos")
st.dataframe(tabela_inteira, hide_index=True)
