"""
Install the Google AI Python SDK

$ pip install google-generativeai
"""

import os
import google.generativeai as genai

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

def llm_basic(phrase):
    model = model_config()
    response = model.generate_content(f"Traduce el siguiente texto al japonés, solo responde con la traducción: {phrase}")
    return response.text


