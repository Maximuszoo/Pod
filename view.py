from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel, QComboBox, QGridLayout, QProgressBar
)

class TextBlockWidget(QWidget):
    def __init__(self, text='', voice='', parent=None):
        super().__init__(parent)
        self.layout = QGridLayout(self)

        self.text_edit = QTextEdit()
        self.text_edit.setText(text)

        self.voice_combo = QComboBox()
        self.voice_combo.addItems(['Google', 'Male'])
        if voice:
            self.voice_combo.setCurrentText(voice)

        self.layout.addWidget(QLabel('Texto:'), 0, 0)
        self.layout.addWidget(self.text_edit, 0, 1)
        self.layout.addWidget(QLabel('Voz:'), 1, 0)
        self.layout.addWidget(self.voice_combo, 1, 1)


class PodcastView(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)

        self.text_block_widgets = []

        # Grid layout para los bloques de texto
        self.grid_layout = QVBoxLayout()
        self.layout.addLayout(self.grid_layout)

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

    def add_text_block_widget(self, text='', voice=''):
        widget = TextBlockWidget(text, voice)
        self.text_block_widgets.append(widget)
        self.grid_layout.addWidget(widget)

