import cv2
import numpy as np

# findCorners
# Given an image of a checkerboard, this function will return the location of all of the corners
# of the squares of the checkerboard
# img - numpy array containing the image of the checkerboard
# returns (9,9,2) numpy array containing the (x,y) coordinates of the checkerboard
def findCorners(img):
    # Convert image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    threshold = 150

    # Apply a threshold to the grayscale image to make the dark squares white and the light squares black
    # Colors are inverted so that the border of the checkboard is white
    # This is a requirement for the cv2.findChessboardCorners to correctly find the corners
    grayThresholded = np.zeros(shape = gray.shape,  dtype = gray.dtype)
    grayThresholded[gray > threshold] = 0
    grayThresholded[gray <= threshold] = 255

    cv2.imshow("test", grayThresholded)
    cv2.waitKey(0)

    # Get the internal corners of the checkerboard using the cv2 find chessboard corners used for camera calibration
    ret, initial_corners = cv2.findChessboardCorners(gray, (7,7), None)

    print(initial_corners)

    # Reshape corners to a square matrix
    initial_corners = np.squeeze(initial_corners, axis = 1)
    initial_corners = np.reshape(initial_corners, (7,7,2))

    # Create a new np array with the dimension of the corners including the external corners of the board
    corners = np.zeros((initial_corners.shape[0] + 2, initial_corners.shape[1] + 2, 2), dtype = initial_corners.dtype)

    # Populate the center of corners with the internal corners detected by the find chessboard algorithm
    corners[1:-1, 1:-1] = initial_corners

    # Iterate over first dimension of the corners matrix and extrapolate the position of the edge corners
    for i in range(len(initial_corners)):

        # Vector that describes the length (and direction) of one edge of a square
        squareEdgeVector = ((initial_corners[i][6][0]-initial_corners[i][0][0])/6, (initial_corners[i][6][1]-initial_corners[i][0][1])/6)

        # Find the new corners along the line by adding the vector to the last point and subtracting from the first point
        corners[i+1][0] = np.array((int(initial_corners[i][0][0] - squareEdgeVector[0]), int(initial_corners[i][0][1] - squareEdgeVector[1])))
        corners[i+1][-1] = np.array((int(initial_corners[i][6][0] + squareEdgeVector[0]), int(initial_corners[i][6][1] + squareEdgeVector[1])))

    # Iterate over second dimension of the corner matrix and extrapolate position of edge corners
    for i in range(corners.shape[1]):

        # Vector that describes the length (and direction) of one edge of a square
        squareEdgeVector = ((corners[-2][i][0]-corners[1][i][0])/6, (corners[-2][i][1]-corners[1][i][1])/6)

        # Find the new corners along the line by adding the vector to the last point and subtracting from the first point
        corners[0][i] = np.array((int(corners[1][i][0] - squareEdgeVector[0]), int(corners[1][i][1] - squareEdgeVector[1])))
        corners[-1][i] = np.array((int(corners[-2][i][0] + squareEdgeVector[0]), int(corners[-2][i][1] + squareEdgeVector[1])))

    return corners

# findCenters
# Finds the centers of the squares on the checkerboard
# corners - (9,9,2) array of all of the corners of the checkerboard
# returns a (8,8,2) array of the (x,y) coordinates of the centers of each square
def findCenters(corners):
    # Instantiate array for store the centers
    centers = np.zeros((corners.shape[0] - 1, corners.shape[1] -1, 2))

    # Iterate over all of the corners in the corner matrix
    for i in range(corners.shape[0] - 1):
        for j in range(corners.shape[1] - 1):
            # Checkerboard corners form parallelograms for each square
            # Diagonals of parallelgrams bisect at the center of mass
            # Therefore, we can find the center of two opposing corners to find the centers of the squares
            firstCorner = np.array(corners[i][j])
            secondCorner = np.array(corners[i+1][j+1])

            centers[i][j] = (firstCorner + secondCorner)/2

    return centers


def findPieces(image):
    # Find the difference between the two images
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Set our filtering parameters
    # Initialize parameter settiing using cv2.SimpleBlobDetector
    params = cv2.SimpleBlobDetector_Params()

    # # Set Area filtering parameters
    # params.filterByArea = True
    # params.minArea = 100

    # # Set Circularity filtering parameters
    # params.filterByCircularity = True
    # params.minCircularity = 0.9

    # # Set Convexity filtering parameters
    # # params.filterByConvexity = True
    # # params.minConvexity = 0.2

    # # Set inertia filtering parameters
    # params.filterByInertia = True
    # params.minInertiaRatio = 0.01

    # Create a detector with the parameters
    detector = cv2.SimpleBlobDetector_create(params)

    # Detect blobs
    keypoints = detector.detect(image)

    # Draw blobs on our image as red circles
    blank = np.zeros((1, 1))
    blobs = cv2.drawKeypoints(image, keypoints, blank, (0, 0, 255),
                            cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    number_of_blobs = len(keypoints)
    text = "Number of Circular Blobs: " + str(len(keypoints))
    cv2.putText(blobs, text, (20, 550),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 100, 255), 2)

    # Show blobs
    cv2.imshow("Filtering Circular Blobs Only", blobs)
    cv2.waitKey(0)
    cv2.destroyAllWindows()







    # # ensure at least some circles were found
    # if circles is not None:
    #     # convert the (x, y) coordinates and radius of the circles to integers
    #     circles = np.round(circles[0, :]).astype("int")

    #     # loop over the (x, y) coordinates and radius of the circles
    #     for (x, y, r) in circles:
    #         # draw the circle in the output image, then draw a rectangle
    #         # corresponding to the center of the circle
    #         cv2.circle(output, (x, y), r, (0, 255, 0), 4)
    #         cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

    # show the output image




# Load image from file
img = cv2.imread("test4.jpg")

imgWithPieces = cv2.imread("test4.jpg")

#findPieces(imgWithPieces)

corners = findCorners(img)

# Once we have found all the corners of the checkerboard, we need to find the center of mass of the squares
centers = findCenters(corners)

color = (255,0,0)

for center in np.reshape(centers, (64,2)):
    cv2.circle(img, (int(center[0]), int(center[1])), radius = 5, color = color)

cv2.imshow("test",img)
cv2.waitKey(20000)


