from data.input_data import Point


class HiddenNeuron():
    def __init__(self, weights, activation):
        self.weights = weights
        self.activation = activation
        self.output_neuron = None

    def __str__(self):
        str = "[{}, r={}, output={}]" .format(self.weights, self.activation, self.output_neuron)
        return str

class OutputNeuron():
    def __init__(self, class_name):
        self.class_name = class_name
    
    def __str__(self):
        x = "[{}]" .format(self.class_name)
        return x
    
class RceNetwork():
    def __init__(self, r_max: int = 3):
        self.r_max = r_max
        self.modification = None # Modification flag
        self.train_input_index = 0 # Index of training for dataset
        self.hit = None # Hit flag
        self.index_of_hidden_neuron = 0
        self.hidden_layer : list[HiddenNeuron] = []
        self.output_layer : list[OutputNeuron] = []
        self.iteration = 0
        self.comment = ""
        self.last_action = ""

    def __str__(self):
        output_message = "######################\n"
        output_message += "RCE Network\n"
        output_message += f"iteration: {self.iteration}\n"
        output_message += f"index of train vector: {self.train_input_index}\n"
        output_message += f"index of hidden neuron: {self.index_of_hidden_neuron}\n"
        output_message += f"last action: {self.last_action}\n"
        output_message += f"{self.comment}\n"
        output_message += "----------------------\n"
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
        self.last_action = "Adding new hidden neuron at ({},{}) r = {}" .format(training_point.x, training_point.y, self.r_max)
        new_hidden_neuron = HiddenNeuron([training_point.x, training_point.y], self.r_max)
        self.modification = True
        self.hidden_layer.append(new_hidden_neuron)
        for output_neuron in self.output_layer:
            if output_neuron.class_name == training_point.class_name:
                new_hidden_neuron.output_neuron = output_neuron
                self.last_action += "; Output neuron already existed for class {}" .format(training_point.class_name)
                return
            
        new_output_neuron = OutputNeuron(training_point.class_name)
        new_hidden_neuron.output_neuron = new_output_neuron
        self.output_layer.append(new_output_neuron)
        self.last_action += "; Adding new output neuron {}" .format(new_output_neuron)
        