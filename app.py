import streamlit as st
import pandas as pd

st.set_page_config(page_title="Calculadora de Flecha - Fase 1", layout="wide")

st.title("🧮 Calculadora de Flecha - Entrada de Datos y Conversión")

st.markdown("### 🔌 Ingreso de Datos del Cable")

col1, col2 = st.columns([1, 1])

with col1:
    calibre = st.text_input("Calibre", placeholder="Ej. 6 AWG")
    xlpe_mm = st.number_input("XLPE (mm)", value=0.0, step=0.01)
    tipo_conductor = st.selectbox("Tipo Conductor", ["AAC", "AAAC", "ACSR"])
    carga_rotura_kgf = st.number_input("Carga de Rotura (kgf)", value=0.0)
    diametro_mm = st.number_input("Diámetro Total (mm)", value=0.0)
    peso_kg_km = st.number_input("Peso Conductor (kg/km)", value=0.0)
    corriente = st.number_input("Corriente (A)", value=0.0)
    coef_seguridad = st.number_input("Coef. de Seguridad", value=1.0, step=0.1)

with col2:
    st.markdown("#### 🔁 Conversión Automática de Unidades")

    carga_rotura_N = carga_rotura_kgf * 9.81
    diametro_m = diametro_mm / 1000
    peso_N_m = (peso_kg_km * 9.81) / 1000

    st.write(f"**Carga de Rotura (N):** {carga_rotura_N:,.2f}")
    st.write(f"**Diámetro Total (m):** {diametro_m:.5f}")
    st.write(f"**Peso Conductor (N/m):** {peso_N_m:.5f}")

st.markdown("---")
st.markdown("### 🌬️ Condiciones de Entorno")

col3, col4 = st.columns([1, 1])

with col3:
    viento_areaA_kmh = st.number_input("Velocidad Viento (km/h) - Área A", value=0.0)
    viento_areaB_kmh = st.number_input("Velocidad Viento (km/h) - Área B", value=0.0)
    vano_m = st.number_input("Distancia del Vano (m)", value=0.0)

with col4:
    st.markdown("#### 🔁 Conversión Automática")
    viento_areaA_ms = viento_areaA_kmh / 3.6
    viento_areaB_ms = viento_areaB_kmh / 3.6

    st.write(f"**Área A (m/s):** {viento_areaA_ms:.2f}")
    st.write(f"**Área B (m/s):** {viento_areaB_ms:.2f}")

# ============================
# RESUMEN DE CARACTERÍSTICAS
# ============================

st.markdown("---")
st.markdown("### 📋 Resumen del Cable Ingresado")

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
st.dataframe(df_resumen, use_container_width=True)
