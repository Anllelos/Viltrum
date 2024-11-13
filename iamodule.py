"""
Install the Google AI Python SDK

$ pip install google-generativeai
"""

import google.generativeai as genai
import time
import requests
import imghdr
import io

def model_config():

    genai.configure(api_key="AIzaSyBdeTO2gxkLt8waX0s1lsSpJdiOkRffadU")

# Create the model
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
        
    )   

    return model


def upload_to_gemini(path, mime_type=None):
  """Uploads the given file to Gemini.

  See https://ai.google.dev/gemini-api/docs/prompting_with_media
  """
  file = genai.upload_file(path, mime_type=mime_type)
  print(f"Uploaded file '{file.display_name}' as: {file.uri}")
  return file

def wait_for_files_active(files):
  """Waits for the given files to be active.

  Some files uploaded to the Gemini API need to be processed before they can be
  used as prompt inputs. The status can be seen by querying the file's "state"
  field.

  This implementation uses a simple blocking polling loop. Production code
  should probably employ a more sophisticated approach.
  """
  print("Waiting for file processing...")
  for name in (file.name for file in files):
    file = genai.get_file(name)
    while file.state.name == "PROCESSING":
      print(".", end="", flush=True)
      time.sleep(10)
      file = genai.get_file(name)
    if file.state.name != "ACTIVE":
      raise Exception(f"File {file.name} failed to process")
  print("...all files ready")
  print()

def llm_promt_engineering_image(identification_photo_url, user_photo_url):
    model = model_config()

    # Descargar las imágenes desde las URL
    response1 = requests.get(identification_photo_url)
    response2 = requests.get(user_photo_url)

    # Verificar que ambas imágenes se descargaron correctamente
    if response1.status_code != 200 or response2.status_code != 200:
        return None  # Si alguna imagen no se descarga correctamente, devuelve None

    # Obtener el tipo MIME de las imágenes
    mime_type1 = imghdr.what(None, h=response1.content)
    mime_type2 = imghdr.what(None, h=response2.content)

    # Mapeo de extensiones que imghdr.what devuelve a tipos MIME reales
    mime_type_map = {
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'png': 'image/png',
        'bmp': 'image/bmp'
    }

    # Convertir lo que devuelve imghdr.what a un MIME real usando el mapeo
    mime_type1 = mime_type_map.get(mime_type1, None)
    mime_type2 = mime_type_map.get(mime_type2, None)

    # Lista de tipos MIME permitidos
    allowed_mime_types = ['image/jpeg', 'image/png', 'image/bmp', 'image/jpg']

    # Verificar si ambos tipos MIME están permitidos
    if mime_type1 not in allowed_mime_types or mime_type2 not in allowed_mime_types:
        return None  # Si alguno no es permitido, retorna None
    
    image1 = io.BytesIO(response1.content)  # Crea un archivo temporal en memoria para la primera imagen
    image2 = io.BytesIO(response2.content)  # Crea un archivo temporal en memoria para la segunda imagen

    files = [
        upload_to_gemini(image1, mime_type=mime_type1),
        upload_to_gemini(image2, mime_type=mime_type2)
    ]

    chat = model.start_chat(
        history = [
            {"role":"user",
            "parts":
            [
            files[0],
            files[1],
            '''
            Buenas noches. Vas a recibir dos imágenes, y tu tarea es determinar si ambas imágenes corresponden a la misma persona y si al menos una de ellas proviene de una identificación oficial. Sigue estos pasos secuenciales para realizar el análisis:
1. Verificación de Identificación:

    Verifica si al menos una de las imágenes es una fotografía de una identificación oficial (por ejemplo, una tarjeta de identificación escaneada o fotografiada).
        Si ninguna de las imágenes es de una identificación, devuelve inmediatamente {"is_verified":"False"} y no continúes con el resto de las verificaciones.

2. Verificación de Diferencias en las Imágenes:

    Asegúrate de que las dos imágenes no sean exactamente iguales.
        Si ambas imágenes son idénticas (por ejemplo, dos fotos normales o dos fotos de la misma identificación), devuelve {"is_verified":"False"}.

3. Verificación Facial:

    Si se pasa la verificación de identificación y las imágenes son diferentes:
        Compara los siguientes rasgos faciales entre las dos imágenes:
            Color, tamaño y forma de los ojos
            Tamaño y forma de la frente
            Color de piel (ten en cuenta posibles variaciones debido a la iluminación)
            Color, tamaño y forma de los labios
            Forma y grosor de las cejas
            Forma del rostro
            Otros rasgos faciales relevantes
        Si las dos imágenes muestran a la misma persona, procede al siguiente paso; de lo contrario, devuelve {"is_verified":"False"}.

4. Resultado Final:

    Si las dos imágenes corresponden a la misma persona y se cumplen todos los requisitos anteriores, devuelve {"is_verified":"True"}.
    Si no se cumplen, devuelve {"is_verified":"False"}.

Devuelve únicamente el resultado en el siguiente formato, sin texto adicional ni cambios en la estructura:

{"is_verified":"(True si ambas imágenes corresponden a la misma persona, una es una identificación, y se cumplen los requisitos; False si no se parecen o no se cumplen los requisitos)"}
            ''']
            },
        ]
    )
    response = chat.send_message("Estas son las dos imagenes a comparar")
    return response.text


def llm_basic(language, phrase):
    model = model_config()
    response = model.generate_content(f"Traduce el siguiente texto al {language}, solo responde con la traducción no agregues ni cambies texto: {phrase}")
    return response.text


