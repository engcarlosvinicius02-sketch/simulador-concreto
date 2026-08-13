import streamlit as st
import joblib
import numpy as np

# Carrega a IA que você treinou
modelo = joblib.load('modelo_concreto.pkl')

st.title("Simulador de Resistência do Concreto 🏗️")
st.write("Versão Realística: Calibração para Canteiro de Obras")
st.divider()

# Escolha do perfil do usuário
modo = st.sidebar.radio("Como você deseja inserir as medidas?", 
                        ["Medidas de Obra (Sacos e Latas)", "Medidas de Laboratório (kg/m³)"])

st.sidebar.markdown("---")

if modo == "Medidas de Obra (Sacos e Latas)":
    st.sidebar.info("Baseado em 1 Saco de Cimento (50kg) e Latas padrão de 18L")
    
    sacos_cimento = 1.0 
    latas_areia = st.sidebar.number_input("Latas de Areia (18L)", min_value=0.0, value=4.0)
    latas_brita = st.sidebar.number_input("Latas de Brita (18L)", min_value=0.0, value=6.0)
    latas_agua = st.sidebar.number_input("Latas de Água (18L)", min_value=0.0, value=1.5)
    idade = st.sidebar.number_input("Idade de Cura (Dias)", min_value=1, value=28)
    
    # Tratando o "Inchaço da Areia" real da obra (areia úmida ocupa mais volume e tem menos massa seca)
    massa_cimento = 50.0 
    massa_areia = (latas_areia * 18.0 * 1.45) * 0.85 # Fator de correção de umidade da areia de obra
    massa_brita = latas_brita * 18.0 * 1.45
    massa_agua = latas_agua * 18.0 * 1.0
    
    vol_cimento = massa_cimento / 3150.0
    vol_areia = massa_areia / 2650.0
    vol_brita = massa_brita / 2700.0
    vol_agua = massa_agua / 1000.0
    vol_total_m3 = vol_cimento + vol_areia + vol_brita + vol_agua
    
    cimento = massa_cimento / vol_total_m3
    areia = massa_areia / vol_total_m3
    brita = massa_brita / vol_total_m3
    agua = massa_agua / vol_total_m3
    escoria = 0.0
    cinza = 0.0
    superplast = 0.0

else:
    cimento = st.sidebar.number_input("Cimento", min_value=0.0, value=350.0)
    escoria = st.sidebar.number_input("Escória", min_value=0.0, value=0.0)
    cinza = st.sidebar.number_input("Cinza Volante", min_value=0.0, value=0.0)
    agua = st.sidebar.number_input("Água", min_value=0.0, value=180.0)
    superplast = st.sidebar.number_input("Superplastificante", min_value=0.0, value=0.0)
    brita = st.sidebar.number_input("Agregado Graúdo (Brita)", min_value=0.0, value=1050.0)
    areia = st.sidebar.number_input("Agregado Miúdo (Areia)", min_value=0.0, value=750.0)
    idade = st.sidebar.number_input("Idade (Dias)", min_value=1, value=28)

# Botão de calcular principal
if st.button("Prever Resistência Real de Obra", type="primary"):
    entrada = np.array([[cimento, escoria, cinza, agua, superplast, brita, areia, idade]])
    previsao_laboratorio = modelo.predict(entrada)[0]
    
    # APLICAÇÃO DO FATOR DE CANTEIRO (Desconto de 22% para refletir as perdas reais de execução)
    if modo == "Medidas de Obra (Sacos e Latas)":
        fator_execucao_obra = 0.78 
        previsao_final = previsao_laboratorio * fator_execucao_obra
    else:
        previsao_final = previsao_laboratorio # Se for modo laboratório, mantém puro
    
    st.success(f"A Resistência Estimada para o Canteiro de Obras aos {int(idade)} dias é de aproximadamente **{previsao_final:.2f} MPa**")
    
    if modo == "Medidas de Obra (Sacos e Latas)":
        st.warning(f"⚠️ *Nota de Engenharia:* O modelo calculou {previsao_laboratorio:.1f} MPa em condições de laboratório puro, mas aplicamos um fator de redução de 22% para contabilizar o atrito, umidade dos agregados e condições reais de lançamento na obra.")
