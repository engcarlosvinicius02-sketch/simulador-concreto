import streamlit as st
import joblib
import numpy as np

# Carrega a IA que você treinou
modelo = joblib.load('modelo_concreto.pkl')

st.title("Simulador de Resistência do Concreto 🏗️")
st.write("Previsão de fck usando Inteligência Artificial e Conversão de Traço")
st.divider()

# Escolha do perfil do usuário
modo = st.sidebar.radio("Como você deseja inserir as medidas?", 
                        ["Medidas de Obra (Sacos e Latas)", "Medidas de Laboratório (kg/m³)"])

st.sidebar.markdown("---")

if modo == "Medidas de Obra (Sacos e Latas)":
    st.sidebar.info("Baseado em 1 Saco de Cimento (50kg) e Latas padrão de 18L")
    
    sacos_cimento = 1.0 # Fixo em 1 saco para o traço base
    latas_areia = st.sidebar.number_input("Latas de Areia (18L)", min_value=0.0, value=4.0)
    latas_brita = st.sidebar.number_input("Latas de Brita (18L)", min_value=0.0, value=6.0)
    latas_agua = st.sidebar.number_input("Latas de Água (18L)", min_value=0.0, value=1.5)
    idade = st.sidebar.number_input("Idade de Cura (Dias)", min_value=1, value=28)
    
    # 1. Convertendo Volume (Latas) para Massa (kg)
    # Massa Unitária média (kg/L): Areia = 1.45 | Brita = 1.45 | Água = 1.0
    massa_cimento = 50.0 
    massa_areia = latas_areia * 18.0 * 1.45
    massa_brita = latas_brita * 18.0 * 1.45
    massa_agua = latas_agua * 18.0 * 1.0
    
    # 2. Calculando o Volume Absoluto da mistura (m³)
    # Massa Específica média (kg/m³): Cimento = 3150 | Areia = 2650 | Brita = 2700 | Água = 1000
    vol_cimento = massa_cimento / 3150.0
    vol_areia = massa_areia / 2650.0
    vol_brita = massa_brita / 2700.0
    vol_agua = massa_agua / 1000.0
    vol_total_m3 = vol_cimento + vol_areia + vol_brita + vol_agua
    
    # 3. Descobrindo a quantidade de materiais para fazer exatamente 1 m³ (kg/m³)
    cimento = massa_cimento / vol_total_m3
    areia = massa_areia / vol_total_m3
    brita = massa_brita / vol_total_m3
    agua = massa_agua / vol_total_m3
    escoria = 0.0
    cinza = 0.0
    superplast = 0.0

else:
    # Modo Engenheiro (kg/m³) - O código original que você já tinha
    st.sidebar.info("Insira os quantitativos exatos para 1 m³ de concreto")
    cimento = st.sidebar.number_input("Cimento", min_value=0.0, value=350.0)
    escoria = st.sidebar.number_input("Escória", min_value=0.0, value=0.0)
    cinza = st.sidebar.number_input("Cinza Volante", min_value=0.0, value=0.0)
    agua = st.sidebar.number_input("Água", min_value=0.0, value=180.0)
    superplast = st.sidebar.number_input("Superplastificante", min_value=0.0, value=0.0)
    brita = st.sidebar.number_input("Agregado Graúdo (Brita)", min_value=0.0, value=1050.0)
    areia = st.sidebar.number_input("Agregado Miúdo (Areia)", min_value=0.0, value=750.0)
    idade = st.sidebar.number_input("Idade (Dias)", min_value=1, value=28)

# Botão de calcular principal
if st.button("Prever Resistência", type="primary"):
    entrada = np.array([[cimento, escoria, cinza, agua, superplast, brita, areia, idade]])
    previsao = modelo.predict(entrada)
    
    # Mostra o resultado com destaque
    st.success(f"A Resistência Estimada (fck) aos {int(idade)} dias é de {previsao[0]:.2f} MPa")
    
    # Se o usuário usou latas, o sistema mostra a conversão técnica para provar que funciona
    if modo == "Medidas de Obra (Sacos e Latas)":
        st.info(f"**Análise Técnica dos Bastidores:** Para calcular isso, a IA converteu suas latas no seguinte consumo: {cimento:.0f} kg/m³ de Cimento, {areia:.0f} kg/m³ de Areia, {brita:.0f} kg/m³ de Brita e {agua:.0f} Litros/m³ de Água.")
