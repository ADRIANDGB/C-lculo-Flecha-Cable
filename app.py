import streamlit as st
import pandas as pd

st.set_page_config(page_title="Calculadora de Flecha - Fase 1", layout="wide")

import streamlit as st

# Configurar página
st.set_page_config(page_title="Calculadora Nutricional", layout="centered")


st.markdown("""
    <style>
    /* Moderniza los campos sin forzar modo claro */
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

st.markdown("## 🔌 Datos del Cable y Conversión")

col_izq, col_der = st.columns([1.3, 1])

with col_izq:
    calibre = st.text_input("Calibre", placeholder="Ej. 6 AWG")
    xlpe_mm = st.number_input("XLPE (mm)", value=0.0, step=0.01)
    tipo_conductor = st.selectbox("Tipo Conductor", ["AAC", "AAAC", "ACSR"])
    carga_rotura_kgf = st.number_input("Carga de Rotura (kgf)", value=0.0)
    diametro_mm = st.number_input("Diámetro Total (mm)", value=0.0)
    peso_kg_km = st.number_input("Peso Conductor (kg/km)", value=0.0)
    corriente = st.number_input("Corriente (A)", value=0.0)
    coef_seguridad = st.number_input("Coef. de Seguridad", value=1.0, step=0.1)

    st.markdown("### 🌬️ Condiciones de Entorno")
    viento_areaA_kmh = st.number_input("Velocidad Viento (km/h) - Área A", value=0.0)
    viento_areaB_kmh = st.number_input("Velocidad Viento (km/h) - Área B", value=0.0)
    vano_m = st.number_input("Distancia del Vano (m)", value=0.0)

with col_der:
    st.markdown("### 📋 Resumen del Cable")

    carga_rotura_N = carga_rotura_kgf * 9.81
    diametro_m = diametro_mm / 1000
    peso_N_m = (peso_kg_km * 9.81) / 1000
    viento_areaA_ms = viento_areaA_kmh / 3.6
    viento_areaB_ms = viento_areaB_kmh / 3.6

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

from xhtml2pdf import pisa
import io

# Convertir HTML a PDF usando xhtml2pdf
def convertir_a_pdf(html_content):
    pdf_stream = io.BytesIO()
    pisa_status = pisa.CreatePDF(
        io.StringIO(html_content), dest=pdf_stream
    )
    if pisa_status.err:
        return None
    return pdf_stream.getvalue()

# Tabla convertida a HTML
html_tabla = df_resumen.to_html(index=False)

# HTML completo con estilo
html_contenido = f"""
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            font-family: Arial, sans-serif;
        }}
        h2 {{
            text-align: center;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th, td {{
            border: 1px solid #444;
            padding: 8px;
            text-align: left;
        }}
        th {{
            background-color: #f2f2f2;
        }}
    </style>
</head>
<body>
    <h2>Resumen del Cable</h2>
    {html_tabla}
</body>
</html>
"""

# Botón para descargar PDF
if st.button("📄 Exportar resumen como PDF"):
    pdf_bytes = convertir_a_pdf(html_contenido)
    if pdf_bytes:
        st.download_button(
            label="📥 Descargar PDF",
            data=pdf_bytes,
            file_name="resumen_cable.pdf",
            mime="application/pdf"
        )
    else:
        st.error("❌ Error al generar el PDF")


# Fase 2, cálculo de Flecha
import streamlit as st
import numpy as np

# CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Flecha de Cable", layout="wide")

# CSS para tarjetas personalizadas
st.markdown("""
    <style>
        .tarjeta {
            background-color: white;
            border: 1px solid #e0e0e0;
            border-radius: 12px;
            padding: 1rem;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
            text-align: center;
            font-size: 14px;
        }
        .tarjeta h3 {
            margin: 0;
            font-size: 14px;
            color: #555;
        }
        .tarjeta p {
            margin: 0;
            font-size: 20px;
            font-weight: bold;
            color: #222;
        }
        .tarjeta-flecha {
            background-color: white;
            border: 2px solid #e6b8b8;
            border-radius: 14px;
            padding: 1.2rem;
            box-shadow: 3px 3px 12px rgba(0,0,0,0.07);
            text-align: center;
        }
        .tarjeta-flecha h3 {
            font-size: 16px;
            color: #880000;
            margin-bottom: 5px;
        }
        .tarjeta-flecha p {
            font-size: 34px;
            font-weight: bold;
            color: #b80000;
            margin: 0;
        }
    </style>
""", unsafe_allow_html=True)

# === PARÁMETROS
diametro_m = 0.014  # m
peso_N_m = 9.2
carga_rotura_N = 2550 * 9.81
coef_seguridad = 2
vano_m = 50
viento_areaA_ms = 31.94
viento_areaB_ms = 38.88

# === FUNCIÓN DE CÁLCULO
def calcular_flecha(area_nombre, velocidad_ms):
    pv = 0.613 * (velocidad_ms ** 2)
    pc = pv * diametro_m
    pa = np.sqrt(peso_N_m ** 2 + pc ** 2)
    tension = carga_rotura_N / coef_seguridad
    flecha = (pa * vano_m ** 2) / (8 * tension)

    st.markdown(f"### 🔸 Resultados para {area_nombre}")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="tarjeta">
            <h3>Presión viento</h3>
            <p>{pv:.2f} N/m²</p>
        </div>""", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="tarjeta">
            <h3>Carga horizontal</h3>
            <p>{pc:.4f} N/m</p>
        </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="tarjeta">
            <h3>Peso aparente</h3>
            <p>{pa:.4f} N/m</p>
        </div>""", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="tarjeta">
            <h3>Tensión admisible</h3>
            <p>{tension:.2f} N</p>
        </div>""", unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="tarjeta-flecha">
            <h3>📏 Flecha</h3>
            <p>{flecha:.3f} m</p>
        </div>""", unsafe_allow_html=True)

# === MOSTRAR RESULTADOS
calcular_flecha("Área A", viento_areaA_ms)
calcular_flecha("Área B", viento_areaB_ms)




#FASE 3 - VISUALIZACION

import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.markdown("## 🏗️ Esquema del Cable y Flecha")

# Selector de área
area_seleccionada = st.selectbox("Selecciona el área para graficar:", ["Área A", "Área B"])

# Determinar datos según el área
if area_seleccionada == "Área A":
    velocidad_viento = viento_areaA_ms
    label_area = "Área A"
else:
    velocidad_viento = viento_areaB_ms
    label_area = "Área B"

# Intentar graficar si los datos son válidos
try:
    pv = 0.613 * (velocidad_viento ** 2)
    pc = pv * diametro_m
    pa = np.sqrt(peso_N_m ** 2 + pc ** 2)
    tension_admisible = carga_rotura_N / coef_seguridad
    flecha = (pa * vano_m ** 2) / (8 * tension_admisible)

    if any(np.isnan(val) or np.isinf(val) for val in [pv, pc, pa, flecha]):
        raise ValueError("❌ Hay valores inválidos en los cálculos.")

    # Coordenadas de la curva del cable
    x = np.linspace(0, vano_m, 100)
    y = - (4 * flecha / vano_m ** 2) * x * (vano_m - x)

    torre_altura = abs(flecha) * 1.8
    y += torre_altura  # elevar la curva

    x_centro = vano_m / 2
    y_centro = min(y)

    fig = go.Figure()

    # Curva del cable
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', line=dict(color='black', width=3), name='Cable'))

    # Poste izquierdo
    fig.add_trace(go.Scatter(x=[0, 0], y=[0, torre_altura], mode='lines', line=dict(color='black', width=4), showlegend=False))
    fig.add_annotation(x=-1, y=torre_altura + 0.3, text="Poste B", showarrow=False, font=dict(size=12))

    # Poste derecho
    fig.add_trace(go.Scatter(x=[vano_m, vano_m], y=[0, torre_altura], mode='lines', line=dict(color='black', width=4), showlegend=False))
    fig.add_annotation(x=vano_m - 1.2, y=torre_altura + 0.3, text="Poste A", showarrow=False, font=dict(size=12))

    # Altura de fijación
    fig.add_trace(go.Scatter(x=[0, vano_m], y=[torre_altura, torre_altura], mode='lines', line=dict(color='gray', dash='dash'), name='Altura de fijación'))

    # Flecha
    fig.add_trace(go.Scatter(x=[x_centro, x_centro], y=[y_centro, torre_altura], mode='lines', line=dict(color='red', width=2), name='Flecha f'))
    fig.add_annotation(x=x_centro + 1, y=(y_centro + torre_altura)/2, text=f"f ≈ {flecha:.3f} m", showarrow=False, font=dict(color='red', size=12))

    # Velocidad viento
    fig.add_annotation(x= vano_m / 2 - 3, y=torre_altura + 0.8,
                       text=f"🌬️ Viento: {velocidad_viento:.2f} m/s", showarrow=False,
                       font=dict(color='blue', size=12))

    # Configuración visual
    fig.update_layout(
        title=f"Esquema de Tendido y Flecha - {label_area}",
        margin=dict(l=20, r=20, t=40, b=20),
        showlegend=True,
        height=500
    )
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)

    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"⚠️ Error al generar el gráfico: {e}")



#FASE 4 - EXPORTACION DATOS

from xhtml2pdf import pisa
from io import BytesIO
import base64
import os

# 👉 FUNCIONES DE EXPORTACIÓN A PDF
def generar_imagen_del_grafico(fig):
    img_buffer = BytesIO()
    fig.savefig(img_buffer, format="png", bbox_inches="tight")
    img_buffer.seek(0)
    encoded = base64.b64encode(img_buffer.read()).decode('utf-8')
    return f"<img src='data:image/png;base64,{encoded}' width='600'/>"

def generar_pdf_html(tabla_html, tabla_areaA_html, tabla_areaB_html, grafico_html):
    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; }}
            h2 {{ color: #333; }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 10px;
            }}
            th, td {{
                border: 1px solid #aaa;
                padding: 6px;
                text-align: left;
            }}
            th {{
                background-color: #f2f2f2;
            }}
        </style>
    </head>
    <body>
        <h2>Resumen del Cable</h2>
        {tabla_html}

        <h2>Cálculo de Flecha - Área A</h2>
        {tabla_areaA_html}

        <h2>Cálculo de Flecha - Área B</h2>
        {tabla_areaB_html}

        <h2>Visualización del Cable (Área A)</h2>
        {grafico_html}
    </body>
    </html>
    """
    return html

def convertir_html_a_pdf(html_content):
    pdf_stream = BytesIO()
    pisa_status = pisa.CreatePDF(html_content, dest=pdf_stream)
    if pisa_status.err:
        return None
    return pdf_stream.getvalue()

# 👉 BOTÓN PARA EXPORTAR
if st.button("📄 Exportar todo como PDF"):
    # Tabla resumen cable
    tabla_cable_html = df_resumen.to_html(index=False)

    # Recalcular datos de Área A y B (repetimos lógica para asegurar valores)
    def datos_flecha(viento_ms):
        pv = 0.613 * (viento_ms ** 2)
        pc = pv * diametro_m
        pa = np.sqrt(peso_N_m ** 2 + pc ** 2)
        tension = carga_rotura_N / coef_seguridad
        flecha = (pa * vano_m ** 2) / (8 * tension)
        return {
            "Presión Viento pv (N/m²)": round(pv, 2),
            "Carga Horizontal del Viento Pc (N/m)": round(pc, 4),
            "Peso Aparente Viento Pa (N/m)": round(pa, 4),
            "Tensión Horizontal Admisible (N)": round(tension, 2),
            "Flecha (m)": round(flecha, 4)
        }

    df_A = pd.DataFrame(datos_flecha(viento_areaA_ms).items(), columns=["Parámetro", "Valor"])
    df_B = pd.DataFrame(datos_flecha(viento_areaB_ms).items(), columns=["Parámetro", "Valor"])

    tabla_areaA_html = df_A.to_html(index=False)
    tabla_areaB_html = df_B.to_html(index=False)

    # Generar gráfico Área A
    # Usamos nuevamente lo de la Fase 3
    pv = 0.613 * (viento_areaA_ms ** 2)
    pc = pv * diametro_m
    pa = np.sqrt(peso_N_m ** 2 + pc ** 2)
    tension_admisible = carga_rotura_N / coef_seguridad
    flecha = (pa * vano_m ** 2) / (8 * tension_admisible)

    x = np.linspace(0, vano_m, 100)
    y = - (4 * flecha / vano_m ** 2) * x * (vano_m - x)
    torre_altura = abs(flecha) * 1.8
    y += torre_altura

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot([0, vano_m], [torre_altura, torre_altura], color="gray", linestyle="--", label="Altura de fijación")
    ax.plot(x, y, color="black", linewidth=2, label="Cable")
    ax.plot([0, 0], [0, torre_altura], color="black", linewidth=3)
    ax.plot([vano_m, vano_m], [0, torre_altura], color="black", linewidth=3)
    ax.text(-0.5, torre_altura + 0.3, "Poste B", fontsize=11)
    ax.text(vano_m - 1.2, torre_altura + 0.3, "Poste A", fontsize=11)
    x_centro = vano_m / 2
    y_centro = min(y)
    ax.plot([x_centro, x_centro], [y_centro, torre_altura], color="red", linewidth=2, label="Flecha f")
    ax.text(x_centro + 1, (y_centro + torre_altura) / 2, f"f ≈ {flecha:.3f} m", color="red", fontsize=10, weight="bold")
    ax.axis("off")
    grafico_html = generar_imagen_del_grafico(fig)

    # Juntar todo en HTML y convertir a PDF
    html_final = generar_pdf_html(tabla_cable_html, tabla_areaA_html, tabla_areaB_html, grafico_html)
    pdf_bytes = convertir_html_a_pdf(html_final)

    if pdf_bytes:
        st.download_button(
            label="📥 Descargar PDF completo",
            data=pdf_bytes,
            file_name="resumen_flecha_cable.pdf",
            mime="application/pdf"
        )
    else:
        st.error("❌ Hubo un error al generar el PDF.")

