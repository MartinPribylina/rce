import copy
from rce.rce_network import HiddenNeuron, RceNetwork
from data.point import Point

class RceTrainer:
    def __init__(self):
        """
        Initialize RCE Trainer.

        self.rce_network : RceNetwork = RceNetwork()
            Current RCE network.

        self.rce_networks : list[RceNetwork] = []
            List of all RCE networks created during training. Progression of training.

        self.training_done = False
            Flag indicating if training is done.
        """
        self.rce_network : RceNetwork = RceNetwork()
        self.rce_networks : list[RceNetwork] = []
        self.training_done = False

    def Train(self, training_input: list[Point]):
        """
        Trains rce network. Saves all intermediate results in self.rce_networks.

        Args:
            training_input (list[Point]): List of training points.
        """
        if len(training_input) == 0:
            print("RCE Network: Training dataset is empty!")
            return
        
        self.set_initial_state_for_training()

        # Set modification to True for first iteration
        self.rce_network.modification = True
        # Train until any modification occurs
        while self.rce_network.modification:
            self.rce_network.modification = False
            # Go through all training vectors
            while self.rce_network.train_input_index < len(training_input):
                self.rce_network.hit = False
                # Go through all hidden neurons (hyperspheres) for current training vector
                training_point : Point = training_input[self.rce_network.train_input_index]
                self.rce_network.index_of_hidden_neuron = 0
                self.rce_network.comment = ""
                self.rce_network.last_action = ""
                while self.rce_network.index_of_hidden_neuron < len(self.rce_network.hidden_layer):
                    hidden_neuron : HiddenNeuron = self.rce_network.hidden_layer[self.rce_network.index_of_hidden_neuron]
                    # Calculate distance between training point and hidden neuron
                    distance = self.calculate_distance(training_point, hidden_neuron)

                    # Check if training point is in hidden neuron
                    if distance <= hidden_neuron.activation:
                        # Check if training point class matches hidden neuron class
                        if hidden_neuron.output_neuron.class_name == training_point.class_name:
                            # Classes match - hit = True => no need to create new hidden neuron
                            self.rce_network.hit = True
                            self.rce_network.comment = "Comparing training point {} to hidden neuron {} - hit, class matches".format(training_point, hidden_neuron)
                        else:
                            # Classes don't match - modfiy hidden neuron activation
                            self.rce_network.modification = True
                            self.rce_network.comment = "Comparing training point {} to hidden neuron {} - hit, class doesn't match".format(training_point, hidden_neuron)
                            hidden_neuron.activation = distance / 2
                            self.rce_network.comment += " - updating hiddent neuron to {}" .format(self.rce_network.hidden_layer[self.rce_network.index_of_hidden_neuron])
                    else:
                        self.rce_network.comment = "Comparing training point {} to hidden neuron {} - no hit".format(training_point, hidden_neuron)
                    # Make a copy of current training progress
                    self.rce_networks.append(copy.deepcopy(self.rce_network))
                    self.rce_network.index_of_hidden_neuron += 1
                
                # No sufficient hidden neuron for training point => add new hidden neuron
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

    def set_initial_state_for_training(self):
        """
        Resets the state of the RCE Trainer for a new training session.
        """
        self.rce_network.hidden_layer = []
        self.rce_network.output_layer = []
        self.rce_network.train_input_index = 0
        self.rce_network.index_of_hidden_neuron = 0
        self.rce_network.iteration = 1
        self.rce_network : RceNetwork = RceNetwork()
        self.rce_network.last_action = "No action - new network was created"
        self.rce_networks : list[RceNetwork] = [copy.deepcopy(self.rce_network)]
        self.training_done = False

    def calculate_distance(self, point : Point, hidden_neuron : HiddenNeuron) -> float:
        """
        Calculates the Euclidean distance between a point and a hidden neuron.

        :param point: Point whose distance to the hidden neuron is to be calculated.
        :param hidden_neuron: Hidden neuron whose distance to the point is to be calculated.
        :return: float - The Euclidean distance between the point and the hidden neuron.
        """
        # sqrt(a^2 + b^2)
        return ((point.x - hidden_neuron.weights[0]) ** 2 
                + (point.y - hidden_neuron.weights[1]) ** 2) ** 0.5

    