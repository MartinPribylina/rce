from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QFileDialog, QHBoxLayout, QComboBox, QMessageBox
from PyQt5.QtCore import Qt

from data.input_data import InputData
from data.json_serializer import JsonSerializer
from data.my_exceptions import AlreadyExists
from .styles import get_button_style, get_red_button_style
from .mpl_canvas import MplCanvas
from data.point import Point
import json

class CreateDatasetScreen(QWidget):
    def __init__(self, switch_screen):
        super().__init__()
        self.graph_border_offset = 1.5
        self.switch_screen = switch_screen
        self.input = InputData()
        self.initUI()
    
    def initUI(self):
        main_layout = QHBoxLayout()

        self.canvas = MplCanvas(self)
        main_layout.addWidget(self.canvas)

        controls_widget = QWidget()
        controls_widget.setMaximumWidth(200)
        controls_layout = QVBoxLayout()
        controls_widget.setLayout(controls_layout)

        save_button = self.build_button("Save Dataset", self.save_dataset)
        load_button = self.build_button("Load Dataset", self.load_dataset)
        back_button = self.build_button("Back", lambda: self.switch_screen("main_menu"))
        general_button_layout = QVBoxLayout()
        general_button_layout.addWidget(save_button)
        general_button_layout.addWidget(load_button)
        general_button_layout.addWidget(back_button)
        controls_layout.addLayout(general_button_layout)

        form_layout = QVBoxLayout()
        heading_label = QLabel("Create or remove points")
        heading_label.setWordWrap(True)
        heading_label.setAlignment(Qt.AlignBottom)
        heading_label.setStyleSheet("font-weight: bold; font-size: 24px; padding-bottom: 10px;")
        form_layout.addWidget(heading_label)
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

        add_point_button = self.build_button("Add Point", self.add_point)
        form_layout.addWidget(add_point_button)

        remove_point_button = self.build_button("Remove Point", self.remove_point)
        remove_point_button.setStyleSheet(get_red_button_style())
        form_layout.addWidget(remove_point_button)

        remove_all_points_button = self.build_button("Remove All", self.remove_all_points)
        remove_all_points_button.setStyleSheet(get_red_button_style())
        form_layout.addWidget(remove_all_points_button)

        controls_layout.addLayout(form_layout)

        main_layout.addWidget(controls_widget)

        self.setLayout(main_layout)

    def build_button(self, title, function = None):
        button = QPushButton(title, self)
        button.setStyleSheet(get_button_style())
        if function is not None:
            button.clicked.connect(function)
        return button
    
    def add_point(self):
        """
        Adds a point to the InputData object if it does not already exist.

        Attempts to extract float values from the x and y input fields, and
        the class name from the class name input field. If the point does not
        already exist in the InputData object, it is added and the point is
        plotted on the graph. If the point already exists, a warning message
        is displayed. If the input is invalid, an error message is displayed.

        :return: None
        """
        try:
            x = float(self.x_input.text())
            y = float(self.y_input.text())
            point = Point(x, y, self.class_input.currentText())
            self.input.add_point(point)
            self.canvas.ax.scatter(x, y, color=point.get_color(), label=point.class_name)
            x_values = [point.x for point in self.input.data.values()] if self.input.data else [0]
            y_values = [point.y for point in self.input.data.values()] if self.input.data else [0]
            x_min, x_max = min(x_values) - self.graph_border_offset, max(x_values) + self.graph_border_offset
            y_min, y_max = min(y_values) - self.graph_border_offset, max(y_values) + self.graph_border_offset

            self.canvas.ax.set_xlim(x_min, x_max)
            self.canvas.ax.set_ylim(y_min, y_max)
            self.canvas.draw()

        except AlreadyExists:
            QMessageBox.warning(self, "Warning", "Point already exists!\nPoint {}".format(point))
        except ValueError as e:
            QMessageBox.warning(self, "Warning", "Invalid input: {}".format(e))

    def remove_point(self):
        """
        Removes a point from the InputData object if it exists.

        Attempts to extract float values from the x and y input fields. 
        If the point exists in the InputData object, it is removed and 
        all points are re-plotted on the graph. If the point does not exist, 
        a warning message is displayed. If the input is invalid, an error message 
        is displayed.

        :return: None
        """
        try:
            x = float(self.x_input.text())
            y = float(self.y_input.text())
            point = Point(x, y, self.class_input.currentText())
            removed =self.input.remove_point(point)
            if removed:
                self.redraw_all_points()
            else:
                QMessageBox.warning(self, "Warning", "Point which you are trying to remove does not exist!\nPoint {}".format(point))
        except ValueError as e:
            QMessageBox.warning(self, "Warning", "Invalid input: {}".format(e))

    def remove_all_points(self):
        """
        Removes all points from the InputData.

        :return: None
        """
        self.input.remove_all_points()
        self.redraw_all_points()

    def redraw_all_points(self):
        try:
            self.canvas.ax.cla()
            for _, point in self.input.data.items():
                self.canvas.ax.scatter(point.x, point.y, color=point.get_color(), label=point.class_name)

            self.canvas.draw()
        except Exception:
            print("Invalid input")

    def load_dataset(self):
        """
        Attempts to load a dataset from a JSON file.

        If the dataset contains duplicated points, a warning message is displayed. 
        If the input is invalid, an error message is displayed.

        :return: None
        """
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Load Dataset", "", "JSON Files (*.json);;All Files (*)", options=options)
        try:
            if file_name:
                with open(file_name, 'r') as f:
                    parsed_data = json.loads(f.read())
                    self.input = InputData(parsed_data)
                    self.redraw_all_points()
                print(f"Loaded dataset: {file_name}")
        except AlreadyExists:
            QMessageBox.warning(self, "Warning", "Dataset contains duplicated points!")
        except Exception as e:
            QMessageBox.warning(self, "Warning", "An error occurred while loading the dataset!\nError: {}".format(e))

    def save_dataset(self):
        """
        Saves the current dataset list(Point) to a JSON file.

        :return: None
        """
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Dataset", "", "JSON Files (*.json);;All Files (*)", options=options)
        try:
            if file_name:
                with open(file_name, 'w') as f:
                    jsonSerializer = JsonSerializer()
                    json_output = jsonSerializer.serialize(list(self.input.data.values()))
                    print(json_output)
                    f.write(json_output)

                QMessageBox.information(self, "Saving Finished", f"Dataset successfully saved to {file_name}!")
        except Exception as e:
            QMessageBox.warning(self, "Warning", "An error occurred while saving the dataset!\nError: {}".format(e))
