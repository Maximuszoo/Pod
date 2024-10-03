from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel, QComboBox, QGridLayout, QProgressBar, QScrollArea, QHBoxLayout
)

class TextBlockWidget(QWidget):
    def __init__(self, text='', voice='', remove_callback=None, parent=None):
        super().__init__(parent)
        self.layout = QGridLayout(self)

        self.text_edit = QTextEdit()
        self.text_edit.setText(text)

        self.voice_combo = QComboBox()
        self.voice_combo.addItems(['Spanish (Spain)', 'Spanish (Latin America)'])
        if voice:
            self.voice_combo.setCurrentText(voice)

        # Botón para eliminar el bloque
        self.remove_button = QPushButton("Eliminar")
        self.remove_button.clicked.connect(remove_callback)

        # Añadir los elementos al layout
        self.layout.addWidget(QLabel('Texto:'), 0, 0)
        self.layout.addWidget(self.text_edit, 0, 1)
        self.layout.addWidget(QLabel('Voz:'), 1, 0)
        self.layout.addWidget(self.voice_combo, 1, 1)
        self.layout.addWidget(self.remove_button, 2, 1)  # Colocar el botón de eliminar


class PodcastView(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)

        self.text_block_widgets = []

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

    def add_text_block_widget(self, text='', voice=''):
        """Agrega un bloque de texto con la opción de eliminarlo"""
        # Definir la función de eliminación para este bloque
        def remove_block():
            widget.deleteLater()
            self.text_block_widgets.remove(widget)
            self.scroll_layout.removeWidget(widget)

        # Crear el nuevo bloque de texto con el callback de eliminación
        widget = TextBlockWidget(text, voice, remove_callback=remove_block)
        self.text_block_widgets.append(widget)
        self.scroll_layout.addWidget(widget)
