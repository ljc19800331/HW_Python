import numpy as np

class RNN():

    def __init__(self, spec):

        self.spec = spec
        self.edges = spec['edges']
        self.vertices = spec['vertices']

    def apply(self, data):

        # Get the data shape and the T length
        data_shape = data.shape

        # print(data)
        T = len(data)
        # print("The T is ", T)

        # Define the dictionary state for each time step
        Dict_state = dict()
        for item in self.vertices:
            node = self.vertices[item]['num_nodes']
            value = np.zeros(node)
            Dict_state[item] = value

        # Initialize the memory_in0 as 0 vector
        OUTPUT = np.zeros([T, 1])
        Dict_state['memory_in0'] = np.zeros(data_shape[1])

        # Design an object for checking targetID -- to see if we have more then one sourceID matched to same targetID
        TARGET_check = []

        # The Loop towards the time step
        for i in range(T):

            Dict_state['input'] = data[i, :]    # The size of the data for this case
            TARGET_check = []

            for idx, item in enumerate(self.edges):

                # Read the all three variables
                source_id = item['source_id']
                target_id = item['target_id']
                weight_source = item['weights']

                if target_id in TARGET_check:
                    continue

                # Check if TargetID is more then 1 value
                N_targetid = [item_test['target_id'] == target_id for item_test in self.edges]
                N_targetid_sum = sum([item_test['target_id'] == target_id for item_test in self.edges])

                if N_targetid_sum == 1:  # only 1 input value -- this is the normal case
                    Dict_state[target_id] = self.vertices[target_id]['activation'](
                        np.matmul(Dict_state[source_id], weight_source)
                        + self.vertices[target_id]['bias'])

                elif N_targetid_sum > 1:  # more then one input values -- this is the specical case

                    # save the TargetID -- since it will go through all the sourceID items with the same targetID
                    TARGET_check.append(target_id)

                    # Find all the input values
                    source_list = [item_test['source_id'] for item_test in self.edges if item_test['target_id'] == target_id]
                    item_list = [item_test for item_test in self.edges if item_test['target_id'] == target_id]

                    # Calculate the weighted values before function activation within the source_ids
                    h_sum = 0
                    for Dict_loop in item_list:
                        source_id_check = Dict_loop['source_id']
                        # print(source_id_check)
                        # print((Dict_state[source_id_check]))
                        # print((Dict_loop['weights']))
                        h_sum += np.matmul( Dict_state[source_id_check], np.asarray(Dict_loop['weights'], dtype = np.float64))

                    # Activation function for this case -- f = h(w1 * input1 + w2 * input2 + bias)
                    Dict_state[target_id] = self.vertices[target_id]['activation'](
                                            h_sum + self.vertices[target_id]['bias']
                                            )

            # Update the information for the output for each time step
            memory = Dict_state['memory_out0']
            OUTPUT[i] = Dict_state['output']

            # print(i+1)
            # print("memory_input:", Dict_state['memory_in0'])
            # update the memory input with the previous memory output
            Dict_state['memory_in0'] = memory

            # Check the values for each time step


            # print("input: ", Dict_state['input'])
            # print("h0: ", Dict_state['h0'])
            # print("h3: ", Dict_state['h3'])
            # print("h4: ", Dict_state['h4'])
            # print("h1: ", Dict_state['h1'])
            # print("h2: ", Dict_state['h2'])
            # print("memory_output:", Dict_state['memory_out0'])
            # print("output: ", Dict_state['output'])

        return OUTPUT