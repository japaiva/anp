import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image

st.set_page_config(layout="wide")

@st.cache_data
def gerar_df():
    df = pd.read_excel(
        io = "dados_anp.xlsx",
        engine="openpyxl",
        sheet_name="Plan1",
        usecols="A:Q",
        nrows=22299
    )
    return df

df = gerar_df()

ColunasUteis = ["MÊS","PRODUTO","REGIÃO","ESTADO","PREÇO MÉDIO REVENDA"]
df2 = df[ColunasUteis]

with st.sidebar:
    st.subheader("ANALISE HISTORICA ANP")
    logo = Image.open("logo.jpg")
    st.image(logo, use_column_width=True)
    st.subheader("SELEÇÃO DE FILTROS")

    fProduto = st.selectbox(
        "Selecione o combustível:",
        options=df2["PRODUTO"].unique()
    )

    fEstado = st.selectbox(
        "Selecione o Estado:",
        options=df2["ESTADO"].unique()
    )

    dadosfiltro = df2.loc[
        (df2["PRODUTO"] == fProduto) &
        (df2["ESTADO"] == fEstado)
    ]

updateDatas = dadosfiltro["MÊS"].dt.strftime('%Y/%b')
dadosfiltro["MÊS"] = updateDatas[0:]

st.header("PREÇO DOS COMBUSTÍVEIS DO BRASIL")
st.markdown("Combustível:" + fProduto)
st.markdown("Estado:" + fEstado)

grafCombEstado = alt.Chart(dadosfiltro).mark_line(
    point=alt.OverlayMarkDef(color='red',size=20)
).encode(
    x = "MÊS:T",
    y = "PREÇO MÉDIO REVENDA",
    strokeWidth=alt.value(3)
).properties(
    height = 500,
    width = 1000
)

st.altair_chart(grafCombEstado)

#dadosfiltro
#streamlit run dashboard.py