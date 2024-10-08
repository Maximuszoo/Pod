from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel, QComboBox, QGridLayout, QProgressBar, QScrollArea, QHBoxLayout, QLineEdit, QFileDialog
)

class TextBlockWidget(QWidget):
    def __init__(self, text='', voice='Google (Latin America)', speed='Normal', remove_callback=None, parent=None):
        super().__init__(parent)
        self.layout = QGridLayout(self)

        self.text_edit = QTextEdit()
        self.text_edit.setText(text)

        self.voice_combo = QComboBox()
        self.voice_combo.addItems(['Google (Spain)', 'Google (Latin America)'])  # Nombres modificados
        if voice:
            self.voice_combo.setCurrentText(voice)

        self.speed_combo = QComboBox()
        self.speed_combo.addItems(['Muy lenta', 'Lenta', 'Normal', 'Rápida', 'Muy rápida'])  # Opciones de velocidad
        self.speed_combo.setCurrentText(speed)

        # Botón para eliminar el bloque
        self.remove_button = QPushButton("Eliminar")
        self.remove_button.clicked.connect(remove_callback)

        # Añadir los elementos al layout
        self.layout.addWidget(QLabel('Texto:'), 0, 0)
        self.layout.addWidget(self.text_edit, 0, 1)
        self.layout.addWidget(QLabel('Voz:'), 1, 0)
        self.layout.addWidget(self.voice_combo, 1, 1)
        self.layout.addWidget(QLabel('Velocidad:'), 2, 0)
        self.layout.addWidget(self.speed_combo, 2, 1)
        self.layout.addWidget(self.remove_button, 3, 1)

class PodcastView(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)

        self.text_block_widgets = []

        # Campo de entrada para el título del podcast
        self.title_label = QLabel("Título del Podcast:")
        self.title_edit = QLineEdit(self)
        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.title_edit)

        # Campo de entrada para la ruta de guardado
        self.save_path_label = QLabel("Ruta de guardado:")
        self.save_path_edit = QLineEdit(self)
        self.layout.addWidget(self.save_path_label)
        self.layout.addWidget(self.save_path_edit)

        # Botón para seleccionar la ruta de guardado
        self.browse_button = QPushButton("Seleccionar carpeta")
        self.layout.addWidget(self.browse_button)

        # ScrollArea para los bloques de texto
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)

        # Widget interno para la ScrollArea
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_area.setWidget(self.scroll_widget)

        # Agregar la ScrollArea al layout principal
        self.layout.addWidget(self.scroll_area)

        # Botón para agregar un nuevo bloque de texto
        self.add_text_block_button = QPushButton("Agregar bloque de texto")
        self.layout.addWidget(self.add_text_block_button)

        # Barra de progreso
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setValue(0)  # Valor inicial en 0%
        self.layout.addWidget(self.progress_bar)

        # Botón para generar el podcast
        self.generate_audio_button = QPushButton("Generar Podcast")
        self.layout.addWidget(self.generate_audio_button)

        # Label para mostrar el estado del programa
        self.status_label = QLabel("No iniciado")
        self.layout.addWidget(self.status_label)

        self.setMinimumSize(800, 200)  # Establece un ancho mínimo y un alto mínimo en píxeles

    def add_text_block_widget(self, text='', voice='Google (Latin America)', speed='Normal'):
        """Agrega un bloque de texto con la opción de eliminarlo"""
        def remove_block():
            widget.deleteLater()
            self.text_block_widgets.remove(widget)
            self.scroll_layout.removeWidget(widget)

        widget = TextBlockWidget(text, voice, speed, remove_callback=remove_block)
        self.text_block_widgets.append(widget)
        self.scroll_layout.addWidget(widget)

    def get_save_path(self):
        """Devuelve la ruta de guardado actual ingresada por el usuario"""
        return self.save_path_edit.text()

    def open_save_dialog(self):
        """Abre un cuadro de diálogo para seleccionar la carpeta de guardado"""
        folder = QFileDialog.getExistingDirectory(self, "Seleccionar carpeta de guardado")
        if folder:
            self.save_path_edit.setText(folder)
