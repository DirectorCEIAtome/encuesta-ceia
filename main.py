import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- 1. CONFIGURACIÓN VISUAL Y ESTÉTICA ---
st.set_page_config(page_title="Gestión CEIA Tomé", page_icon="📊", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #001f3f; }
    h1, h2, h3, h4, label, .stSlider, p { color: #00d4ff !important; font-family: 'Arial Black', sans-serif; }
    .stSelectbox, .stTextArea, [data-baseweb="select"] { background-color: #003366 !important; border: 1px solid #00d4ff; border-radius: 8px; }
    .stButton>button { background-color: #00d4ff; color: #001f3f; font-weight: bold; border-radius: 20px; width: 100%; border: none; height: 3.5em; }
    .stButton>button:hover { background-color: #ffffff; color: #001f3f; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ENCABEZADO INSTITUCIONAL ---
col1, col2 = st.columns([1, 4])
ruta_actual = os.path.dirname(os.path.abspath(__file__))

with col1:
    # Buscador de logo flexible
    for f in os.listdir(ruta_actual):
        if f.lower().startswith("logo") or f.startswith("WhatsApp"):
            st.image(os.path.join(ruta_actual, f), width=160)
            break

with col2:
    st.write("# CEIA POETA ALFONSO MORA DE TOMÉ")
    st.write("### Instrumento de Evaluación de Clima Escolar y Convivencia EPJA")

st.markdown("---")

# --- 3. FORMULARIO ELABORADO ---
with st.form("encuesta_tecnica", clear_on_submit=True):
    
    # SECCIÓN A: CARACTERIZACIÓN
    st.subheader("I. Caracterización del Estudiante")
    c1, c2 = st.columns(2)
    with c1:
        jornada = st.selectbox("Jornada de Clases:", ["Mañana", "Tarde", "Noche"])
    with c2:
        curso = st.selectbox("Nivel Educativo Actual:", [
            "1er Nivel Básico (1° a 4° Básico)",
            "2do Nivel Básico (5° y 6° Básico)",
            "3er Nivel Básico (7° y 8° Básico)",
            "1er Ciclo Media (1° y 2° Medio HC)",
            "2do Ciclo Media (3° y 4° Medio HC)"
        ])

    st.markdown("---")
    
    # SECCIÓN B: DIMENSIONES TÉCNICAS
    st.subheader("II. Dimensión: Relaciones y Respeto Institucional")
    st.write("Esta sección evalúa el cumplimiento del Artículo 2° de la LGE sobre el desarrollo ético y moral.")
    
    p1 = st.select_slider(
        "1. ¿Siente que sus profesores y el personal del CEIA valoran su experiencia de vida y lo tratan con dignidad?",
        options=["Nunca", "Rara vez", "Frecuentemente", "Siempre"]
    )
    
    st.subheader("III. Dimensión: Seguridad y Protección (RICE)")
    p2 = st.radio(
        "2. ¿Cómo evalúa la capacidad del establecimiento para resolver conflictos de forma justa y sin discriminación?",
        ["Insuficiente", "Regular", "Buena", "Excelente"]
    )

    st.subheader("IV. Dimensión: Pertenencia y Bienestar")
    p3 = st.select_slider(
        "3. ¿Qué tan orgulloso/a se siente de pertenecer a la comunidad del CEIA Poeta Alfonso Mora?",
        options=["Nada orgulloso/a", "Poco orgulloso/a", "Orgulloso/a", "Muy orgulloso/a"]
    )

    st.subheader("V. Propuestas Directivas")
    propuesta = st.text_area("Desde su perspectiva, ¿cuál es la mejora más urgente que el Director debería implementar para fortalecer la convivencia?")

    enviar = st.form_submit_button("REGISTRAR EVALUACIÓN INSTITUCIONAL")

# --- 4. PROCESAMIENTO DE DATOS ---
if enviar:
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
    datos = {
        "Fecha": fecha, "Jornada": jornada, "Curso": curso, 
        "Dignidad": p1, "Justicia_Conflictos": p2, 
        "Pertenencia": p3, "Sugerencia_Director": propuesta
    }
    
    # Guardar en CSV
    df = pd.DataFrame([datos])
    archivo_csv = os.path.join(ruta_actual, 'datos_gestion_ceia.csv')
    
    if not os.path.isfile(archivo_csv):
        df.to_csv(archivo_csv, index=False, encoding='utf-8-sig')
    else:
        df.to_csv(archivo_csv, mode='a', header=False, index=False, encoding='utf-8-sig')
    
    st.success("✅ Su evaluación ha sido registrada exitosamente. Esta información será utilizada para la mejora continua de nuestro CEIA.")
    st.balloons()