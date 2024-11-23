class OutputNeuron():
    def __init__(self, class_name):
        """
        Initialize OutputNeuron with a given class name.

        :param class_name: The class name associated with the output neuron.
        """
        self.class_name = class_name
    
    def __str__(self):
        x = "[{}]" .format(self.class_name)
        return x