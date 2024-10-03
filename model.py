# model.py

import os
from pydub import AudioSegment  # Necesario para combinar audios
import requests

class TextBlock:
    def __init__(self, text='', voice='Google (Latin America)'):
        self.text = text
        self.voice = voice

class PodcastModel:
    def __init__(self):
        self.text_blocks = [TextBlock()]  # Inicia con un bloque de texto
        self.available_voices = self.get_available_voices()
        self.max_tts_chars = 200  # Límite de caracteres para Google TTS

    def get_available_voices(self):
        """Obtiene las voces disponibles para el programa"""
        voices = {
            'Google (Spain)': 'es-ES',  # Código correcto para español de España
            'Google (Latin America)': 'es-419'  # Código para español latino
        }
        return voices

    def add_text_block(self):
        """Añade un nuevo bloque de texto"""
        self.text_blocks.append(TextBlock())

    def generate_audio(self, file_name='podcast.mp3'):
        """Genera el archivo de audio combinando todos los bloques de texto"""
        combined_audio = None
        temp_files = []

        # Procesar cada bloque de texto y generar un archivo temporal
        for idx, block in enumerate(self.text_blocks):
            if not block.text.strip():
                print(f"Bloque de texto {idx + 1} está vacío. Se omitirá.")
                continue  # Omitir bloques vacíos

            temp_file = f'temp_{idx}.mp3'
            self.generate_google_voice_audio(block.text, temp_file, block.voice)

            # Verificar si el archivo temporal existe y tiene un tamaño adecuado
            if os.path.exists(temp_file) and os.path.getsize(temp_file) > 1000:  # Tamaño mínimo 1KB
                temp_files.append(temp_file)
            else:
                print(f"Error generando el archivo de audio {temp_file}, se omitirá.")

        # Combinar todos los archivos temporales
        if temp_files:
            combined_audio = AudioSegment.from_file(temp_files[0])  # Cargar el primer archivo
            for temp_file in temp_files[1:]:
                next_audio = AudioSegment.from_file(temp_file)
                combined_audio += next_audio  # Concatenar los audios

            combined_audio.export(file_name, format="mp3")

        # Eliminar archivos temporales
        for temp_file in temp_files:
            os.remove(temp_file)

    def generate_google_voice_audio(self, text, temp_file, voice_code):
        """Genera audio usando la API de Google Translate, dividiendo el texto si es necesario"""
        # Dividir el texto si excede el límite de caracteres
        segments = self.split_text_into_segments(text, self.max_tts_chars)

        combined_audio = AudioSegment.silent(duration=0)  # Inicia con un segmento de audio vacío

        for idx, segment in enumerate(segments):
            # URL de la API de Google Translate
            url = f"http://translate.google.com/translate_tts?ie=UTF-8&q={segment}&tl={voice_code}&client=tw-ob"
            
            # Realizar la solicitud y verificar si la respuesta es exitosa
            response = requests.get(url)
            if response.status_code == 200:
                # Guardar la respuesta en un archivo temporal
                segment_file = f"{temp_file}_part{idx}.mp3"
                with open(segment_file, 'wb') as f:
                    f.write(response.content)
                
                # Combinar el audio descargado
                segment_audio = AudioSegment.from_file(segment_file)
                combined_audio += segment_audio
                
                # Eliminar el archivo temporal de cada segmento
                os.remove(segment_file)
            else:
                print(f"Error: No se pudo obtener el archivo de audio para el segmento '{segment}'. Status code: {response.status_code}")

        # Exportar el archivo combinado
        combined_audio.export(temp_file, format="mp3")

    def split_text_into_segments(self, text, max_chars):
        """Divide el texto en segmentos más pequeños basados en el límite de caracteres"""
        words = text.split()
        segments = []
        current_segment = ""

        for word in words:
            if len(current_segment) + len(word) + 1 <= max_chars:  # +1 para el espacio
                current_segment += (word + " ")
            else:
                segments.append(current_segment.strip())
                current_segment = word + " "

        if current_segment:  # Añadir el último segmento si queda algo
            segments.append(current_segment.strip())

        return segments
