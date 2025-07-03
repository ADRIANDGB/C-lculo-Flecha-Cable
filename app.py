# --- FASE 1: IMPORTAR LIBRERIAS Y CONFIGURACION INICIAL ---
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from xhtml2pdf import pisa
from io import BytesIO
import base64

st.set_page_config(page_title="Calculadora de Flecha - Fase 1", layout="wide")

st.markdown("""
    <style>
    input, select, textarea {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: inherit !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 8px !important;
        padding: 8px !important;
    }
    div[data-baseweb="select"] > div {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border-radius: 8px !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    div[role="radiogroup"] > label {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border-radius: 8px !important;
        padding: 6px 10px !important;
        margin-bottom: 4px;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- FASE 2: ENTRADA DE DATOS Y CONVERSIONES ---
st.title("🧮 Calculadora de Flecha - Entrada de Datos y Resumen")

with st.sidebar.expander("📥 Ingreso de Datos del Cable", expanded=True):
    calibre = st.text_input("Calibre", placeholder="Ej. 6 AWG")
    xlpe_mm = st.number_input("XLPE (mm)", value=0.0, step=0.01)
    tipo_conductor = st.selectbox("Tipo Conductor", ["AAC", "AAAC", "ACSR"])
    carga_rotura_kgf = st.number_input("Carga de Rotura (kgf)", value=0.0)
    diametro_mm = st.number_input("Diámetro Total (mm)", value=0.0)
    peso_kg_km = st.number_input("Peso Conductor (kg/km)", value=0.0)
    corriente = st.number_input("Corriente (A)", value=0.0)
    coef_seguridad = st.number_input("Coef. de Seguridad", value=1.0, step=0.1)
    viento_areaA_kmh = st.number_input("Velocidad Viento (km/h) - Área A", value=0.0)
    viento_areaB_kmh = st.number_input("Velocidad Viento (km/h) - Área B", value=0.0)
    vano_m = st.number_input("Distancia del Vano (m)", value=0.0)

# Conversiones
peso_N_m = peso_kg_km * 9.81 / 1000
carga_rotura_N = carga_rotura_kgf * 9.81
diametro_m = diametro_mm / 1000
viento_areaA_ms = viento_areaA_kmh * 1000 / 3600
viento_areaB_ms = viento_areaB_kmh * 1000 / 3600

# Mostrar resumen
datos_resumen = {
    "Parámetro": [
        "Calibre", "XLPE (mm)", "Tipo Conductor", "Carga Rotura (kgf)",
        "Carga Rotura (N)", "Diámetro Total (mm)", "Diámetro Total (m)",
        "Peso (kg/km)", "Peso (N/m)", "Corriente (A)", "Coef. Seguridad",
        "Viento Área A (km/h)", "Viento Área A (m/s)",
        "Viento Área B (km/h)", "Viento Área B (m/s)", "Distancia del Vano (m)"
    ],
    "Valor": [
        calibre, xlpe_mm, tipo_conductor, carga_rotura_kgf,
        round(carga_rotura_N, 2), diametro_mm, round(diametro_m, 5),
        peso_kg_km, round(peso_N_m, 5), corriente, coef_seguridad,
        viento_areaA_kmh, round(viento_areaA_ms, 2),
        viento_areaB_kmh, round(viento_areaB_ms, 2), vano_m
    ]
}

df_resumen = pd.DataFrame(datos_resumen)
st.markdown("## 📋 Resumen de Datos del Cable")
st.dataframe(df_resumen, use_container_width=True)
