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
            # Diagonals of parallelograms bisect at the center of mass
            # Therefore, we can find the center of two opposing corners to find the centers of the squares
            firstCorner = np.array(corners[i][j])
            secondCorner = np.array(corners[i+1][j+1])

            centers[i][j] = (firstCorner + secondCorner)/2

    return centers

# findPieces
# Given an image of a checker board and the location of the center of the squares, this function will determine what color piece is at each square
# The function assumes that the pieces are only on black squares of the board and that the color of the pieces are known prior to running the program
# Returns: 2d numpy array of game state
# -1 - No piece present
#  0 - Black regular piece
#  1 - Red regular piece
#  2 - Black king
#  3 - Red king
def findPieces(image, corners):
    return np.zeros(shape = (8,8))

# getBoardState
# Returns the position of all the pieces on the checkers board
# Uses findCorners to locate vertices on the board, findCenters to find the centers of each of the square,
# and findPieces to determine what piece is in each square
# Returns: 2d numpy array of game state
# -1 - No piece present
#  0 - Black regular piece
#  1 - Red regular piece
#  2 - Black king
#  3 - Red king
def getBoardState(image):
    corners = findCorners(image)
    centers = findCenters(corners)

    return findPieces(image, corners)






if __name__ == "__main__":
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


