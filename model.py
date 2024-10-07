import os
from pydub import AudioSegment  # Necesario para combinar audios
import requests

class TextBlock:
    def __init__(self, text='', voice='Google (Latin America)', speed='Normal'):
        self.text = text
        self.voice = voice
        self.speed = speed  # Agregar atributo de velocidad

class PodcastModel:
    def __init__(self):
        self.text_blocks = [TextBlock()]  # Inicia con un bloque de texto
        self.available_voices = self.get_available_voices()
        self.max_tts_chars = 200  # Límite de caracteres para Google TTS
        self.speed_map = {
            'Muy lenta': 0.5,  # Desacelerar a la mitad
            'Lenta': 0.8,      # Desacelerar a 80%
            'Normal': 1.0,     # Velocidad normal
            'Rápida': 1.2,     # Acelerar a 120%
            'Muy rápida': 1.5   # Acelerar a 150%
        }

    def get_available_voices(self):
        """Obtiene las voces disponibles para el programa"""
        voices = {
            'Google (Spain)': 'es-ES',  # Código correcto para español de España
            'Google (Latin America)': 'es-419',  # Código para español latino
            'Nueva Voz 1': 'es-CO',  # Ejemplo de nueva voz
            'Nueva Voz 2': 'es-MX'   # Ejemplo de nueva voz
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
                # Ajustar la velocidad del audio
                audio_segment = AudioSegment.from_mp3(temp_file)
                adjusted_audio = audio_segment.speedup(playback_speed=self.speed_map[block.speed])

                # Combinar con el audio final
                if combined_audio is None:
                    combined_audio = adjusted_audio
                else:
                    combined_audio += adjusted_audio

                temp_files.append(temp_file)

        if combined_audio:
            combined_audio.export(file_name, format='mp3')
            print(f"Podcast generado: {file_name}")
        else:
            print("No se generó audio debido a que todos los bloques de texto estaban vacíos.")

        # Eliminar archivos temporales
        for temp_file in temp_files:
            os.remove(temp_file)

    def generate_google_voice_audio(self, text, file_name, voice_code):
        """Genera el audio usando Google TTS y lo guarda en file_name"""
        if len(text) > self.max_tts_chars:
            print(f"El texto excede el límite de {self.max_tts_chars} caracteres para Google TTS.")
            return False

        url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={text}&tl={voice_code}&client=tw-ob"
        response = requests.get(url)

        if response.status_code == 200:
            with open(file_name, 'wb') as f:
                f.write(response.content)
            return True
        else:
            print(f"Error al generar el audio: {response.status_code}")
            return False
