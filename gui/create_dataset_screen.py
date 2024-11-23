from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QFileDialog, QHBoxLayout, QComboBox
from PyQt5.QtCore import Qt

from data.input_data import InputData
from data.my_exceptions import AlreadyExists
from .styles import get_button_style, get_red_button_style
from .mpl_canvas import MplCanvas
from data.point import Point
import json

class CreateDatasetScreen(QWidget):
    def __init__(self, switch_screen):
        super().__init__()
        self.graph_border = 1.5
        self.switch_screen = switch_screen
        self.input = InputData()

        main_layout = QHBoxLayout()

        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        main_layout.addWidget(self.canvas)

        controls_widget = QWidget()
        controls_widget.setMaximumWidth(200)
        controls_layout = QVBoxLayout()
        controls_widget.setLayout(controls_layout)

        save_button = QPushButton("Save Dataset")
        load_button = QPushButton("Load Dataset")
        back_button = QPushButton("Back")
        save_button.setStyleSheet(get_button_style())
        load_button.setStyleSheet(get_button_style())
        back_button.setStyleSheet(get_button_style())
        general_button_layout = QVBoxLayout()
        general_button_layout.addWidget(save_button)
        general_button_layout.addWidget(load_button)
        general_button_layout.addWidget(back_button)
        controls_layout.addLayout(general_button_layout)

        form_layout = QVBoxLayout()
        form_layout.addWidget(QLabel("Create or remove points"))
        x_layout = QHBoxLayout()
        self.x_input = QLineEdit()
        x_layout.addWidget(QLabel("X:"))
        x_layout.addWidget(self.x_input)
        form_layout.addLayout(x_layout)

        y_layout = QHBoxLayout()
        self.y_input = QLineEdit()
        y_layout.addWidget(QLabel("Y:"))
        y_layout.addWidget(self.y_input)
        form_layout.addLayout(y_layout)

        class_layout = QHBoxLayout()
        self.class_input = QComboBox()
        self.class_input.addItems(["Red", "Green", "Blue", "Cyan", "Magenta", "Black"])
        class_layout.addWidget(QLabel("Class:"))
        class_layout.addWidget(self.class_input)
        form_layout.addLayout(class_layout)

        add_point_button = QPushButton("Add Point")
        add_point_button.setStyleSheet(get_button_style())
        form_layout.addWidget(add_point_button)

        remove_point_button = QPushButton("Remove Point")
        remove_point_button.setStyleSheet(get_red_button_style())
        form_layout.addWidget(remove_point_button)

        controls_layout.addLayout(form_layout)

        main_layout.addWidget(controls_widget)

        self.setLayout(main_layout)

        add_point_button.clicked.connect(self.add_point)
        remove_point_button.clicked.connect(self.remove_point)
        save_button.clicked.connect(self.save_dataset)
        load_button.clicked.connect(self.load_dataset)
        back_button.clicked.connect(lambda: self.switch_screen("main_menu"))

    def add_point(self):
        try:
            x = float(self.x_input.text())
            y = float(self.y_input.text())
            point = Point(x, y, self.class_input.currentText())
            self.input.add_point(point)
            self.canvas.ax.scatter(x, y, color=point.get_color(), label=point.class_name)
            x_values = [point.x for point in self.input.data.values()] if self.input.data else [0]
            y_values = [point.y for point in self.input.data.values()] if self.input.data else [0]
            x_min, x_max = min(x_values) - self.graph_border, max(x_values) + self.graph_border
            y_min, y_max = min(y_values) - self.graph_border, max(y_values) + self.graph_border

            self.canvas.ax.set_xlim(x_min, x_max)
            self.canvas.ax.set_ylim(y_min, y_max)
            self.canvas.draw()

        except AlreadyExists:
            print("Point already exists")
        except ValueError:
            print("Invalid input")

    def remove_point(self):
        try:
            x = float(self.x_input.text())
            y = float(self.y_input.text())
            point_key = f"{x}_{y}"
            if point_key in self.input.data:
                del self.input.data[point_key]
                self.redraw_all_points(self.input.data)
            else:
                print("Point does not exist")

        except ValueError:
            print("Invalid input")

    def redraw_all_points(self, points):
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
