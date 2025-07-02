import streamlit as st
import pandas as pd

st.set_page_config(page_title="Calculadora de Flecha - Fase 1", layout="wide")

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


#Fase 2, calculo de Flecha
import numpy as np

st.markdown("---")
st.markdown("## 📉 Cálculo de la Flecha")

# Mostrar fórmulas
st.markdown("### 🧮 Fórmulas utilizadas")
st.latex(r"pv = 0.613 \cdot v^2")
st.latex(r"P_c = pv \cdot d")
st.latex(r"P_a = \sqrt{w^2 + P_c^2}")
st.latex(r"T = \frac{\text{Carga de rotura (N)}}{\text{Coeficiente de Seguridad}}")
st.latex(r"f = \frac{P_a \cdot L^2}{8 \cdot T}")

# === CALCULOS PARA AMBAS ÁREAS ===
def calcular_flecha(area_nombre, velocidad_ms):
    pv = 0.613 * (velocidad_ms ** 2)
    pc = pv * diametro_m
    pa = np.sqrt(peso_N_m ** 2 + pc ** 2)
    tension_admisible = carga_rotura_N / coef_seguridad
    flecha = (pa * vano_m ** 2) / (8 * tension_admisible)

    resultados = {
        "Presión Viento pv (N/m²)": round(pv, 2),
        "Carga Horizontal del Viento Pc (N/m)": round(pc, 4),
        "Peso Aparente Viento Pa (N/m)": round(pa, 4),
        "Tensión Horizontal Admisible (N)": round(tension_admisible, 2),
        "Flecha (m)": round(flecha, 4)
    }

    df_resultados = pd.DataFrame({
        "Datos calculados (" + area_nombre + ")": list(resultados.keys()),
        "Valor": list(resultados.values())
    })

    st.markdown(f"### 🔸 Resultados para {area_nombre}")
    st.dataframe(df_resultados, use_container_width=True)

    # Resaltar flecha con estilo personalizado
st.markdown(f"""
<div style='background-color:#fffbe6;padding:10px;border:1px solid #e0d6a3;border-radius:10px'>
    <b>📏 Flecha calculada para {area_nombre}:</b> <span style='font-size:18px;color:#b80000;font-weight:bold'>{flecha:.3f} m</span>
</div>
""", unsafe_allow_html=True)

# Calcular para ambas áreas
calcular_flecha("Área A", viento_areaA_ms)
calcular_flecha("Área B", viento_areaB_ms)
