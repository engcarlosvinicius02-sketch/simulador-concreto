import streamlit as st
import joblib
import numpy as np

# Carrega a IA que você treinou
modelo = joblib.load('modelo_concreto.pkl')

# Desenha a interface do site
st.title("Simulador de Resistência do Concreto 🏗️")
st.write("Projeto Integrado Multidisciplinar - Previsão de fck usando Inteligência Artificial")
st.divider()

st.sidebar.header("Insira os dados do traço (kg/m³)")

# Cria as caixas para o usuário digitar os valores
cimento = st.sidebar.number_input("Cimento", min_value=0.0, value=350.0)
escoria = st.sidebar.number_input("Escória", min_value=0.0, value=0.0)
cinza = st.sidebar.number_input("Cinza Volante", min_value=0.0, value=0.0)
agua = st.sidebar.number_input("Água", min_value=0.0, value=180.0)
superplast = st.sidebar.number_input("Superplastificante", min_value=0.0, value=0.0)
brita = st.sidebar.number_input("Agregado Graúdo (Brita)", min_value=0.0, value=1050.0)
areia = st.sidebar.number_input("Agregado Miúdo (Areia)", min_value=0.0, value=750.0)
idade = st.sidebar.number_input("Idade (Dias)", min_value=1, value=28)

# Botão de calcular
if st.button("Prever Resistência", type="primary"):
    entrada = np.array([[cimento, escoria, cinza, agua, superplast, brita, areia, idade]])
    previsao = modelo.predict(entrada)
    st.success(f"A Resistência Estimada (fck) aos {idade} dias é de {previsao[0]:.2f} MPa")