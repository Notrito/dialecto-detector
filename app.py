import gradio as gr
import spacy
import json
import random
from collections import Counter

# Cargar modelo
print("Cargando modelo...")
nlp = spacy.load("./model-last")
print("✓ Modelo cargado")

# Función de detección
def detectar_dialectismos(texto):
    doc = nlp(texto)
    colors = {
        "ARGENTINISMO": "#75aadb",  # Azul celeste argentino
        "ESPAÑOLISMO": "#c60b1e"     # Rojo español
    }
    options = {
        "colors": colors
    }
    
    html = spacy.displacy.render(
        doc, 
        style="ent", 
        jupyter=False,
        options=options
    )
    return html

# Ejemplos predefinidos
ejemplos = [
    "Che boludo, ¿vos sabés dónde dejé las llaves del bondi?",
    "Tío, este curro es una mierda, me voy a flipar",
]


# Cargar tweets al inicio (fuera de las funciones)
with open('tweets_sample.json', 'r', encoding='utf-8') as f:
    TODOS_LOS_TWEETS = json.load(f)

def generar_muestra_y_estadisticas():
    """
    Genera muestra de 1000 tweets y retorna estadísticas + la muestra misma
    """
    # Samplear 1000 tweets aleatorios
    muestra = random.sample(TODOS_LOS_TWEETS, min(1000, len(TODOS_LOS_TWEETS)))
    
    # Calcular estadísticas (mismo código de antes)
    total_argentinismos = 0
    total_españolismos = 0
    palabras_arg = []
    palabras_esp = []
    tweets_argentinos = 0
    tweets_españoles = 0
    
    for tweet in muestra:
        argentinismos = tweet['argentinismos']
        españolismos = tweet['españolismos']
        
        total_argentinismos += len(argentinismos)
        total_españolismos += len(españolismos)
        
        palabras_arg.extend(argentinismos)
        palabras_esp.extend(españolismos)
        
        if len(argentinismos) > len(españolismos):
            tweets_argentinos += 1
        elif len(españolismos) > len(argentinismos):
            tweets_españoles += 1
    
    top_arg = Counter(palabras_arg).most_common(10)
    top_esp = Counter(palabras_esp).most_common(10)
    
    # HTML con estadísticas
    html_stats = f"""
    <div style="font-family: Arial, sans-serif; padding: 20px;">
        <h2>📊 Estadísticas de 1000 tweets aleatorios</h2>
        
        <div style="display: flex; gap: 20px; margin: 20px 0;">
            <div style="flex: 1; background: #75aadb; color: white; padding: 20px; border-radius: 10px;">
                <h3>🇦🇷 Argentinismos</h3>
                <p style="font-size: 32px; margin: 10px 0;"><strong>{total_argentinismos}</strong></p>
                <p>detectados en total</p>
                <p style="font-size: 20px;"><strong>{tweets_argentinos}</strong> tweets argentinos</p>
            </div>
            
            <div style="flex: 1; background: #c60b1e; color: white; padding: 20px; border-radius: 10px;">
                <h3>🇪🇸 Españolismos</h3>
                <p style="font-size: 32px; margin: 10px 0;"><strong>{total_españolismos}</strong></p>
                <p>detectados en total</p>
                <p style="font-size: 20px;"><strong>{tweets_españoles}</strong> tweets españoles</p>
            </div>
        </div>
        
        <div style="display: flex; gap: 20px; margin-top: 30px;">
            <div style="flex: 1;">
                <h3>🔝 Top 10 Argentinismos</h3>
                <ol>
                    {"".join(f'<li><strong>{palabra}</strong>: {count} veces</li>' for palabra, count in top_arg)}
                </ol>
            </div>
            
            <div style="flex: 1;">
                <h3>🔝 Top 10 Españolismos</h3>
                <ol>
                    {"".join(f'<li><strong>{palabra}</strong>: {count} veces</li>' for palabra, count in top_esp)}
                </ol>
            </div>
        </div>
    </div>
    """
    
    # Retornar HTML de stats y la muestra para usarla después
    return html_stats, muestra


def obtener_5_tweets_aleatorios(muestra):
    """
    Obtiene 5 tweets aleatorios de la muestra
    """
    if not muestra:
        return gr.Radio(choices=[], label="Primero genera una muestra")
    
    tweets_sample = random.sample(muestra, min(5, len(muestra)))
    
    # Crear lista de opciones (texto truncado para visualización)
    opciones = []
    for i, tweet in enumerate(tweets_sample):
        texto = tweet['text']
        # Truncar si es muy largo
        preview = texto[:100] + "..." if len(texto) > 100 else texto
        opciones.append((preview, texto))  # (label, value)
    
    return gr.Radio(choices=opciones, label="Selecciona un tweet", value=opciones[0][1] if opciones else None)



# Variable global para almacenar la muestra actual
muestra_actual = []

def wrapper_generar_muestra():
    global muestra_actual
    html_stats, muestra_actual = generar_muestra_y_estadisticas()
    return html_stats

def wrapper_5_tweets():
    global muestra_actual
    return obtener_5_tweets_aleatorios(muestra_actual)

# Interfaz Gradio
with gr.Blocks() as demo:
    gr.Markdown("# 🗣️ Detector de Dialecto Español: Argentino 🇦🇷 vs Español 🇪🇸")
    gr.Markdown("Analiza una muestra de 1000 tweets aleatorios del dataset y explora ejemplos individuales.")
    
    # Botón para generar muestra
    btn_generar = gr.Button("🎲 Generar Muestra de 1000 Tweets", variant="primary", size="lg")
    output_stats = gr.HTML()
    
    gr.Markdown("---")
    gr.Markdown("### Explorar ejemplos de la muestra")
    
    # Botón para obtener 5 tweets
    btn_samplear = gr.Button("📋 Mostrar 5 Tweets Aleatorios")
    radio_tweets = gr.Radio(choices=[], label="Selecciona un tweet para analizar")
    
    # Botón para analizar el tweet seleccionado
    btn_analizar = gr.Button("🔍 Analizar Tweet Seleccionado", variant="secondary")
    output_analisis = gr.HTML()
    
    # Eventos
    btn_generar.click(
        fn=wrapper_generar_muestra,
        inputs=None,
        outputs=output_stats
    )
    
    btn_samplear.click(
        fn=wrapper_5_tweets,
        inputs=None,
        outputs=radio_tweets
    )
    
    btn_analizar.click(
        fn=detectar_dialectismos,
        inputs=radio_tweets,
        outputs=output_analisis
    )


if __name__ == "__main__":
    demo.launch()