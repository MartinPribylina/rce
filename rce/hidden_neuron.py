class HiddenNeuron():
    def __init__(self, weights, radius):
        """
        Initialize HiddenNeuron with given weights and activation radius.

        :param weights: List of two floats, weights of the neuron.
        :param activation: Float, activation radius of the neuron.
        """
        self.weights = weights
        self.radius = radius
        self.output_neuron = None

    def __str__(self):
        str = "[{}, r={:.2f}, output={}]" .format(self.weights, self.radius, self.output_neuron)
        return str