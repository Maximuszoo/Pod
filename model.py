from gtts import gTTS
import pyttsx3
import os
from pydub import AudioSegment  # Necesario para combinar audios

class TextBlock:
    def __init__(self, text='', voice='Google'):
        self.text = text
        self.voice = voice

class PodcastModel:
    def __init__(self):
        self.text_blocks = [TextBlock()]  # Inicia con un bloque de texto
        self.available_voices = self.get_available_voices()

    def get_available_voices(self):
        """Obtiene las voces disponibles para el programa"""
        voices = {'Google': 'es', 'Male': 'es-us'}
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
            if block.voice == 'Google':
                tts = gTTS(text=block.text, lang=self.available_voices[block.voice])
                tts.save(temp_file)
            else:
                engine = pyttsx3.init()
                engine.setProperty('voice', block.voice)
                engine.save_to_file(block.text, temp_file)
                engine.runAndWait()

            temp_files.append(temp_file)

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

