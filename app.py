import streamlit as st
import pandas as pd
import numpy as np

# Configurar la página
st.set_page_config(page_title="Calculadora de Flecha", layout="wide")

# Estilos CSS para tarjetas modernas
st.markdown("""
    <style>
        .metric-card {
            background-color: #ffffff;
            border-radius: 12px;
            padding: 20px;
            margin: 10px 0;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
            text-align: center;
        }
        .metric-title {
            font-size: 16px;
            color: #333333;
            margin-bottom: 8px;
        }
        .metric-value {
            font-size: 24px;
            font-weight: bold;
            color: #333333;
        }
        .flecha-value {
            font-size: 36px;
            font-weight: bold;
            color: #b80000;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🧮 Calculadora de Flecha - Resultados en Tarjetas")

# Parámetros de entrada simulados (puedes reemplazar por tus inputs)
diametro_m = 0.014  # metros
peso_N_m = 9.2  # N/m
carga_rotura_N = 2550 * 9.81  # N
coef_seguridad = 2
vano_m = 50  # metros
viento_areaA_ms = 31.94
viento_areaB_ms = 38.88

# Función para calcular flecha y mostrar resultados con tarjetas

def calcular_flecha_con_tarjeta(area_nombre, velocidad_ms):
    pv = 0.613 * (velocidad_ms ** 2)
    pc = pv * diametro_m
    pa = np.sqrt(peso_N_m ** 2 + pc ** 2)
    tension_admisible = carga_rotura_N / coef_seguridad
    flecha = (pa * vano_m ** 2) / (8 * tension_admisible)

    st.markdown(f"### 🔸 Resultados para {area_nombre}")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Presión del Viento</div>
            <div class="metric-value">{pv:.2f} N/m²</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Carga Horizontal</div>
            <div class="metric-value">{pc:.4f} N/m</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Peso Aparente</div>
            <div class="metric-value">{pa:.4f} N/m</div>
        </div>
        """, unsafe_allow_html=True)

    col4, col5 = st.columns([1, 1])
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Tensión Admisible</div>
            <div class="metric-value">{tension_admisible:.2f} N</div>
        </div>
        """, unsafe_allow_html=True)
    with col5:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">📏 Flecha Calculada</div>
            <div class="flecha-value">{flecha:.3f} m</div>
        </div>
        """, unsafe_allow_html=True)

# Calcular para ambas áreas
calcular_flecha_con_tarjeta("Área A", viento_areaA_ms)
calcular_flecha_con_tarjeta("Área B", viento_areaB_ms)
