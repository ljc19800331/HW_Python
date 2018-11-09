import numpy as np
# from moving_average import spec
from example1 import spec

data = np.ones((10, 2))
# data = np.random.uniform(size=(10, 1))
data_shape = data.shape
T = len(data)       # number of time step

# Define the state dictionary
vertices = spec['vertices']
# vtx_names = list()
# for i in vertices.keys():
#     vtx_names.append(i)

# Define the key items and values
Dict_state = dict()
edges = spec['edges']

# Initialize the dictionary values
for item in vertices:
    node = vertices[item]['num_nodes']
    value = np.zeros(node)
    Dict_state[item] = value

# Initialize the memory --
Dict_state['memory_in0'] = np.zeros(data_shape[1])

for i in range(T):

    Dict_state['input'] = data[i,:]

    for item in edges:
        source_id = item['source_id']
        target_id = item['target_id']
        weights = item['weights']
        Dict_state[target_id] = Dict_state[target_id] + vertices[target_id]['activation'](np.matmul(Dict_state[source_id], weights) + vertices[target_id]['bias'])
        # Dict_state[target_id] = vertices[target_id]['activation'](np.matmul(Dict_state[source_id], weights) + vertices[target_id]['bias'])

    memory = Dict_state['memory_out0']
    print(Dict_state['output'])

    for item in vertices:
        node = vertices[item]['num_nodes']
        value = np.zeros(node)
        Dict_state[item] = value

    Dict_state['memory_in0'] = memory

truth = np.array([
    [-1.02626227],
    [-0.95136591],
    [-0.98218756],
    [-0.98431546],
    [-0.98666519],
    [-0.98744132],
    [-0.98783109],
    [-0.98801656],
    [-0.98811267],
    [-0.98816380]
])

# n = 1
# data_cat = np.concatenate( (np.zeros((n, 1)), data[:-n, :]))
# truth = (data + data_cat) / 2
# print(truth)