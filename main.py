# Vision utils
from vision_utils.BoardStateDetection import findCorners, getBoardState
from vision_utils.BaxterCameraInterface import captureImage

# Game utils
from game_utils.

# Baxter utils
from baxter_utils

################################# CALIBRATION PROCEDURE #################################
#TODO Calibrate board position by moving Baxter in compliant mode

# Checkerboard camera calibration
# Capture a picture of the empty checkers board and determine the location of each square (corners of the squares) in the frame
emptyBoardImage = captureImage()
corners = findCorners(emptyBoard)

#TODO Create new checkers game
game =

while not game.finished():
    #TODO wait for opponent move

    # Capture image of the board
    boardImage = captureImage()

    # Determine the game state
    gameState = getBoardState(boardImage, corners)

    #TODO Send board state to game engine and determine move

    #TODO Determine what motions need to be made to execute move

    #TODO Calculate motion trajectories and execute




