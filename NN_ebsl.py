import random
import math

# placeholder = network[0][input, layer, output][neuron]
# weights     = network[1][gap between layers(strating at 0)][end neuron][start neuron/ input]
# biases      = network[2][layer][wich neuron (starting at 0)]
# fitness     = network[3]


def sigmoid(x):
    return 1 / (1 + math.e ** -x)


def create_network(num_inputs, num_layer, neurons_pro_layer, num_outputs):
    # network[0] = placeholders for calculation, network[1] = weights, network[2] = biases, network[3] = fitness score
    network = []
    # from here on creates placeholders for the network
    # creates input placeholder
    network.append([[]])
    for innput in range(num_inputs):
        network[0][0].append(0)

    # creates neuron placholder
    for layer in range(num_layer):
        network[0].append([])
        for neuron in range(neurons_pro_layer):
            network[0][1 + layer].append(0)

    # creates output placehpolders
    network[0].append([])
    for output in range(num_outputs):
        network[0][num_layer + 1].append(0)

    # from here on it creates all weights for the network
    # network[1][gap between (input)layers(strating at 0)][end neuron][start neuron/ input]
    # sets random weights from the inputs to first layer
    network.append([[]])
    for neuron in range(neurons_pro_layer):
        network[1][0].append([])
        for innput in range(num_inputs):
            network[1][0][neuron].append(random.gauss(0, 0.5))
            # network[1][0][neuron].append(2)

    # sets random weights inbetween layers
    for gap in range(1, num_layer):
        network[1].append([])
        for end_neuron in range(neurons_pro_layer):
            network[1][gap].append([])
            for startneuron in range(neurons_pro_layer):
                network[1][gap][end_neuron].append(random.gauss(0, 0.5))

    # sets random weights from the last layer to outputs
    network[1].append([])
    for output in range(num_outputs):
        network[1][num_layer].append([])
        for neuron in range(neurons_pro_layer):
            network[1][num_layer][output].append(random.gauss(0, 0.5))

    # from here on it creates all biases for the Network
    # network[2][layer][wich neuron (starting at 0)]
    # sets biases for all neurons
    network.append([])
    for layer in range(num_layer):
        network[2].append([])
        for neuron in range(neurons_pro_layer):
            # network[2][layer].append(random.gauss(0, 0.5))
            network[2][layer].append(0)

    # sets all biases for the outputlayer
    network[2].append([])
    for output in range(num_outputs):
        # network[2][num_layer].append(random.gauss(0, 0.5))
        network[2][num_layer].append(0)

    # appends a placeholder for the fitness score
    network.append([0])
    return network


def calculate_output(network, input_list):
    # returns the list of outputs
    # places inputs inside of placeholder
    for innput in range(len(input_list)):
        network[0][0][innput] = input_list[innput]

    # shit ton of maths
    for layer in range(1, len(network[0])):
        for end_neuron in range(len(network[0][layer])):
            network[0][layer][end_neuron] = network[2][layer - 1][end_neuron]
            for multiplication in range(len(network[0][layer - 1])):
                network[0][layer][end_neuron] += network[0][layer - 1][multiplication] * \
                                                 network[1][layer - 1][end_neuron][multiplication]
            network[0][layer][end_neuron] = sigmoid(network[0][layer][end_neuron])
    return network[0][-1]


def safe_network(network, filename):
    file = open(str(filename), "a+")
    file.write(str(network) + "\n")
    file.close()


def combine_networks(network1, network2, how_many):
    # both networks HAVE TO contain the same number inputs, hiddenlayers, neurons per layer and outputs
    # network1 & network2 = both netowrks, how_many = number of networks you want
    output_list = []

    for all_networks in range(how_many):
        # sets all placeholders in their place
        output_list.append([network1[0][:]])

        # sets all weights
        output_list[all_networks].append([])

        for i in range(len(network1[1])):
            output_list[all_networks][1].append([])
            for j in range(len(network1[1][i])):
                output_list[all_networks][1][i].append([])
                for k in range(len(network1[1][i][j])):
                    output_list[all_networks][1][i][j].append([])
                    output_list[all_networks][1][i][j][k] = ((how_many - all_networks) * network1[1][i][j][k] +
                                                             (all_networks + 1) * network2[1][i][j][k]) / (how_many + 1)

        # sets all biases
        output_list[all_networks].append([])
        for i in range(len(network1[2])):
            output_list[all_networks][2].append([])
            for j in range(len(network1[2][i])):
                output_list[all_networks][2][i].append([])
                output_list[all_networks][2][i][j] = ((how_many - all_networks) * network1[2][i][j] +
                                                      ((all_networks + 1) * network2[2][i][j])) / (how_many + 1)

    # creates fitness score placeholders for all networks
    for network in output_list:
        network.append([0])
    return output_list


def micro_evolution(network, percentage_change, changesize=0.25):
    # both networks HAVE TO contain the same number inputs, hiddenlayers, neurons per layer and outputs
    # network & network2 = both netowrks, how_many = number of output networks you will recieve
    output_network = []

    # sets all placeholders in their place
    output_network.append(network[0][:])

    # sets all weights
    output_network.append([])

    for i in range(len(network[1])):
        output_network[1].append([])
        for j in range(len(network[1][i])):
            output_network[1][i].append([])
            for k in range(len(network[1][i][j])):
                output_network[1][i][j].append([])
                output_network[1][i][j][k] = network[1][i][j][k]
                if random.uniform(0, 100) < percentage_change:
                    output_network[1][i][j][k] += random.gauss(0, changesize)

    # sets all biases
    output_network.append([])
    for i in range(len(network[2])):
        output_network[2].append([])
        for j in range(len(network[2][i])):
            output_network[2][i].append([])
            output_network[2][i][j] = network[2][i][j]
            if random.uniform(0, 100) < percentage_change:
                output_network[2][i][j] += random.gauss(0, changesize)

    # creates fitness score placeholders
    output_network.append([0])

    return output_network
