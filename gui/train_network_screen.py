import json
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QMessageBox, QLabel, QLineEdit
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from data.my_exceptions import AlreadyExists
from gui.mpl_canvas import MplCanvas
from data.input_data import InputData
from rce.rce_trainer import RceTrainer
from .styles import get_button_style


class TrainNetworkScreen(QWidget):
    def __init__(self, switch_screen):
        super().__init__()
        self.switch_screen = switch_screen
        self.rce_trainer = None
        self.rce_current_network_index = 0
        self.graph_border_offset = 1.5
        self.r_max = 3
        self.initUI()

    def initUI(self):
        """
        Initializes the user interface for the training screen.

        Sets up the main layout with a Matplotlib canvas for visualizing the network,
        an information label providing instructions, and navigation buttons to control
        the training process. Includes buttons for loading data, training the network,
        and navigating through different iterations of training and individual steps 
        over training points of the training process.
        """
        main_layout = QVBoxLayout()

        # Header
        header_layout = QVBoxLayout()
        header_label = self.build_header()
        header_layout.addWidget(header_label)

        # Progress info
        progress_info_layout = self.build_progress_info()
        header_layout.addLayout(progress_info_layout)

        main_layout.addLayout(header_layout)

        # Matplotlib canvas and information layout
        canvas_info_layout = QHBoxLayout()
        self.canvas = MplCanvas(self)
        canvas_info_layout.addWidget(self.canvas)

        main_layout.addLayout(canvas_info_layout)

        # Navigation buttons
        nav_layout = QHBoxLayout()

        first_epoch_button = self.build_first_epoch_button()
        nav_layout.addWidget(first_epoch_button)

        prev_epoch_button = self.build_prev_epoch_button()
        nav_layout.addWidget(prev_epoch_button)

        prev_step_button = self.build_prev_step_button()
        nav_layout.addWidget(prev_step_button)

        next_step_button = self.build_next_step_button()
        nav_layout.addWidget(next_step_button)

        next_epoch_button = self.build_next_epoch_button()
        nav_layout.addWidget(next_epoch_button)

        last_epoch_button = self.build_last_epoch_button()
        nav_layout.addWidget(last_epoch_button)

        main_layout.addLayout(nav_layout)

        # Control buttons layout
        controls_layout = QVBoxLayout()

        load_data_button = self.build_load_data_button()
        controls_layout.addWidget(load_data_button)

        # Train Network button
        train_network_button = self.build_train_network_button()
        controls_layout.addWidget(train_network_button)

        # R max input
        train_widget = QWidget()
        train_widget.setMaximumWidth(200)
        train_layout = QHBoxLayout()
        r_max_label = QLabel("R max:", self)
        self.r_input = QLineEdit()
        self.r_input.setText(str(self.r_max))
        train_layout.addWidget(r_max_label)
        train_layout.addWidget(self.r_input)
        train_widget.setLayout(train_layout)
        controls_layout.addWidget(train_widget)

        # Back button
        back_button = self.build_back_button()
        controls_layout.addWidget(back_button)

        controls_layout.setAlignment(Qt.AlignTop)

        canvas_info_layout.addLayout(controls_layout)

        # Information label
        self.build_info_label()
        controls_layout.addWidget(self.info_label)

        self.setLayout(main_layout)

    def build_info_label(self):
        self.info_label = QLabel(
            "Welcome to RCE training screen!\n1. Load dataset\n2. Train network\n3. Use arrows to step through the training process\n"
            "<<< - skips to first training iteration\n>>> - skips to last training iteration\n<< - skips to beggining of iteration or previous training iteration if currently positioned on first training input\n"
            ">> - skips to end of iteration or next training iteration if currently positioned on last training input\n < - skips to previous training input\n > - skips to next training input",
            self)
        self.info_label.setAlignment(Qt.AlignTop)
        self.info_label.setStyleSheet("QLabel { background-color : white; border: 1px solid black; }")
        self.info_label.setFixedWidth(200)
        self.info_label.setWordWrap(True)

    def build_back_button(self):
        back_button = QPushButton("Back", self)
        back_button.setStyleSheet(get_button_style())
        back_button.clicked.connect(self.goBack)
        return back_button

    def build_train_network_button(self):
        train_network_button = QPushButton("Train Network", self)
        train_network_button.setStyleSheet(get_button_style())
        train_network_button.clicked.connect(self.train_network)
        return train_network_button

    def build_load_data_button(self):
        load_data_button = QPushButton("Load Data", self)
        load_data_button.setStyleSheet(get_button_style())
        load_data_button.clicked.connect(self.load_data)
        return load_data_button

    def build_last_epoch_button(self):
        last_epoch_button = QPushButton(">>>", self)
        last_epoch_button.setStyleSheet(get_button_style())
        last_epoch_button.clicked.connect(self.last_epoch)
        return last_epoch_button

    def build_next_epoch_button(self):
        next_epoch_button = QPushButton(">>", self)
        next_epoch_button.setStyleSheet(get_button_style())
        next_epoch_button.clicked.connect(self.next_epoch)
        return next_epoch_button

    def build_next_step_button(self):
        next_step_button = QPushButton(">", self)
        next_step_button.setStyleSheet(get_button_style())
        next_step_button.clicked.connect(self.next_step)
        return next_step_button

    def build_prev_step_button(self):
        prev_step_button = QPushButton("<", self)
        prev_step_button.setStyleSheet(get_button_style())
        prev_step_button.clicked.connect(self.prev_step)
        return prev_step_button

    def build_prev_epoch_button(self):
        prev_epoch_button = QPushButton("<<", self)
        prev_epoch_button.setStyleSheet(get_button_style())
        prev_epoch_button.clicked.connect(self.prev_epoch)
        return prev_epoch_button

    def build_first_epoch_button(self):
        first_epoch_button = QPushButton("<<<", self)
        first_epoch_button.setStyleSheet(get_button_style())
        first_epoch_button.clicked.connect(self.first_epoch)
        return first_epoch_button

    def build_progress_info(self):
        progress_info_layout = QVBoxLayout()
        self.iteration_label = QLabel("Iteration: None", self)
        self.iteration_label.setAlignment(Qt.AlignLeft)
        self.training_vector_label = QLabel("Training Vector: None", self)
        self.training_vector_label.setAlignment(Qt.AlignLeft)
        self.action_label = QLabel("Action: None", self)
        self.action_label.setAlignment(Qt.AlignLeft)
        self.comment_label = QLabel("Comment: None", self)
        self.comment_label.setAlignment(Qt.AlignLeft)
        progress_info_layout.addWidget(self.iteration_label)
        progress_info_layout.addWidget(self.training_vector_label)
        progress_info_layout.addWidget(self.action_label)
        progress_info_layout.addWidget(self.comment_label)
        return progress_info_layout

    def build_header(self):
        header_label = QLabel("RCE Network", self)
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("QLabel { font-size: 18pt; }")
        return header_label

    def load_data(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Load Dataset", "", "JSON Files (*.json);;All Files (*)", options=options)

        try:
            if file_name:
                with open(file_name, 'r') as f:
                    parsed_data = json.loads(f.read())
                    self.input = InputData(parsed_data)
                    self.training_data = list(self.input.data.values())
                self.info_label.setText("Dataset loaded successfully!\nReady for training.")
                QMessageBox.information(self, "Loading Finished", "Dataset was loaded successfully!")
                self.train_network()
        except AlreadyExists:
            QMessageBox.warning(self, "Warning", "Dataset contains duplicated points!")
        except Exception as e:
            QMessageBox.warning(self, "Warning", "An error occurred while loading the dataset!\nError: {}".format(e))

    def train_network(self):
        if hasattr(self, 'training_data'):
            r_max = self.r_max
            try:
                new_r_max = float(self.r_input.text())
                if new_r_max > 0:
                    r_max = new_r_max
            except Exception:
                QMessageBox.warning(self, "Warning", "Invalid input for r_max: {}".format(self.r_input.text()) + "\nUsing default value!")
            self.rce_trainer = RceTrainer(r_max)
            self.rce_trainer.Train(self.training_data)
            self.rce_current_network_index = 0
            self.plot_network()
            self.info_label.setText("Training finished successfully!")
            QMessageBox.information(self, "Training Finished", "Training finished successfully!")
        else:
            QMessageBox.warning(self, "Warning", "No training data loaded!")

    def plot_network(self):
        self.canvas.ax.cla()

        current_network = self.rce_trainer.rce_networks[self.rce_current_network_index]
        last_network = self.rce_trainer.rce_networks[len(self.rce_trainer.rce_networks) - 1]
        self.iteration_label.setText("Training Iteration: {}/{}".format(current_network.iteration, last_network.iteration))
        self.training_vector_label.setText("Training Vector: {}/{}".format(current_network.train_input_index, len(self.input.data.values()) - 1))
        self.comment_label.setText("Comment: {}".format(self.rce_trainer.rce_networks[self.rce_current_network_index].comment))
        self.action_label.setText("Action: {}".format(self.rce_trainer.rce_networks[self.rce_current_network_index].action))
        # Get the min and max values for x and y
        x_values = [point.x for point in self.training_data]
        y_values = [point.y for point in self.training_data]
        x_min, x_max = min(x_values) - self.graph_border_offset, max(x_values) + self.graph_border_offset
        y_min, y_max = min(y_values) - self.graph_border_offset, max(y_values) + self.graph_border_offset

        self.canvas.ax.set_xlim(x_min, x_max)
        self.canvas.ax.set_ylim(y_min, y_max)

        for point in self.training_data:
            self.canvas.ax.scatter(point.x, point.y, color=point.class_name)

        
        self.info_label.setText(current_network.__str__())
        for neuron in current_network.hidden_layer:
            circle = plt.Circle((neuron.weights[0], neuron.weights[1]), neuron.activation, color=neuron.output_neuron.class_name, fill=False, linewidth=2)
            self.canvas.ax.add_artist(circle)

        if len(current_network.hidden_layer) > 0 and current_network.index_of_hidden_neuron is not None:
            current_hidden_neuron = current_network.hidden_layer[current_network.index_of_hidden_neuron]
            circle = plt.Circle((current_hidden_neuron.weights[0], current_hidden_neuron.weights[1]), current_hidden_neuron.activation, color="yellow", fill=False, linewidth=1)
            self.canvas.ax.add_artist(circle)

        current_input = list(self.input.data.values())[current_network.train_input_index if current_network.train_input_index is not None else 0]
        self.canvas.ax.scatter(current_input.x, current_input.y, s=15, color="yellow")

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
