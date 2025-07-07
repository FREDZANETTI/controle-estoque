import streamlit as st
import pandas as pd
import os
from datetime import datetime

DATA_FILE = os.path.join("data", "estoque.csv")

def carregar_dados():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=["Data", "Produto", "Categoria", "Quantidade", "Tipo"])

def salvar_dados(df):
    df.to_csv(DATA_FILE, index=False)

def registrar_movimentacao(data, produto, categoria, quantidade, tipo):
    df = carregar_dados()
    nova_linha = {
        "Data": data,
        "Produto": produto,
        "Categoria": categoria,
        "Quantidade": quantidade if tipo == "Entrada" else -quantidade,
        "Tipo": tipo
    }
    df = pd.concat([df, pd.DataFrame([nova_linha])], ignore_index=True)
    salvar_dados(df)

st.title("📦 Controle de Estoque")

with st.form("form_estoque"):
    data = st.date_input("Data", value=datetime.today())
    produto = st.text_input("Nome do Produto")
    categoria = st.text_input("Categoria")
    quantidade = st.number_input("Quantidade", min_value=1)
    tipo = st.selectbox("Tipo", ["Entrada", "Saída"])
    submitted = st.form_submit_button("Registrar")

    if submitted:
        registrar_movimentacao(data, produto, categoria, quantidade, tipo)
        st.success("Movimentação registrada com sucesso!")

# Dashboard
st.header("📊 Dashboard do Estoque")
df = carregar_dados()
if not df.empty:
    saldo = df.groupby("Produto")["Quantidade"].sum().reset_index()
    st.bar_chart(saldo.set_index("Produto"))
    with st.expander("📄 Dados brutos"):
        st.dataframe(df)
else:
    st.info("Nenhum dado registrado ainda.")
