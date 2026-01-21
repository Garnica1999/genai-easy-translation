from google import genai
from google.genai import types # Importante para los tipos de configuración
from flask import Flask, request
import re

app = Flask(__name__)

# Configuración del Cliente
# Nota: Si usas proxy a nivel de sistema, el SDK lo tomará automáticamente.
api_key = "AIzaSyB34UwbdIxL-nKmPZoqegCU5SfEdxRUmo4"
client = genai.Client(api_key=api_key)

@app.route('/translate', methods=['get'])
def translate():
    content = request.args.get('text')
    if not content:
        return "Falta el texto", 400

    language = "es"
    
    # 1. Definimos el System Prompt
    system_instruction = (
        f"You are a professional, authentic translation engine. Only return translations. "
        f"Translate the content to {language} Language. "
        f"Maintain symbols like <Keep This Symbol>."
    )

    # 2. Configuramos los Hiperparámetros y el System Prompt
    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        temperature=0.3,
        top_k=1,
        top_p=1,
        max_output_tokens=2048,
        # Si quieres añadir Safety Settings:
        safety_settings=[
            types.SafetySetting(
                category='HARM_CATEGORY_HARASSMENT',
                threshold='BLOCK_ONLY_HIGH'
            )
        ]
    )

    try:
        # 3. Realizamos la petición
        # Usamos gemini-2.5-flash que es el actual más rápido y capaz
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"<Start>{content}<End>",
            config=config
        )

        trans = response.text

        # Limpieza de etiquetas
        trans = re.sub(r"<Start>|<End>", "", trans).strip()
        
        return trans

    except Exception as e:
        print(f"Error: {e}")
        return f"Error en la traducción: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)