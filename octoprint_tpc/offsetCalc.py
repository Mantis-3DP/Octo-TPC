import numpy as np

def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

def calcOffset(xy0, xy1, camerastep, resolution):
	pos0 = np.array(xy0)
	pos2 = np.array(xy1)
	vecCamera0 = np.array([0, 0])
	vecCamera1 = np.array([camerastep["x"], camerastep["y"]])
	CameraPos0 = np.array([resolution[0] / 2, resolution[1] / 2])
	v0 = pos2 - pos0
	v1 = vecCamera1-vecCamera0

	# Translation
	matTrans = np.eye(3, dtype=int)
	matTrans[0, 2] = pos0[0]
	matTrans[1, 2] = pos0[1]

	matTransBack = np.eye(3, dtype=int)
	matTransBack[0, 2] = -pos0[0]
	matTransBack[1, 2] = -pos0[1]

	# Scale
	scaleTool = np.linalg.norm(v0)
	scaleCamera = np.linalg.norm(v1)  # length vector the tool moved above the camera


	matScale = np.eye(3, dtype=float)
	matScale[0, 0] = scaleCamera/scaleTool
	matScale[1, 1] = scaleCamera/scaleTool

	# mirror
	matMir = np.eye(3, dtype=int)
	matMirY = matMir
	matMirY[1, 1] = -1

	# Rotation
	angle0 = angle_between(v0, v1)

	matRot = np.zeros([3, 3])
	matRot[0, 0] = np.cos(angle0)
	matRot[1, 0] = -np.sin(angle0)
	matRot[0, 1] = np.sin(angle0)
	matRot[1, 1] = np.cos(angle0)
	matRot[2, 2] = 1

	# matRotScale = np.matmul(matRot, matScale)
	# matRotScaleTrans = np.matmul(matRotScale, matTrans)
	# matBackRotScaleTrans = np.matmul(matRotScaleTrans, matTransBack)
	# matMirYScale = np.matmul(matMirY, matScale)
	# matRotTrans = np.matmul(matTrans, matRot)
	# matScaleRotTrans= np.matmul(matScale, matRotTrans)
	# matTransBackScaleRotTrans = np.matmul(matTransBack, matScaleRotTrans)
	# matTransBRotTrans = np.matmul(matTransBack, matRotTrans)

	offset = np.dot(matScale, np.append(pos0-CameraPos0, 0))
	# TODO: hier ist noch etwas falsch
	offset = (offset[0:2])
	print(offset)
	return offset


if __name__ == '__main__':
    # this script is being run directly in the interpreter
    # i.e.  python this_script.py
    #
    # this block will not be executed when this is import'ed

	xy0 = [480, 240]
	xy1 = [640, 80]
	camerastep = dict(x=2, y=2)
	calcOffset(xy0, xy1, camerastep, resolution=[640, 480])
