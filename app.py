import streamlit as st

st.set_page_config(page_title="Calculadora de Flecha - Fase 1", layout="centered")

st.title("🧮 Calculadora de Flecha - Entrada de Datos (Fase 1)")

st.markdown("### 🔌 Datos del Cable")

col1, col2 = st.columns(2)

with col1:
    calibre = st.text_input("Calibre", "6 AWG")
    xlpe_mm = st.number_input("XLPE (mm)", value=1.14)
    tipo_conductor = st.selectbox("Tipo Conductor", ["AAC", "AAAC", "ACSR"])
    carga_rotura_kgf = st.number_input("Carga de Rotura (kgf)", value=255.0)
    diametro_mm = st.number_input("Diámetro total (mm)", value=14.5)
    peso_kg_km = st.number_input("Peso Conductor (kg/km)", value=157.0)
    corriente = st.number_input("Corriente (A)", value=76.0)
    coef_seguridad = st.number_input("Coef. de Seguridad", value=2.0)

with col2:
    # Conversiones automáticas
    carga_rotura_N = carga_rotura_kgf * 9.81
    diametro_m = diametro_mm / 1000
    peso_N_m = (peso_kg_km * 9.81) / 1000

    st.markdown("**🔁 Conversión de Unidades:**")
    st.write(f"**Carga de Rotura (N):** {carga_rotura_N:,.2f}")
    st.write(f"**Diámetro (m):** {diametro_m:.5f}")
    st.write(f"**Peso (N/m):** {peso_N_m:.5f}")

st.divider()
st.markdown("### 🌬️ Condiciones de Entorno")

col3, col4 = st.columns(2)

with col3:
    viento_areaA_kmh = st.number_input("Velocidad Viento (km/h) - Área A", value=115.0)
    viento_areaB_kmh = st.number_input("Velocidad Viento (km/h) - Área B", value=140.0)
    vano_m = st.number_input("Distancia del Vano (m)", value=50.0)

with col4:
    viento_areaA_ms = viento_areaA_kmh / 3.6
    viento_areaB_ms = viento_areaB_kmh / 3.6

    st.markdown("**🔁 Conversión de Unidades:**")
    st.write(f"**Área A (m/s):** {viento_areaA_ms:.2f}")
    st.write(f"**Área B (m/s):** {viento_areaB_ms:.2f}")
