from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QFileDialog, QHBoxLayout, QComboBox
from PyQt5.QtCore import Qt

from data.input_data import InputData
from data.my_exceptions import AlreadyExists
from .styles import get_button_style
from .mpl_canvas import MplCanvas
from data.point import Point
import json

class CreateDatasetScreen(QWidget):
    def __init__(self, switch_screen):
        super().__init__()

        self.switch_screen = switch_screen
        self.input = InputData()

        layout = QVBoxLayout()

        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)

        form_layout = QHBoxLayout()
        self.x_input = QLineEdit()
        self.y_input = QLineEdit()
        self.class_input = QComboBox()
        self.class_input.addItems(["Red", "Green", "Blue"])  # Príklad tried

        self.add_point_button = QPushButton("Add Point")
        self.save_button = QPushButton("Save Dataset")
        self.load_button = QPushButton("Load Dataset")
        self.back_button = QPushButton("Back")

        self.add_point_button.setStyleSheet(get_button_style())
        self.save_button.setStyleSheet(get_button_style())
        self.load_button.setStyleSheet(get_button_style())
        self.back_button.setStyleSheet(get_button_style())

        form_layout.addWidget(QLabel("X:"))
        form_layout.addWidget(self.x_input)
        form_layout.addWidget(QLabel("Y:"))
        form_layout.addWidget(self.y_input)
        form_layout.addWidget(QLabel("Class:"))
        form_layout.addWidget(self.class_input)
        form_layout.addWidget(self.add_point_button)

        layout.addWidget(self.canvas)
        layout.addLayout(form_layout)
        layout.addWidget(self.save_button)
        layout.addWidget(self.load_button)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

        self.add_point_button.clicked.connect(self.add_point)
        self.save_button.clicked.connect(self.save_dataset)
        self.load_button.clicked.connect(self.load_dataset)
        self.back_button.clicked.connect(lambda: self.switch_screen("main_menu"))

    def add_point(self):
        try:
            x = float(self.x_input.text())
            y = float(self.y_input.text())
            point = Point(x, y, self.class_input.currentText())
            self.input.add_point(point)
            self.canvas.ax.scatter(x, y, color=point.get_color(), label=point.class_name)
            self.canvas.draw()
        except AlreadyExists:
            print("Point already exists")
        except ValueError:
            print("Invalid input")

    def redraw_all_points(self, points : dict[str, Point]):
        try:
            self.canvas.ax.cla()
            for key, point in points.items():
                self.canvas.ax.scatter(point.x, point.y, color=point.get_color(), label=point.class_name)
                
            self.canvas.draw()
        except AlreadyExists:
            print("Point already exists")
        except ValueError:
            print("Invalid input")

    def load_dataset(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Load Dataset", "", "JSON Files (*.json);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'r') as f:
                parsed_data = json.loads(f.read())
                self.input = InputData(parsed_data)
                self.redraw_all_points(self.input.data)
            print(f"Loaded dataset: {file_name}")

    def custom_serializer(self, obj):
        if isinstance(obj, InputData):
            return obj.__dict__
        if isinstance(obj, Point):
            return obj.__dict__
        raise TypeError(f"Type {type(obj)} not serializable")

    def save_dataset(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Dataset", "", "JSON Files (*.json);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'w') as f:
                json_str = json.dumps(self.input, default=self.custom_serializer)
                print(json_str)
                f.write(json_str)

            print(f"Dataset saved to {file_name}")
