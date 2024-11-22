import json
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog, QMessageBox, QHBoxLayout
from PyQt5.QtCore import Qt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from rce.rce_network import RceNetwork
from data.input_data import Point, InputData
from rce.rce_trainer import RceTrainer
from .styles import get_button_style

class TrainNetworkScreen(QWidget):
    def __init__(self, switch_screen):
        super().__init__()
        self.switch_screen = switch_screen
        self.rce_trainer = RceTrainer()
        self.rce_current_network_index = 0
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()

        # Matplotlib canvas
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        main_layout.addWidget(self.canvas)

        # Navigation buttons layout
        nav_layout = QHBoxLayout()

        first_epoch_button = QPushButton("<<<", self)
        first_epoch_button.setStyleSheet(get_button_style())
        first_epoch_button.clicked.connect(self.first_epoch)
        nav_layout.addWidget(first_epoch_button)

        prev_epoch_button = QPushButton("<<", self)
        prev_epoch_button.setStyleSheet(get_button_style())
        prev_epoch_button.clicked.connect(self.prev_epoch)
        nav_layout.addWidget(prev_epoch_button)

        prev_step_button = QPushButton("<", self)
        prev_step_button.setStyleSheet(get_button_style())
        prev_step_button.clicked.connect(self.prev_step)
        nav_layout.addWidget(prev_step_button)

        next_step_button = QPushButton(">", self)
        next_step_button.setStyleSheet(get_button_style())
        next_step_button.clicked.connect(self.next_step)
        nav_layout.addWidget(next_step_button)

        next_epoch_button = QPushButton(">>", self)
        next_epoch_button.setStyleSheet(get_button_style())
        next_epoch_button.clicked.connect(self.next_epoch)
        nav_layout.addWidget(next_epoch_button)

        last_epoch_button = QPushButton(">>>", self)
        last_epoch_button.setStyleSheet(get_button_style())
        last_epoch_button.clicked.connect(self.last_epoch)
        nav_layout.addWidget(last_epoch_button)

        main_layout.addLayout(nav_layout)

        # Load Data button
        load_data_button = QPushButton("Load Data", self)
        load_data_button.setStyleSheet(get_button_style())
        load_data_button.clicked.connect(self.load_data)
        main_layout.addWidget(load_data_button)

        # Train Network button
        train_network_button = QPushButton("Train Network", self)
        train_network_button.setStyleSheet(get_button_style())
        train_network_button.clicked.connect(self.train_network)
        main_layout.addWidget(train_network_button)

        # Back button
        back_button = QPushButton("Back", self)
        back_button.setStyleSheet(get_button_style())
        back_button.clicked.connect(self.goBack)
        main_layout.addWidget(back_button)

        self.setLayout(main_layout)

    def load_data(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Load Dataset", "", "JSON Files (*.json);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'r') as f:
                parsed_data = json.loads(f.read())
                self.input = InputData(parsed_data)
            self.training_data = list(self.input.data.values())
            self.plot_data()
            self.rce_trainer = RceTrainer()
            self.rce_current_network_index = 0
            QMessageBox.information(self, "Loading Finished", "Dataset was loaded successfully!")
    
    def plot_data(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        # Get the min and max values for x and y
        x_values = [point.x for point in self.training_data]
        y_values = [point.y for point in self.training_data]
        x_min, x_max = min(x_values) - 3, max(x_values) + 3
        y_min, y_max = min(y_values) - 3, max(y_values) + 3

        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)

        class_colors = {'Red': 'r', 'Blue': 'b', 'Green': 'g'}
        for point in self.training_data:
            ax.scatter(point.x, point.y, color=class_colors.get(point.class_name, 'k'))

        self.canvas.draw()

    def train_network(self):
        if hasattr(self, 'training_data'):
            self.rce_trainer.Train(self.training_data)
            self.rce_current_network_index = 0
            self.plot_network()
            QMessageBox.information(self, "Training Finished", "Training finished succesfully!")
        else:
            QMessageBox.warning(self, "Warning", "No training data loaded!")

    def plot_network(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        # Get the min and max values for x and y
        x_values = [point.x for point in self.training_data]
        y_values = [point.y for point in self.training_data]
        x_min, x_max = min(x_values) - 3, max(x_values) + 3
        y_min, y_max = min(y_values) - 3, max(y_values) + 3

        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)

        class_colors = {'Red': 'r', 'Blue': 'b', 'Green': 'g'}
        for point in self.training_data:
            ax.scatter(point.x, point.y, color=class_colors.get(point.class_name, 'k'))

        current_network = self.rce_trainer.rce_networks[self.rce_current_network_index]
        for neuron in current_network.hidden_layer:
            circle = plt.Circle((neuron.weights[0], neuron.weights[1]), neuron.activation, color=class_colors.get(neuron.output_neuron.class_name, 'k'), fill=False)
            ax.add_artist(circle)

        self.canvas.draw()

    def first_epoch(self):
        if not self.rce_trainer.training_done:
            return
        self.rce_current_network_index = 0
        self.plot_network()

    def last_epoch(self):
        if not self.rce_trainer.training_done:
            return
        self.rce_current_network_index = len(self.rce_trainer.rce_networks) - 1
        print(len(self.rce_trainer.rce_networks))
        print(self.rce_current_network_index)
        self.plot_network()

    def prev_epoch(self):
        if not self.rce_trainer.training_done:
            return
        current_network = self.rce_trainer.rce_networks[self.rce_current_network_index]
        iteration = current_network.iteration
        if iteration <= 0:
            return
        
        while self.rce_current_network_index > 0:
            self.rce_current_network_index -= 1
            current_network = self.rce_trainer.rce_networks[self.rce_current_network_index]
            if current_network.train_input_index == 0:
                break


    def prev_step(self):
        if not self.rce_trainer.training_done:
            return
        if self.rce_current_network_index > 0:
            self.rce_current_network_index -= 1
            self.plot_network()

    def next_step(self):
        if not self.rce_trainer.training_done:
            return
        if self.rce_current_network_index < len(self.rce_trainer.rce_networks) - 1:
            self.rce_current_network_index += 1
            self.plot_network()

    def next_epoch(self):
        if not self.rce_trainer.training_done:
            return
        while self.rce_current_network_index < len(self.rce_trainer.rce_networks) - 1:
            self.rce_current_network_index += 1
            current_network = self.rce_trainer.rce_networks[self.rce_current_network_index]
            if current_network.train_input_index == 0:
                break

    def goBack(self):
        self.switch_screen("main_menu")
