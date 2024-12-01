import json
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QMessageBox, QLabel, QLineEdit
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from data.my_exceptions import AlreadyExists
from gui.mpl_canvas import MplCanvas
from data.input_data import InputData
from rce.rce_trainer import RceTrainer
from .styles import get_button_style, get_font_size_16_style

info_text = "Welcome to RCE training screen!\n1. Load dataset\n2. Train network\n3. Use arrows to step through the training process\n"
info_text += "<<< - skips to first training iteration\n>>> - skips to last training iteration\n<< - skips to beggining of iteration or previous training iteration if currently positioned on first training input\n"
info_text += ">> - skips to end of iteration or next training iteration if currently positioned on last training input\n < - skips to previous training input\n > - skips to next training input"

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

        nav_layout.addWidget(self.build_button("<<<", self.first_iteration))
        nav_layout.addWidget(self.build_button("<<", self.prev_iteration))
        nav_layout.addWidget(self.build_button("<", self.prev_step))
        nav_layout.addWidget(self.build_button(">", self.next_step))
        nav_layout.addWidget(self.build_button(">>", self.next_iteration))
        nav_layout.addWidget(self.build_button(">>>", self.last_iteration))

        main_layout.addLayout(nav_layout)

        # Control buttons layout
        controls_layout = QVBoxLayout()

        load_data_button = self.build_button("Load Data", self.load_data)
        controls_layout.addWidget(load_data_button)

        # Train Network button
        train_network_button = self.build_button("Train Network", self.train_network)
        controls_layout.addWidget(train_network_button)

        # R max input
        train_widget = QWidget()
        train_widget.setMaximumWidth(400)
        train_layout = QHBoxLayout()
        r_max_label = QLabel("R max:", self)
        self.r_input = QLineEdit()
        self.r_input.setText(str(self.r_max))
        train_layout.addWidget(r_max_label)
        train_layout.addWidget(self.r_input)
        train_widget.setLayout(train_layout)
        controls_layout.addWidget(train_widget)

        # Show results
        show_results_button = self.build_button("Show results", self.show_results)
        controls_layout.addWidget(show_results_button)
        # Help button
        help_button = self.build_button("Help", self.showHelp)
        controls_layout.addWidget(help_button)
        # Back button
        back_button = self.build_button("Back", self.goBack)
        controls_layout.addWidget(back_button)

        controls_layout.setAlignment(Qt.AlignTop)

        canvas_info_layout.addLayout(controls_layout)

        # Information label
        self.build_info_label()
        controls_layout.addWidget(self.info_label)

        self.setLayout(main_layout)

    
    def showHelp(self):
        QMessageBox.information(self, "Help", info_text)
    def show_results(self):
        if self.rce_trainer is None:
            QMessageBox.warning(self, "No results", "No trained network yet.")
            return

        last_network = self.rce_trainer.rce_networks[-1]

        # Create HTML formatted output
        output = "<h2>RCE Network</h2>"
        output += "<p><b>Hidden neurons:</b> {}</p>".format(len(last_network.hidden_layer))
        output += "<p><b>Output neurons:</b> {}</p>".format(len(last_network.output_layer))
        output += "<p><b>R max:</b> {}</p>".format(last_network.r_max)

        output += "<h3>Output neurons:</h3>"
        for neuron in last_network.output_layer:
            output += "<p>{}</p>".format(neuron)

        output += "<h3>Hidden neurons:</h3>"
        for neuron in last_network.hidden_layer:
            output += "<p>{}</p>".format(neuron)

        QMessageBox.information(self, "RCE Network", output)


    def build_info_label(self):
        self.info_label = QLabel(info_text, self)
        self.info_label.setAlignment(Qt.AlignTop)
        self.info_label.setStyleSheet("QLabel { background-color : white; border: 1px solid black; }")
        self.info_label.setWordWrap(True)

    def build_button(self, title, function = None):
        button = QPushButton(title, self)
        button.setStyleSheet(get_button_style())
        if function is not None:
            button.clicked.connect(function)
        return button

    def build_progress_info(self):
        progress_info_layout = QVBoxLayout()
        iteration__training_layout = QHBoxLayout()
        self.iteration_label = self.build_label("Iteration: None", alignment = Qt.AlignLeft, style = get_font_size_16_style())
        self.training_vector_label = self.build_label("Training Vector: None", alignment = Qt.AlignLeft, style = get_font_size_16_style())
        self.filename_label = self.build_label("File Name: None", alignment = Qt.AlignLeft, style = get_font_size_16_style())
        self.action_label = self.build_label("Action: None", alignment = Qt.AlignLeft, style = get_font_size_16_style())
        self.comment_label = self.build_label("Comment: None", alignment = Qt.AlignLeft, style = get_font_size_16_style())
        iteration__training_layout.addWidget(self.iteration_label)
        iteration__training_layout.addWidget(self.training_vector_label)
        iteration__training_layout.addWidget(self.filename_label)
        progress_info_layout.addLayout(iteration__training_layout)
        progress_info_layout.addWidget(self.action_label)
        progress_info_layout.addWidget(self.comment_label)
        return progress_info_layout

    def build_label(self, text, alignment = None, style:str = None):
        label = QLabel(text, self)
        if alignment:
            label.setAlignment(alignment)
        if style:
            label.setStyleSheet(style)
        return label

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
                self.filename_label.setText("File Name: {}".format(file_name.split("/")[-1]))
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
            self.canvas.ax.scatter(point.x, point.y, s=80, color=point.class_name)

        
        self.info_label.setText(current_network.__str__())
        # Show neurons
        for neuron in current_network.hidden_layer:
            circle = plt.Circle((neuron.weights[0], neuron.weights[1]), neuron.radius, color=neuron.output_neuron.class_name, fill=False, linewidth=3)
            self.canvas.ax.add_artist(circle)

        if self.rce_current_network_index != len(self.rce_trainer.rce_networks) - 1 and self.rce_current_network_index != 0:
            # Show current action
            if len(current_network.hidden_layer) > 0 and current_network.index_of_hidden_neuron is not None:
                current_hidden_neuron = current_network.hidden_layer[current_network.index_of_hidden_neuron]
                circle = plt.Circle((current_hidden_neuron.weights[0], current_hidden_neuron.weights[1]), current_hidden_neuron.radius, color="yellow", fill=False, linewidth=1)
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

    def first_iteration(self):
        if not self.can_click_arrows():
            return
        self.rce_current_network_index = 0
        self.plot_network()

    def last_iteration(self):
        if not self.can_click_arrows():
            return
        self.rce_current_network_index = len(self.rce_trainer.rce_networks) - 1
        self.plot_network()

    def prev_iteration(self):
        if not self.can_click_arrows():
            return
        current_network = self.rce_trainer.rce_networks[self.rce_current_network_index]
        iteration = current_network.iteration
        if iteration <= 0:
            return

        while self.rce_current_network_index > 0:
            self.rce_current_network_index -= 1
            current_network = self.rce_trainer.rce_networks[self.rce_current_network_index]
            prev_network_same_iteration = False
            if self.rce_current_network_index - 1 >= 0:
                prev_network_same_iteration = self.rce_trainer.rce_networks[self.rce_current_network_index - 1].iteration == current_network.iteration
            if current_network.train_input_index == 0 and current_network.index_of_hidden_neuron == 0 and not prev_network_same_iteration:
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

    def next_iteration(self):
        if not self.can_click_arrows():
            return
        next_iteration = self.rce_trainer.rce_networks[self.rce_current_network_index].iteration + 1
        while self.rce_current_network_index < len(self.rce_trainer.rce_networks) - 1:
            self.rce_current_network_index += 1
            current_network = self.rce_trainer.rce_networks[self.rce_current_network_index]
            if current_network.iteration == next_iteration:
                break
        self.plot_network()

    def goBack(self):
        self.switch_screen("main_menu")
