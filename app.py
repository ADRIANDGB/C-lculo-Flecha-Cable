# FASE 1 - ENTRADA DE DATOS

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from xhtml2pdf import pisa
from io import BytesIO
import base64

st.set_page_config(page_title="Calculadora Flecha", layout="centered")

# ==== ESTILOS MODERNOS ==== #
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

# ==== CONVERSIONES ====
carga_rotura_N = carga_rotura_kgf * 9.81
peso_N_m = peso_kg_km * 9.81 / 1000
diametro_m = diametro_mm / 1000
viento_areaA_ms = viento_areaA_kmh / 3.6
viento_areaB_ms = viento_areaB_kmh / 3.6

# ==== RESUMEN EN TABLA ====
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

st.markdown("## 🔎 Resumen del Cable")
df_resumen = pd.DataFrame(datos_resumen)
st.dataframe(df_resumen, use_container_width=True)

# FASE 2 - CÁLCULO DE FLECHA

st.markdown("---")
st.markdown("## 📉 Cálculo de la Flecha")

st.markdown("### 🧮 Fórmulas utilizadas")
st.latex(r"pv = 0.613 \cdot v^2")
st.latex(r"P_c = pv \cdot d")
st.latex(r"P_a = \sqrt{w^2 + P_c^2}")
st.latex(r"T = \frac{\text{Carga de rotura (N)}}{\text{Coeficiente de Seguridad}}")
st.latex(r"f = \frac{P_a \cdot L^2}{8 \cdot T}")

# Calculo de flecha con métricas
from streamlit_extras.metric_cards import style_metric_cards

def calcular_flecha(area_nombre, velocidad_ms):
    pv = 0.613 * (velocidad_ms ** 2)
    pc = pv * diametro_m
    pa = np.sqrt(peso_N_m ** 2 + pc ** 2)
    tension_admisible = carga_rotura_N / coef_seguridad
    flecha = (pa * vano_m ** 2) / (8 * tension_admisible)

    st.markdown(f"### 📍 Resultados para {area_nombre}")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Presión Viento pv (N/m²)", round(pv, 2))
        st.metric("Carga Horizontal del Viento Pc", round(pc, 3))
    with col2:
        st.metric("Peso Aparente Pa", round(pa, 3))
        st.metric("Tensión Admisible T", round(tension_admisible, 2))
    with col3:
        st.metric("📏 Flecha (m)", f"{flecha:.3f}", delta="", delta_color="inverse")

    style_metric_cards(border_left_color="#AAAAAA", background_color="#f9f9f9")

    return flecha

flecha_A = calcular_flecha("Área A", viento_areaA_ms)
flecha_B = calcular_flecha("Área B", viento_areaB_ms)

# FASE 3 - VISUALIZACIÓN DE FLECHA

st.markdown("---")
st.markdown("## 🏗️ Visualización del Cable y Flecha")

area = st.selectbox("Selecciona área a graficar:", ["Área A", "Área B"])
vel = viento_areaA_ms if area == "Área A" else viento_areaB_ms
flecha = flecha_A if area == "Área A" else flecha_B

pv = 0.613 * (vel ** 2)
pc = pv * diametro_m
pa = np.sqrt(peso_N_m ** 2 + pc ** 2)
tension_admisible = carga_rotura_N / coef_seguridad

x = np.linspace(0, vano_m, 100)
y = - (4 * flecha / vano_m ** 2) * x * (vano_m - x)
torre_altura = abs(flecha) * 1.8
y += torre_altura
x_centro = vano_m / 2
y_centro = min(y)

fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=y, mode='lines', line=dict(color='black', width=3), name='Cable'))
fig.add_trace(go.Scatter(x=[0, 0], y=[0, torre_altura], mode='lines', line=dict(color='black', width=4)))
fig.add_trace(go.Scatter(x=[vano_m, vano_m], y=[0, torre_altura], mode='lines', line=dict(color='black', width=4)))
fig.add_trace(go.Scatter(x=[0, vano_m], y=[torre_altura, torre_altura], mode='lines', line=dict(color='gray', dash='dash')))
fig.add_trace(go.Scatter(x=[x_centro, x_centro], y=[y_centro, torre_altura], mode='lines', line=dict(color='red', width=2)))
fig.add_annotation(x=x_centro + 1, y=(y_centro + torre_altura)/2, text=f"f ≈ {flecha:.3f} m", font=dict(color='red', size=14))
fig.add_annotation(x= vano_m / 2 - 3, y=torre_altura + 0.8, text=f"🌬️ Viento: {vel:.2f} m/s", font=dict(color='blue', size=12))
fig.update_layout(title=f"Esquema de Tendido y Flecha - {area}", height=500, showlegend=False)
fig.update_xaxes(visible=False)
fig.update_yaxes(visible=False)
st.plotly_chart(fig, use_container_width=True)

def exportar_pdf():
    buffer = BytesIO()
    tabla_html = df_resumen.to_html(index=False)
    contenido_html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; text-align: center; }}
            h2 {{ color: #2F4F4F; }}
            table {{ width: 90%; margin: auto; border-collapse: collapse; }}
            th, td {{ border: 1px solid #999; padding: 8px; text-align: center; }}
            th {{ background-color: #eee; }}
        </style>
    </head>
    <body>
        <h2>Resumen de Datos del Cable</h2>
        {tabla_html}
    </body>
    </html>
    """
    pisa_status = pisa.CreatePDF(contenido_html, dest=buffer)
    if not pisa_status.err:
        st.download_button("📄 Descargar PDF del Resumen", buffer.getvalue(), file_name="resumen_flecha.pdf", mime="application/pdf")
    else:
        st.error("Error al generar el PDF.")

exportar_pdf()



