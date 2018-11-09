import numpy as np

class RNN():

    def __init__(self, spec):
        self.spec = spec
        self.edges = spec['edges']
        self.vertices = spec['vertices']

    def apply(self, data):

        # Get the data shape and the T length
        data_shape = data.shape
        T = len(data)

        # Define the dictionary state for each time step
        Dict_state = dict()
        for item in self.vertices:
            node = self.vertices[item]['num_nodes']
            value = np.zeros(node)
            Dict_state[item] = value

        # Inialize the memory_in0 as 0 vector
        OUTPUT = np.zeros([T,1])
        Dict_state['memory_in0'] = np.zeros(data_shape[1])

        # The Loop towards the time step
        for i in range(T):
            Dict_state['input'] = data[i, :]
            for idx, item in enumerate(self.edges):
                source_id = item['source_id']
                target_id = item['target_id']
                weight_source = item['weights']

                # identify if the target id has more then one source id
                N_targetid = [item_test['target_id'] == target_id for item_test in self.edges]
                # print(N_targetid)

                # check if the target id has more than one values
                if (source_id == 'memory_in0' and target_id == 'h1') or (source_id == 'memory_in0' and target_id == 'output'):
                    memory_id = source_id
                    weight_memory = item['weights']
                    continue
                if (source_id == 'input' and target_id == 'h1') or (source_id == 'input' and target_id == 'output'):
                    Dict_state[target_id] = self.vertices[target_id]['activation'](
                                            np.matmul(Dict_state[source_id], weight_source)
                                          + np.matmul(Dict_state[memory_id], weight_memory)
                                          + self.vertices[target_id]['bias'])
                else:
                    Dict_state[target_id] = self.vertices[target_id]['activation'](
                                            np.matmul(Dict_state[source_id], weight_source)
                                          + self.vertices[target_id]['bias'])

            memory = Dict_state['memory_out0']
            OUTPUT[i] = Dict_state['output']

            # update the dictionary states -- all sets as zeros
            for item in self.vertices:
                node = self.vertices[item]['num_nodes']
                value = np.zeros(node)
                Dict_state[item] = value

            # update the memory input with the previous memory output
            Dict_state['memory_in0'] = memory

        return OUTPUT