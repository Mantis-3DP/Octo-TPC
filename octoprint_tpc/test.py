import numpy as np


xyr0 = [1, 1]
xyr1 = [2, 1]
xyr2 = [2, 2]



import numpy as np

def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))


def calcOffset(xyr0, xyr1, xyr2):
	pos0 = np.array(xyr0)
	pos1 = np.array(xyr1)
	pos2 = np.array(xyr2)
	vecCamera0 = np.array([0, 0])
	vecCameraX = np.array([2, 0])
	vecCameraY = np.array([2, 2])

	# Translation
	matTrans = np.eye(3, dtype=int)
	matTrans[0, 2] = pos0[0]
	matTrans[1, 2] = pos0[1]

	matTransBack = np.eye(3, dtype=int)
	matTransBack[0, 2] = -pos0[0]
	matTransBack[1, 2] = -pos0[1]

	# Scale
	scaleX = np.linalg.norm(vecCameraX-vecCamera0)  # length vector the tool moved above the camera
	scaleY = np.linalg.norm(vecCameraY-vecCameraX)
	scaleToolX = np.linalg.norm(pos1 - pos0)
	scaleToolY = np.linalg.norm(pos2 - pos1)

	matScale = np.eye(3, dtype=float)
	matScale[0, 0] = scaleX/scaleToolX
	matScale[1, 1] = scaleY/scaleToolY

	# mirror

	matMir = -np.eye(3, dtype=int)

	# Rotation
	v0 = pos1 - pos0
	v1 = pos2 - pos1
	angle0 = angle_between(v0, vecCameraX)
	angle1 = angle_between(v1, vecCameraY- vecCameraX)
	matRot = np.zeros([3, 3])
	matRot[0, 0] = np.cos(angle0)
	matRot[1, 0] = np.sin(angle0)
	matRot[0, 1] = -np.sin(angle0)
	matRot[1, 1] = np.cos(angle0)
	matRot[2, 2] = 1

	matRotScale = np.matmul(matRot, matScale)
	matRotScaleTrans = np.matmul(matRotScale, matTrans)
	matBackRotScaleTrans = np.matmul(matRotScaleTrans, matTransBack)
	offset = np.dot(matBackRotScaleTrans, np.append(pos2-pos0, 0))
	# TODO: hier ist noch etwas falsch
	offset = (offset[0:2])
	print(offset)
	return offset

calcOffset(xyr0, xyr1, xyr2)
