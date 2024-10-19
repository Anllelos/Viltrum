"""
Install the Google AI Python SDK

$ pip install google-generativeai
"""

import google.generativeai as genai
import time
import imghdr
import os
from pathlib import Path

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

    dir = str(os.path.dirname(os.path.abspath(__file__)))
    print("------------Dir", dir)
    identification_photo_url = str(Path(identification_photo_url))
    print("--------------Identification", identification_photo_url)
    user_photo_url = str(Path(user_photo_url))
    print("--------------Foto", user_photo_url)


    identification_photo_path = dir + identification_photo_url
    user_photo_path = dir + user_photo_url
    

    mime_type1 = imghdr.what(identification_photo_path)
    mime_type2 = imghdr.what(user_photo_path)

# Mapeo de extensiones que imghdr.what devuelve a tipos MIME reales
    mime_type_map = {
      'jpg': 'image/jpg',
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
        return None

    files = [
      upload_to_gemini(identification_photo_path, mime_type=mime_type1),
      upload_to_gemini(user_photo_path, mime_type=mime_type2)
  ]

    chat = model.start_chat(
        history = [
            {"role":"user",
            "parts":
            [
            files[0],
            files[1],
            '''
            Buenas noches. Vas a recibir dos imágenes y debes determinar si ambas pertenecen a la misma persona. 

            Considera los siguientes rasgos faciales en tu análisis:
            - Color, tamaño y forma de los ojos
            - Tamaño y forma de la frente
            - Color de piel (ten en cuenta que esto puede variar según la iluminación)
            - Color, tamaño y forma de los labios
            - Forma y grosor de las cejas
            - Forma de la cara
            - Otros rasgos faciales relevantes

            Por favor, devuelve el resultado en el siguiente formato, 
            sin texto adicional como, ni cambios en la estructura, ni ```json
            {"is_verified":"X"}
            ``` solo el texto que te muestro a continuación:
            {"is_verified":"(True si la persona es la misma o False si no se parecen en nada)"}
            ''']
            },
        ]
    )
    response = chat.send_message("Estas son las dos imagenes a comparar")
    return response.text


def llm_basic(language, phrase):
    model = model_config()
    response = model.generate_content(f"Traduce el siguiente texto al {language}, solo responde con la traducción: {phrase}")
    return response.text


