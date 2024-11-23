import copy
from rce.rce_network import HiddenNeuron, RceNetwork
from data.point import Point


class RceTrainer:
    def __init__(self):
        self.rce_network : RceNetwork = RceNetwork()
        self.rce_networks : list[RceNetwork] = []
        self.training_done = False

    def Train(self, training_input: list[Point]):
        if len(training_input) == 0:
            print("RCE Network: Training dataset is empty!")
            return
        for point in training_input:
            print(point.x, point.y, point.class_name)
        # Train starting - reset layers
        self.rce_network.hidden_layer = []
        self.rce_network.output_layer = []
        self.rce_network.train_input_index = 0
        self.rce_network.index_of_hidden_neuron = 0
        self.rce_network.iteration = 1
        self.rce_network : RceNetwork = RceNetwork()
        self.rce_network.last_action = "No action - new network was created"
        self.rce_networks : list[RceNetwork] = [copy.deepcopy(self.rce_network)]
        self.training_done = False

        # Initialize first neuron
        training_point = training_input[self.rce_network.train_input_index]
        self.rce_network.modification = True
        self.rce_network.add_new_neuron(training_point)
        self.rce_network.train_input_index += 1
        self.rce_network.comment = "First hidden neuron was added"
        # Add copy after first neuron
        self.rce_networks.append(copy.deepcopy(self.rce_network))

        # Train until any modification occurs
        while self.rce_network.modification:
            self.rce_network.modification = False
            # Go through all training vectors
            while self.rce_network.train_input_index < len(training_input):
                self.rce_network.hit = False
                # Go through all hidden neurons (hyperspheres)
                training_point : Point = training_input[self.rce_network.train_input_index]
                self.rce_network.index_of_hidden_neuron = 0
                self.rce_network.comment = ""
                self.rce_network.last_action = ""
                while self.rce_network.index_of_hidden_neuron < len(self.rce_network.hidden_layer):
                    hidden_neuron : HiddenNeuron = self.rce_network.hidden_layer[self.rce_network.index_of_hidden_neuron]
                    distance = self.calculate_distance(training_point, hidden_neuron)

                    if distance <= hidden_neuron.activation:
                        if hidden_neuron.output_neuron.class_name == training_point.class_name:
                            self.rce_network.hit = True
                            self.rce_network.comment = "Comparing training point {} to hidden neuron {} - hit, class matches".format(training_point, hidden_neuron)
                        else:
                            self.rce_network.comment = "Comparing training point {} to hidden neuron {} - hit, class doesn't match".format(training_point, hidden_neuron)
                            hidden_neuron.activation = distance / 2
                            self.rce_network.comment += " - updating hiddent neuron to {}" .format(self.rce_network.hidden_layer[self.rce_network.index_of_hidden_neuron])
                            self.rce_network.modification = True
                    else:
                        self.rce_network.comment = "Comparing training point {} to hidden neuron {} - no hit".format(training_point, hidden_neuron)
                    # Make a copy of current training progress
                    self.rce_networks.append(copy.deepcopy(self.rce_network))
                    self.rce_network.index_of_hidden_neuron += 1
                
                if not self.rce_network.hit:
                    self.rce_network.add_new_neuron(training_point)
                    self.rce_network.modification = True
                    self.rce_network.comment = "No sufficient hidden neuron for training point {} - adding new hidden neuron".format(training_point)
                    self.rce_networks.append(copy.deepcopy(self.rce_network))
                
                self.rce_network.train_input_index += 1
            # Reset train_input_index for next iteration if any modification occured
            self.rce_network.train_input_index = 0
            self.rce_network.iteration += 1

        self.training_done = True
        print(self.rce_network)

    def calculate_distance(self, point : Point, hidden_neuron : HiddenNeuron):
        # sqrt(a^2 + b^2)
        return ((point.x - hidden_neuron.weights[0]) ** 2 
                + (point.y - hidden_neuron.weights[1]) ** 2) ** 0.5

    