import streamlit as st
import pandas as pd
from textblob import TextBlob # REQUIERE: pip install textblob
import re
from googletrans import Translator # REQUIERE: pip install googletrans

# Configuración de la página
st.set_page_config(
    page_title="Analizador de Texto Simple",
    page_icon="📊",
    layout="wide"
)

# Título y descripción
st.title("📝 Analizador de Texto con TextBlob")
st.markdown("""
Esta aplicación utiliza TextBlob para realizar un análisis básico de texto, traduciendo previamente el contenido a inglés para mejorar la precisión del modelo:
- Análisis de sentimiento (Positivo, Negativo, Neutral)
- Medición de la subjetividad (Opinión vs. Hecho)
- Análisis de frecuencia de palabras clave
""")

# Barra lateral
st.sidebar.title("Opciones")
modo = st.sidebar.selectbox(
    "Selecciona el modo de entrada:",
    ["Texto directo", "Archivo de texto"]
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
        st.error(f"Error al traducir (googletrans): {e}")
        return texto # Devolver el texto original si falla la traducción

# Función para procesar el texto con TextBlob (versión con traducción)
def procesar_texto(texto):
    # Guardar el texto original
    texto_original = texto
    
    # Traducir el texto al inglés para mejor análisis con TextBlob
    texto_ingles = traducir_texto(texto)
    
    # Analizar el texto traducido con TextBlob
    blob = TextBlob(texto_ingles)
    
    # Análisis de sentimiento
    sentimiento = blob.sentiment.polarity
    subjetividad = blob.sentiment.subjectivity
    
    # Extracción de frases
    frases_originales = [frase.strip() for frase in re.split(r'[.!?]+', texto_original) if frase.strip()]
    frases_traducidas = [frase.strip() for frase in re.split(r'[.!?]+', texto_ingles) if frase.strip()]
    
    # Combinar frases originales y traducidas
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
    
    # Visualización de sentimiento y subjetividad
    with col1:
        st.subheader("Análisis de Sentimiento y Subjetividad")
        
        # Sentimiento normalizado (rango -1 a 1 -> 0 a 1)
        sentimiento_norm = (resultados["sentimiento"] + 1) / 2
        
        st.write("**Sentimiento:**")
        st.progress(sentimiento_norm)
        
        if resultados["sentimiento"] > 0.05:
            st.success(f"📈 Positivo ({resultados['sentimiento']:.2f})")
        elif resultados["sentimiento"] < -0.05:
            st.error(f"📉 Negativo ({resultados['sentimiento']:.2f})")
        else:
            st.info(f"📊 Neutral ({resultados['sentimiento']:.2f})")
        
        # Subjetividad (rango 0 a 1)
        st.write("**Subjetividad:**")
        st.progress(resultados["subjetividad"])
        
        if resultados["subjetividad"] > 0.5:
            st.warning(f"💭 Alta subjetividad ({resultados['subjetividad']:.2f})")
        else:
            st.info(f"📋 Baja subjetividad ({resultados['subjetividad']:.2f})")
    
    # Palabras más frecuentes
    with col2:
        st.subheader("Palabras más frecuentes (en inglés)")
        if resultados["contador_palabras"]:
            # Convertir el diccionario a DataFrame para bar_chart
            df_palabras = pd.DataFrame(
                list(resultados["contador_palabras"].items())[:10], 
                columns=['Palabra', 'Frecuencia']
            )
            # Usar 'Palabra' como índice para el gráfico
            df_palabras = df_palabras.set_index('Palabra')
            st.bar_chart(df_palabras)
    
    # Mostrar texto traducido
    st.subheader("Traducción y Análisis Detallado")
    with st.expander("Ver texto original y traducción"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Texto Original:**")
            st.text(resultados["texto_original"])
        with col2:
            st.markdown("**Texto Traducido (Inglés):**")
            st.text(resultados["texto_traducido"])
    
    # Análisis de frases
    st.subheader("Análisis de las primeras 10 frases")
    if resultados["frases"]:
        for i, frase_dict in enumerate(resultados["frases"][:10], 1):
            frase_original = frase_dict["original"]
            frase_traducida = frase_dict["traducido"]
            
            try:
                # Re-analizar el sentimiento de la frase individual
                blob_frase = TextBlob(frase_traducida)
                sentimiento = blob_frase.sentiment.polarity
                
                if sentimiento > 0.05:
                    emoji = "😊"
                elif sentimiento < -0.05:
                    emoji = "😟"
                else:
                    emoji = "😐"
                
                st.write(f"**{i}. {emoji}** **Original:** *\"{frase_original}\"*")
                st.write(f"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Traducción:** *\"{frase_traducida}\"* (Sentimiento: {sentimiento:.2f})")
                st.write("---")
            except:
                st.write(f"**{i}. ❓** **Original:** *\"{frase_original}\"*")
                st.write(f"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Traducción:** *\"{frase_traducida}\"* (Error de análisis)")
                st.write("---")
    else:
        st.write("No se detectaron frases.")

# Lógica principal según el modo seleccionado
if modo == "Texto directo":
    st.subheader("Ingresa tu texto para analizar")
    texto = st.text_area("", height=200, placeholder="Escribe o pega aquí el texto que deseas analizar (funciona mejor con textos en español, inglés o la mayoría de idiomas comunes)...")
    
    if st.button("Analizar texto"):
        if texto.strip():
            with st.spinner("Analizando y traduciendo texto..."):
                resultados = procesar_texto(texto)
                crear_visualizaciones(resultados)
        else:
            st.warning("Ingrese texto para análisis.")

elif modo == "Archivo de texto":
    st.subheader("Carga un archivo de texto")
    archivo = st.file_uploader("", type=["txt", "csv", "md"])
    
    if archivo is not None:
        try:
            # Leer el contenido del archivo
            contenido = archivo.getvalue().decode("utf-8")
            
            with st.expander("Ver contenido del archivo"):
                st.text(contenido[:1000] + ("..." if len(contenido) > 1000 else ""))
            
            if st.button("Analizar archivo"):
                with st.spinner("Analizando y traduciendo archivo..."):
                    resultados = procesar_texto(contenido)
                    crear_visualizaciones(resultados)
        except Exception as e:
            st.error(f"Error al procesar el archivo: {e}")

# Información adicional
with st.expander("📚 Información sobre el análisis y dependencias"):
    st.markdown("""
    ### Sobre el análisis de texto
    
    - **Sentimiento**: Varía de -1 (muy negativo) a 1 (muy positivo).
    - **Subjetividad**: Varía de 0 (muy objetivo, basado en hechos) a 1 (muy subjetivo, basado en opiniones).
    
    ### Dependencias requeridas
    
    Este código utiliza librerías externas que deben estar instaladas en el entorno:
    ```bash
    pip install streamlit pandas textblob googletrans
    ```
    """)
