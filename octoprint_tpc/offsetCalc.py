import numpy as np


def calcOffset(xy0, resolution):
	# 14.1mm bei 480px
	# => 14.1mm/480px = 0.029375 ungefähr 0.03mm/px
	# damit rechne ich einfach Abstand vom Mittelpunkt

	midpoint = [0, 0]

	offset = (np.array(xy0) - midpoint) * 0.03  # mm/px

	print(offset)
	return offset


if __name__ == '__main__':
	# this script is being run directly in the interpreter
	# i.e.  python this_script.py
	#
	# this block will not be executed when this is import'ed

	xy0 = [322, 240]
	calcOffset(xy0, resolution=[640, 480])
