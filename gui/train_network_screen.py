import json
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog, QMessageBox, QHBoxLayout, QLabel
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
        self.graph_border = 1.5
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()

        # Matplotlib canvas and information layout
        canvas_info_layout = QHBoxLayout()

        # Matplotlib canvas
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        canvas_info_layout.addWidget(self.canvas)

        # Information label
        self.info_label = QLabel("Welcome to RCE training screen!\n1. Load dataset\n2. Train network\n3. Use arrows to step through the training process\n<<< - skips to first training iteration\n>>> - skips to last training iteration\n<< - skips to beggining of iteration or previous training iteration if currently positioned on first training input\n>> - skips to end of iteration or next training iteration if currently positioned on last training input\n < - skips to previous training input\n > - skips to next training input", self)
        self.info_label.setAlignment(Qt.AlignTop)
        self.info_label.setStyleSheet("QLabel { background-color : white; border: 1px solid black; }")
        self.info_label.setMaximumWidth(200)
        self.info_label.setWordWrap(True)
        canvas_info_layout.addWidget(self.info_label)

        main_layout.addLayout(canvas_info_layout)

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
            self.info_label.setText("Dataset loaded successfully!\nReady for training.")
            QMessageBox.information(self, "Loading Finished", "Dataset was loaded successfully!")
            self.train_network()
    
    def plot_data(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        # Get the min and max values for x and y
        x_values = [point.x for point in self.training_data]
        y_values = [point.y for point in self.training_data]
        x_min, x_max = min(x_values) - self.graph_border, max(x_values) + self.graph_border
        y_min, y_max = min(y_values) - self.graph_border, max(y_values) + self.graph_border

        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)

        for point in self.training_data:
            ax.scatter(point.x, point.y, color=point.class_name)

        self.canvas.draw()

    def train_network(self):
        if hasattr(self, 'training_data'):
            self.rce_trainer.Train(self.training_data)
            self.rce_current_network_index = 0
            self.plot_network()
            self.info_label.setText("Training finished successfully!")
            QMessageBox.information(self, "Training Finished", "Training finished successfully!")
        else:
            QMessageBox.warning(self, "Warning", "No training data loaded!")

    def plot_network(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        # Get the min and max values for x and y
        x_values = [point.x for point in self.training_data]
        y_values = [point.y for point in self.training_data]
        x_min, x_max = min(x_values) - self.graph_border, max(x_values) + self.graph_border
        y_min, y_max = min(y_values) - self.graph_border, max(y_values) + self.graph_border

        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)

        for point in self.training_data:
            ax.scatter(point.x, point.y, color=point.class_name)

        current_network = self.rce_trainer.rce_networks[self.rce_current_network_index]
        self.info_label.setText(current_network.__str__())
        for neuron in current_network.hidden_layer:
            circle = plt.Circle((neuron.weights[0], neuron.weights[1]), neuron.activation, color=neuron.output_neuron.class_name, fill=False, linewidth=2)
            ax.add_artist(circle)
        
        if len(current_network.hidden_layer) > 0 and current_network.index_of_hidden_neuron is not None:
            current_hidden_neuron = current_network.hidden_layer[current_network.index_of_hidden_neuron]
            circle = plt.Circle((current_hidden_neuron.weights[0], current_hidden_neuron.weights[1]), current_hidden_neuron.activation, color="yellow", fill=False, linewidth=1)
            ax.add_artist(circle)

        current_input = list(self.input.data.values())[current_network.train_input_index if current_network.train_input_index is not None else 0]
        ax.scatter(current_input.x, current_input.y, s=15, color="yellow")

        self.canvas.draw()

    def can_click_arrows(self) -> bool:
        if not hasattr(self, 'training_data'):
            QMessageBox.warning(self, "Warning", "Please load data first!")
            return False
        if not self.rce_trainer.training_done:
            QMessageBox.warning(self, "Warning", "Please train model first!")
            return False
        return True
    def first_epoch(self):
        if not self.can_click_arrows():
            return
        self.rce_current_network_index = 0
        self.plot_network()

    def last_epoch(self):
        if not self.can_click_arrows():
            return
        self.rce_current_network_index = len(self.rce_trainer.rce_networks) - 1
        self.plot_network()

    def prev_epoch(self):
        if not self.can_click_arrows():
            return
        current_network = self.rce_trainer.rce_networks[self.rce_current_network_index]
        iteration = current_network.iteration
        if iteration <= 0:
            return
        
        while self.rce_current_network_index > 0:
            self.rce_current_network_index -= 1
            current_network = self.rce_trainer.rce_networks[self.rce_current_network_index]
            if current_network.train_input_index == 0 and current_network.index_of_hidden_neuron == 0:
                break
        self.plot_network()

    def prev_step(self):
        if not self.can_click_arrows():
            return
        if self.rce_current_network_index > 0:
            self.rce_current_network_index -= 1
            self.plot_network()

    def next_step(self):
        if not self.can_click_arrows():
            return
        if self.rce_current_network_index < len(self.rce_trainer.rce_networks) - 1:
            self.rce_current_network_index += 1
            self.plot_network()

    def next_epoch(self):
        if not self.can_click_arrows():
            return
        while self.rce_current_network_index < len(self.rce_trainer.rce_networks) - 1:
            self.rce_current_network_index += 1
            current_network = self.rce_trainer.rce_networks[self.rce_current_network_index]
            if current_network.train_input_index == 0 and current_network.index_of_hidden_neuron == 0:
                break
        self.plot_network()

    def goBack(self):
        self.switch_screen("main_menu")
