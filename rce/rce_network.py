from data.input_data import Point
from rce.hidden_neuron import HiddenNeuron
from rce.output_neuron import OutputNeuron

class RceNetwork():
    def __init__(self, r_max: int = 3):
        """
        Initialize RCE Network with given maximum radius.

        :param r_max: Maximum radius of all hidden neurons. Default value is 3.
        """
        self.r_max = r_max
        self.modification = False # Modification flag
        self.train_input_index = 0 # Index of training for dataset
        self.hit = None # Hit flag
        self.index_of_hidden_neuron = 0
        self.hidden_layer : list[HiddenNeuron] = []
        self.output_layer : list[OutputNeuron] = []
        self.iteration = 0
        self.comment = ""
        self.action = ""

    def __str__(self):
        output_message = "######################\n"
        output_message += "RCE Network\n"
        output_message += f"iteration: {self.iteration}\n"
        output_message += f"index of train vector: {self.train_input_index}\n"
        output_message += f"index of hidden neuron: {self.index_of_hidden_neuron}\n"
        output_message += f"action: {self.action}\n"
        output_message += f"{self.comment}\n"
        output_message += "----------------------\n"
        output_message += f"r_max: {self.r_max}\n"
        output_message += f"neurons in hidden layer: {len(self.hidden_layer)}\n"
        output_message += f"neurons in output layer: {len(self.output_layer)}\n"
        output_message += f"change in network: {self.modification}\n"
        output_message += f"hit flag: {self.hit}\n"
        output_message += "hidden layer: "
        for i, item in enumerate(self.hidden_layer):
            output_message += "{}, " .format(item)
        output_message += "\n"    
        output_message += "output layer: "
        for i, item in enumerate(self.output_layer):   
            output_message += "{}, " .format(item)
        output_message += "\n"
        output_message += "######################\n"
        return output_message
            
    def add_new_neuron(self, training_point : Point):
        """
        Adds a new hidden neuron to the network at the location of the given training point
        with max radius. If an output neuron for the class of the training point already
        exists in the network, it is assigned to the new hidden neuron. If not, a new output neuron
        is created and added to the network and assigned to the new hidden neuron.

        :param training_point: The location of the new hidden neuron.
        """
        self.action = "Adding new hidden neuron at ({},{}) r = {}" .format(training_point.x, training_point.y, self.r_max)
        new_hidden_neuron = HiddenNeuron([training_point.x, training_point.y], self.r_max)
        self.modification = True
        self.hidden_layer.append(new_hidden_neuron)

        # Check if an output neuron for the class of the training point already exists
        for output_neuron in self.output_layer:
            if output_neuron.class_name == training_point.class_name:
                new_hidden_neuron.output_neuron = output_neuron
                self.action += "; Output neuron already existed for class {}" .format(training_point.class_name)
                return
        
        # Output neuron for class does not exist, create a new one
        new_output_neuron = OutputNeuron(training_point.class_name)
        new_hidden_neuron.output_neuron = new_output_neuron
        self.output_layer.append(new_output_neuron)
        self.action += "; Adding new output neuron {}" .format(new_output_neuron)
        