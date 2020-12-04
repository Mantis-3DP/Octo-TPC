import datetime
import numpy as np

print("Startup may take a few moments: Loading libraries; some of them are very large.")
try:
	global cv2
	import cv2
except:
	print("Import for CV2 failed.  Please install openCV")
	print("You may wish to use https://github.com/DanalEstes/PiInstallOpenCV")
	exit(8)

def nothing(x):
	pass

def putText(frame, text, color=(0, 0, 255), offsetx=0, offsety=0,
			stroke=1):  # Offsets are in character box size in pixels.
	if (text == 'timestamp'): text = datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S")
	baseline = 0
	fontScale = 1
	if (frame.shape[1] > 640): fontScale = stroke = 2
	offpix = cv2.getTextSize('A', cv2.FONT_HERSHEY_SIMPLEX, fontScale, stroke)
	textpix = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, fontScale, stroke)
	offsety = max(offsety, (-frame.shape[0] / 2 + offpix[0][1]) / offpix[0][1])  # Let offsety -99 be top row
	offsetx = max(offsetx, (-frame.shape[1] / 2 + offpix[0][0]) / offpix[0][0])  # Let offsetx -99 be left edge
	offsety = min(offsety, (frame.shape[0] / 2 - offpix[0][1]) / offpix[0][1])  # Let offsety  99 be bottom row.
	offsetx = min(offsetx, (frame.shape[1] / 2 - offpix[0][0]) / offpix[0][0])  # Let offsetx  99 be right edge.
	cv2.putText(frame, text,
				(int(offsetx * offpix[0][0]) + int(frame.shape[1] / 2) - int(textpix[0][0] / 2)
				 , int(offsety * offpix[0][1]) + int(frame.shape[0] / 2) + int(textpix[0][1] / 2)),
				cv2.FONT_HERSHEY_SIMPLEX, fontScale, color, stroke)
	return (frame)

def findValues():
	# Trackba
	cv2.namedWindow("Video")
	cv2.createTrackbar("minThreshold", "Video", 10, 100,nothing)
	cv2.createTrackbar("maxThreshold", "Video", 150, 255,nothing)
	cv2.createTrackbar("C", "Video", 0, 255,nothing)
	cv2.createTrackbar("minArea", "Video", 100, 200,nothing)
	cv2.createTrackbar("minCircularity", "Video", 55, 100,nothing)
	cv2.createTrackbar("minConvexity", "Video", 55, 100,nothing)
	cv2.createTrackbar("minInertiaRatio", "Video", 55, 100,nothing)


	cap = cv2.VideoCapture('http://192.168.178.26:8081/video.mjpg')
	while(True):
		ret, im = cap.read()
		minThreshold = cv2.getTrackbarPos("minThreshold", "Video")
		maxThreshold = cv2.getTrackbarPos("maxThreshold", "Video")
		c = cv2.getTrackbarPos("C", "Video")
		minArea = cv2.getTrackbarPos("minArea", "Video")
		minCircularity= cv2.getTrackbarPos("minCircularity", "Video")/100
		minConvexity = cv2.getTrackbarPos("minConvexity", "Video")/100
		minInertiaRatio = cv2.getTrackbarPos("minInertiaRatio", "Video")/100

		params = cv2.SimpleBlobDetector_Params()
		params.minThreshold = minThreshold;  # 79
		params.maxThreshold = maxThreshold;  # 90

		params.filterByArea = True  # Filter by Area.
		params.minArea = minArea

		params.filterByCircularity = True  # Filter by Circularity
		params.minCircularity = minCircularity #0.45

		params.filterByConvexity = True  # Filter by Convexity
		params.minConvexity = minConvexity #0.45
		params.filterByInertia = True  # Filter by Inertia
		params.minInertiaRatio = minInertiaRatio #0.5

		detector = cv2.SimpleBlobDetector_create(params)
		# Detect blobs.
		keypoints = detector.detect(im)
		frame = cv2.drawKeypoints(im, keypoints, np.array([]), (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)


		frame = putText(frame, 'timestamp', offsety=99)
		frame = putText(frame, 'number of circles: {}'.format(len(keypoints)), offsety=4)

		cv2.imshow("Video", frame)
		if cv2.waitKey(1) & 0xFF == ord("q"):
			break
	cap.release()
	cv2.destroyAllWindows



def createDetector(minThreshold=10, maxThreshold=200, minArea=100, minCircularity=0.55, minConvexity=0.55, minInertiaRatio=0.55):
	# Setup SimpleBlobDetector parameters.
	params = cv2.SimpleBlobDetector_Params()
	params.minThreshold = minThreshold # Change thresholds
	params.maxThreshold = maxThreshold
	params.filterByArea = True  # Filter by Area.
	params.minArea = minArea
	params.filterByCircularity = True  # Filter by Circularity
	params.minCircularity = minCircularity
	params.filterByConvexity = True  # Filter by Convexity
	params.minConvexity = minConvexity
	params.filterByInertia = True  # Filter by Inertia
	params.minInertiaRatio = minInertiaRatio
	detector = cv2.SimpleBlobDetector_create(params)
	return (detector)



def testConf():
	while(True):
		im = saveFrame()
		keypoints = createDetector().detect(im)
		frame = cv2.drawKeypoints(im, keypoints, np.array([]), (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

		frame = putText(frame, 'timestamp', offsety=99)
		print(len(keypoints))
		cv2.imshow("Video", frame)
		if cv2.waitKey(1) & 0xFF == ord("q"):
			break
	cv2.destroyAllWindows


def saveFrame():
	cap = cv2.VideoCapture('http://192.168.178.26:8081/video.mjpg')
	ret, im = cap.read()
	if im is None:
		print("unable to capture frame")
	return im


def position():
	im = saveFrame()
	keypoints = createDetector().detect(im)
	if len(keypoints) == 1:
		xy = np.around(keypoints[0].pt)
		r = np.around(keypoints[0].size / 2)
		text = "locating position successful"
		success = True
	elif len(keypoints) > 1:
		xy = [0, 0]
		r = 0
		text = "multiple positions found, check your settings"
		success = False
	elif len(keypoints) == 0:
		xy = [0, 0]
		r = 0
		text = "no position found, check your settings"
		success = False
	return xy, r, success



if __name__ == '__main__':
    # this script is being run directly in the interpreter
    # i.e.  python this_script.py
    #
    # this block will not be executed when this is import'ed
	findValues()
