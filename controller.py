from PyQt5.QtCore import QObject, QTimer
from PyQt5.QtWidgets import QMessageBox
from model import PodcastModel
from view import PodcastView

class PodcastController(QObject):
    def __init__(self, model, view):
        super().__init__()
        self.model = model
        self.view = view

        # Conectar los botones a las funciones del controlador
        self.view.add_text_block_button.clicked.connect(self.add_text_block)
        self.view.generate_audio_button.clicked.connect(self.generate_podcast)
        self.view.browse_button.clicked.connect(self.select_save_folder)

        # Inicializar con el primer bloque de texto
        self.view.add_text_block_widget()

    def add_text_block(self):
        """Añade un nuevo bloque de texto tanto en el modelo como en la vista"""
        self.model.add_text_block()
        self.view.add_text_block_widget()

    def select_save_folder(self):
        """Abre el cuadro de diálogo para seleccionar la carpeta de guardado"""
        self.view.open_save_dialog()

    def generate_podcast(self):
        """Genera el podcast y actualiza la barra de progreso"""
        title = self.view.title_edit.text()
        save_path = self.view.get_save_path()

        # Verificar si la ruta de guardado está vacía
        if not save_path:
            self.show_warning("Debe seleccionar o ingresar una ruta de guardado antes de generar el podcast.")
            return

        if not title:
            title = "podcast"  # Nombre por defecto si no se ingresa un título

        file_name = f"{save_path}/{title}.mp3"
        self.view.status_label.setText("Creando podcast...")
        total_blocks = len(self.view.text_block_widgets)
        self.view.progress_bar.setMaximum(total_blocks)
        progress = 0

        for idx, widget in enumerate(self.view.text_block_widgets):
            text = widget.text_edit.toPlainText()
            voice = widget.voice_combo.currentText()
            speed = widget.speed_combo.currentText()  # Obtener la velocidad seleccionada

            # Asignar los valores del texto, voz y velocidad en el modelo
            self.model.text_blocks[idx].text = text
            self.model.text_blocks[idx].voice = self.model.available_voices[voice]
            self.model.text_blocks[idx].speed = speed

            # Simular procesamiento con un temporizador (o realizar el procesamiento real)
            QTimer.singleShot(1000 * (idx + 1), lambda: self.update_progress(idx + 1, total_blocks))

        # Generar el audio con los bloques de texto y sus respectivas voces y velocidades
        self.model.generate_audio(file_name)
        self.view.status_label.setText("Podcast terminado")

    def update_progress(self, progress, total_blocks):
        """Actualiza la barra de progreso según el progreso actual"""
        self.view.progress_bar.setValue(progress)
        if progress == total_blocks:
            self.view.status_label.setText("Podcast terminado")

    def show_warning(self, message):
        """Muestra un cuadro de advertencia con el mensaje proporcionado"""
        warning_box = QMessageBox()
        warning_box.setIcon(QMessageBox.Warning)
        warning_box.setWindowTitle("Advertencia")
        warning_box.setText(message)
        warning_box.setStandardButtons(QMessageBox.Ok)
        warning_box.exec_()
