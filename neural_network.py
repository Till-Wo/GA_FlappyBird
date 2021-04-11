import numpy as np
import pickle
import random
biases_active = False


def sigmoid(X):  # Wichtig nochmal anschauen da ich die Fktion noch nicht ganz verstehe
    return 1 / (1 + np.exp([-x for x in X]))


def softmax(inputs):
    exp_values = np.exp(inputs - max(inputs))
    total = sum(exp_values)
    value = [x / total for x in exp_values]
    return value


def softmax_linear(inputs):
    inputs = inputs[0]
    total = sum(inputs)
    value = [x / total for x in inputs]
    return value



class Layer:
    def __init__(self, n_inputs, n_neurons):
        self.weights = np.random.randn(n_inputs, n_neurons)
        self.n_inputs = n_inputs
        self.n_neurons = n_neurons
        if biases_active:
            self.biases = np.random.randn(1, n_neurons)[0]
        else:
            self.biases = np.zeros((1, n_neurons))

    def forward(self, inputs):
        self.output = np.dot(inputs, self.weights) + self.biases


class Network:
    def __init__(self, n_inputs, n_outputs):
        self.layers = []
        hidden = Layer(n_inputs, 4)
        self.layers.append(hidden)
        output = Layer(self.layers[-1].n_neurons, n_outputs)
        self.layers.append(output)

    def predict(self, network_input):
        inputs = network_input
        for layer in self.layers:
            inputs = sigmoid(inputs)
            layer.forward(inputs)
            inputs = layer.output
        return inputs[0]

    def mutate(self, strength=0.1, learning_rate=0.1):
        for i in range(len(self.layers)):
            for l in range(len(self.layers[i].weights)):
                if random.random() < strength:
                    self.layers[i].weights[l] += (2*random.random()-1)*learning_rate

            if biases_active:

                for l in range(len(self.layers[i].biases)):
                    if random.random() < strength:
                        self.layers[i].biases[l] += (2*random.random()-1)*learning_rate


    def get_flatted(self):
        weights_and_biases = []
        for i in range(len(self.layers)):
            for l in range(len(self.layers[i].weights)):
                for j in range(len(self.layers[i].weights[l])):
                    weights_and_biases.append(self.layers[i].weights[l][j])

            for l in range(len(self.layers[i].biases)):
                weights_and_biases.append(self.layers[i].biases[l])
        return weights_and_biases

    def get_unflattend(self):
        weights = []
        for i in range(len(self.layers)):
            weights.append([])
            for l in range(len(self.layers[i].weights)):
                weights[i].append(self.layers[i].weights[l].tolist())
        return weights

    def set_weights(self, weights_and_biases):
        index = 0
        for i in range(len(self.layers)):
            for l in range(len(self.layers[i].weights)):
                for j in range(len(self.layers[i].weights[l])):
                    self.layers[i].weights[l][j] = weights_and_biases[index]
                    index+=1
            for l in range(len(self.layers[i].biases)):
                self.layers[i].biases[l] = weights_and_biases[index]
                index += 1



    def save(self, path):
        with open(path, 'wb') as fp:
            pickle.dump(self.get_flatted(), fp)


    def load(self, path):
        with open(path, 'rb') as fp:
            itemlist = pickle.load(fp)
        self.set_weights(itemlist)

