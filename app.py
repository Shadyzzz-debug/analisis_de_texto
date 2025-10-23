import streamlit as st
import pandas as pd
from textblob import TextBlob # REQUIERE: pip install textblob
import re
from googletrans import Translator # REQUIERE: pip install googletrans

# --- CSS GÓTICO: PALETA BLOODBORNE ---
gothic_css = """
<style>
/* Paleta Gótica: Fondo #0A0A0A, Texto #F5F5DC, Acento/Sangre #8B0000, Metal #6B5B3E */
.stApp {
    background-color: #0A0A0A;
    color: #F5F5DC;
    font-family: 'Georgia', serif;
}

/* Título Principal (h1): Cincelado, Dramático y GRANDE */
h1 {
    color: #8B0000; /* Rojo sangre */
    text-shadow: 3px 3px 8px #000000;
    font-size: 3.5em; /* Aumentado */
    border-bottom: 7px double #6B5B3E; /* Borde más grueso */
    padding-bottom: 15px;
    margin-bottom: 40px;
    text-align: center;
    letter-spacing: 3px;
}

/* Subtítulos (h2, h3): Menos prominentes, color de metal */
h2, h3 {
    color: #D4D4D4;
    font-family: 'Georgia', serif;
    letter-spacing: 1px;
}

/* Sidebar: Fondo de cámara oscura con bordes intrincados */
[data-testid="stSidebar"] {
    background-color: #1A1A1A;
    color: #F5F5DC;
    border-right: 3px solid #6B5B3E;
    box-shadow: 0 0 15px rgba(107, 91, 62, 0.5), inset 0 0 5px rgba(0, 0, 0, 0.8);
}

/* Botones (Forjar, Iniciar): Botones tipo Sello/Relicario */
.stButton > button {
    background-color: #444444; /* Base metálica */
    color: #F5F5DC;
    border: 3px solid #8B0000; /* Borde rojo sangre */
    border-radius: 8px;
    padding: 12px 25px;
    font-weight: bold;
    box-shadow: 6px 6px 10px #000000, inset 0 0 10px rgba(255, 255, 255, 0.1);
    transition: background-color 0.3s, box-shadow 0.3s, transform 0.1s;
}

.stButton > button:hover {
    background-color: #8B0000; /* Hover a rojo intenso */
    color: white;
    box-shadow: 8px 8px 15px #000000;
    transform: translateY(-2px);
}

/* Alertas y Contenedores de Texto */
div[data-testid="stAlert"] {
    background-color: #1A1A1A !important;
    border: 2px solid #6B5B3E !important;
    color: #F5F5DC !important;
    font-family: 'Georgia', serif;
    box-shadow: 0 0 10px rgba(139, 0, 0, 0.5);
}

/* Texto de Expander (Cofres de conocimiento) */
div[data-testid="stExpander"] {
    border: 1px solid #6B5B3E !important;
    border-radius: 6px;
    margin-top: 15px;
    background-color: #151515;
}
div[data-testid="stExpander"] > div:first-child > div:first-child {
    font-size: 1.2em;
    font-weight: bold;
    color: #F5F5DC;
}

/* Gráficos y progreso */
.stProgress > div > div > div > div {
    background-color: #8B0000; /* Color de progreso rojo sangre */
}

/* Texto de estado (success, warning, error) */
.stSuccess { background-color: #330000; color: #F5F5DC; border-left: 5px solid #8B0000; }
.stWarning { background-color: #333300; color: #F5F5DC; border-left: 5px solid #6B5B3E; }
.stError { background-color: #550000; color: #F5F5DC; border-left: 5px solid #FF4B4B; }
</style>
"""
st.markdown(gothic_css, unsafe_allow_html=True)

# Configuración de la página
st.set_page_config(
    page_title="El Escudriñador de Papiro Perdido",
    page_icon="👁️",
    layout="wide"
)

# Título y descripción GÓTICA
st.title("El Escudriñador de Papiro Perdido")
st.markdown("""
### **El Oráculo del Verbo**
Este artefacto utiliza la [TextBlob] y la [Traducción Mística] para desentrañar la esencia emocional de cualquier escrito:
- **Polaridad del Alma:** El sentir oculto, de la Calamidad (-1) a la Éxtasis (+1).
- **Naturaleza del Escrito:** La medida de su subjetividad (Opinión vs. Verdad Absoluta).
- **Frecuencias de Runas Clave:** Las palabras que portan el mayor peso en el códice.
""")

# Barra lateral GÓTICA
st.sidebar.title("Protocolo del Oráculo")
modo = st.sidebar.selectbox(
    "Selecciona el Modo de Inscripción:",
    ["Inscripción en el Altar", "Carga del Códice (Archivo)"]
)

# Función para contar palabras sin depender de NLTK
def contar_palabras(texto):
    # Lista básica de palabras vacías en español e inglés
    stop_words = set([
        "a", "al", "algo", "algunas", "algunos", "ante", "antes", "como", "con", "contra",
        "cual", "cuando", "de", "del", "desde", "donde", "durante", "e", "el", "ella",
        "ellas", "ellos", "en", "entre", "era", "eras", "es", "esa", "esas", "ese",
        "eso", "esos", "esta", "estas", "este", "esto", "estos", "ha", "había", "han",
        "has", "hasta", "he", "la", "las", "le", "les", "lo", "los", "me", "mi", "mía",
        "mías", "mío", "míos", "mis", "mucho", "muchos", "muy", "nada", "ni", "no", "nos",
        "nosotras", "nosotros", "nuestra", "nuestras", "nuestro", "nuestros", "o", "os", 
        "otra", "otras", "otro", "otros", "para", "pero", "poco", "por", "porque", "que", 
        "quien", "quienes", "qué", "se", "sea", "sean", "según", "si", "sido", "sin", 
        "sobre", "sois", "somos", "son", "soy", "su", "sus", "suya", "suyas", "suyo", 
        "suyos", "también", "tanto", "te", "tenéis", "tenemos", "tener", "tengo", "ti", 
        "tiene", "tienen", "todo", "todos", "tu", "tus", "tuya", "tuyas", "tuyo", "tuyos", 
        "tú", "un", "una", "uno", "unos", "vosotras", "vosotros", "vuestra", "vuestras", 
        "vuestro", "vuestros", "y", "ya", "yo",
        # Inglés
        "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", 
        "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being", 
        "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't", 
        "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during", 
        "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have", 
        "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", 
        "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", 
        "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", 
        "let's", "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", 
        "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours", 
        "ourselves", "out", "over", "own", "same", "shan't", "she", "she'd", "she'll", 
        "she's", "should", "shouldn't", "so", "some", "such", "than", "that", "that's", 
        "the", "their", "theirs", "them", "themselves", "then", "there", "there's", 
        "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", 
        "through", "to", "too", "under", "until", "up", "very", "was", "wasn't", "we", 
        "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's", "when", 
        "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", 
        "why's", "with", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've",
        "your", "yours", "yourself", "yourselves"
    ])
    
    # Limpiar y tokenizar texto
    palabras = re.findall(r'\b\w+\b', texto.lower())
    
    # Filtrar palabras vacías y contar frecuencias
    palabras_filtradas = [palabra for palabra in palabras 
                          if palabra not in stop_words and len(palabra) > 2]
    
    # Contar frecuencias
    contador = {}
    for palabra in palabras_filtradas:
        contador[palabra] = contador.get(palabra, 0) + 1
    
    # Ordenar por frecuencia
    contador_ordenado = dict(sorted(contador.items(), key=lambda x: x[1], reverse=True))
    
    return contador_ordenado, palabras_filtradas

# Inicializar el traductor
translator = Translator()

# Función para traducir texto (detecta idioma, traduce a inglés)
def traducir_texto(texto):
    try:
        # Detecta automáticamente el idioma de origen y traduce a inglés
        traduccion = translator.translate(texto, dest='en')
        return traduccion.text
    except Exception as e:
        st.error(f"❌ Fracaso de la Tradición Mística: {e}. Se utiliza el texto original.")
        return texto

# Función para procesar el texto con TextBlob (versión con traducción)
def procesar_texto(texto):
    texto_original = texto
    
    # Traducir el texto al inglés
    texto_ingles = traducir_texto(texto)
    
    # Analizar el texto traducido con TextBlob
    blob = TextBlob(texto_ingles)
    
    sentimiento = blob.sentiment.polarity
    subjetividad = blob.sentiment.subjectivity
    
    # Extracción de frases
    frases_originales = [frase.strip() for frase in re.split(r'[.!?]+', texto_original) if frase.strip()]
    frases_traducidas = [frase.strip() for frase in re.split(r'[.!?]+', texto_ingles) if frase.strip()]
    
    frases_combinadas = []
    for i in range(min(len(frases_originales), len(frases_traducidas))):
        frases_combinadas.append({
            "original": frases_originales[i],
            "traducido": frases_traducidas[i]
        })
    
    # Contar palabras
    contador_palabras, palabras = contar_palabras(texto_ingles)
    
    return {
        "sentimiento": sentimiento,
        "subjetividad": subjetividad,
        "frases": frases_combinadas,
        "contador_palabras": contador_palabras,
        "palabras": palabras,
        "texto_original": texto_original,
        "texto_traducido": texto_ingles
    }

# Función para crear visualizaciones usando componentes nativos de Streamlit
def crear_visualizaciones(resultados):
    col1, col2 = st.columns(2)
    
    # Análisis de Sentimiento y Subjetividad (Polaridad del Alma)
    with col1:
        st.subheader("I. La Esencia Oculta")
        
        # Sentimiento normalizado
        sentimiento_norm = (resultados["sentimiento"] + 1) / 2
        
        st.write("#### **Polaridad del Alma (Sentimiento):**")
        st.progress(sentimiento_norm)
        
        if resultados["sentimiento"] > 0.05:
            st.success(f"✨ Éxtasis Ascendente (Positivo: {resultados['sentimiento']:.2f})")
        elif resultados["sentimiento"] < -0.05:
            st.error(f"💀 Calamidad inminente (Negativo: {resultados['sentimiento']:.2f})")
        else:
            st.info(f"🌫️ Silencio Observante (Neutral: {resultados['sentimiento']:.2f})")
        
        # Subjetividad
        st.write("#### **Naturaleza del Escrito (Subjetividad):**")
        st.progress(resultados["subjetividad"])
        
        if resultados["subjetividad"] > 0.5:
            st.warning(f"💭 Alta Creencia Personal (Subjetivo: {resultados['subjetividad']:.2f})")
        else:
            st.info(f"📜 Baja Interpretación (Objetivo: {resultados['subjetividad']:.2f})")
    
    # Palabras más frecuentes (Frecuencias de Runas Clave)
    with col2:
        st.subheader("II. Frecuencias de Runas Clave")
        if resultados["contador_palabras"]:
            st.markdown("Las 10 runas más potentes del Códice (en su forma traducida):")
            df_palabras = pd.DataFrame(
                list(resultados["contador_palabras"].items())[:10], 
                columns=['Runa', 'Poder']
            )
            df_palabras = df_palabras.set_index('Runa')
            st.bar_chart(df_palabras)
        else:
             st.warning("No hay runas detectadas para calcular frecuencias.")
    
    # Mostrar texto traducido
    st.markdown("---")
    st.subheader("III. El Eco del Manuscrito Traducido")
    with st.expander("Revelar el Texto Completo (Original y Místico)"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**El Papiro Inicial (Original):**")
            st.text(resultados["texto_original"])
        with col2:
            st.markdown("**La Traducción Mística (Inglés):**")
            st.text(resultados["texto_traducido"])
    
    # Análisis de frases
    st.subheader("IV. Fragmentos de la Revelación (Análisis Detallado)")
    st.caption("Cada fragmento es escudriñado por su Polaridad.")
    if resultados["frases"]:
        for i, frase_dict in enumerate(resultados["frases"][:10], 1):
            frase_original = frase_dict["original"]
            frase_traducida = frase_dict["traducido"]
            
            try:
                blob_frase = TextBlob(frase_traducida)
                sentimiento = blob_frase.sentiment.polarity
                
                if sentimiento > 0.05:
                    emoji = "✨" # Éxtasis
                    color = "green"
                elif sentimiento < -0.05:
                    emoji = "💀" # Calamidad
                    color = "red"
                else:
                    emoji = "🌫️" # Silencio
                    color = "orange"
                
                st.markdown(f"""
                <div style="background-color: #1A1A1A; padding: 10px; border-radius: 5px; margin-bottom: 5px; border-left: 3px solid #6B5B3E;">
                    <p style="color: #F5F5DC; font-size: 1.1em;">
                        {i}. {emoji} **Original:** *"{frase_original}"*
                    </p>
                    <p style="color: #D4D4D4; font-size: 0.9em;">
                        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Traducción:** *"{frase_traducida}"* (<span style="color: {color};">Polaridad: {sentimiento:.2f}</span>)
                    </p>
                </div>
                """, unsafe_allow_html=True)
            except:
                st.markdown(f"{i}. ❓ **Original:** *\"{frase_original}\"*")
                st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Traducción:** *\"{frase_traducida}\"* (Error Místico)")
                st.write("---")
    else:
        st.warning("El velo es demasiado denso. No se detectaron fragmentos.")

# Lógica principal según el modo seleccionado
if modo == "Inscripción en el Altar":
    st.subheader("Inscribe el Ritual en el Papiro")
    texto = st.text_area("", height=200, placeholder="Escribe aquí el grimorio que deseas desentrañar...", key="altar_input")
    
    if st.button("🔥 Forjar el Análisis Rúnico"):
        if texto.strip():
            with st.spinner("Desentrañando los velos de la verdad y traduciendo la lengua arcana..."):
                resultados = procesar_texto(texto)
                crear_visualizaciones(resultados)
        else:
            st.warning("⚠️ El Altar está vacío. Se requiere una inscripción.")

elif modo == "Carga del Códice (Archivo)":
    st.subheader("Carga un pergamino (Archivo .txt, .csv, o .md)")
    archivo = st.file_uploader("", type=["txt", "csv", "md"])
    
    if archivo is not None:
        try:
            contenido = archivo.getvalue().decode("utf-8")
            
            with st.expander("Inspeccionar el contenido del Códice"):
                st.text(contenido[:1000] + ("..." if len(contenido) > 1000 else ""))
            
            if st.button("🗝️ Iniciar el Ritual de Archivo"):
                with st.spinner("Desentrañando los velos de la verdad y traduciendo la lengua arcana..."):
                    resultados = procesar_texto(contenido)
                    crear_visualizaciones(resultados)
        except Exception as e:
            st.error(f"❌ Error al profanar el Códice: {e}")

# Información adicional GÓTICA
st.markdown("---")
with st.expander("🕯️ Advertencia y Dependencias Arcanas"):
    st.markdown("""
    Este artefacto depende de la magia de las librerías externas:
    
    - **Polaridad y Subjetividad** provienen de `textblob`.
    - **La Traducción Mística** (necesaria para el análisis) es cortesía de `googletrans`.
    
    Asegúrate de que estas runas estén correctamente invocadas (`pip install streamlit pandas textblob googletrans`).
    """)

