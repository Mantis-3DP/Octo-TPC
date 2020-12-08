import numpy as np
choices = {'x': '102', 'y': '161'}
offset = np.zeros([2])

offset[0] = choices["x"]
offset[1] = choices["y"]
print(offset[0])
print(offset[1])
