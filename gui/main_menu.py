from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton

from .styles import get_button_style

class MainMenu(QWidget):
    def __init__(self, switch_screen):
        super().__init__()

        self.switch_screen = switch_screen

        layout = QVBoxLayout()
        layout.setContentsMargins(50, 100, 50, 100)

        self.train_button = QPushButton("Train and Demo RCE Network")
        self.create_dataset_button = QPushButton("Create Training Dataset")

        self.train_button.setStyleSheet(get_button_style())
        self.create_dataset_button.setStyleSheet(get_button_style())

        layout.addWidget(self.train_button)
        layout.addWidget(self.create_dataset_button)

        self.setLayout(layout)

        self.train_button.clicked.connect(lambda: self.switch_screen("train_network"))
        self.create_dataset_button.clicked.connect(lambda: self.switch_screen("create_dataset"))
