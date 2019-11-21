import rospy
from sensor_msgs.msg import Image
import numpy as np

# cv_bridge for converting ROS images into opencv Mats
from cv_bridge import CvBridge, CvBridgeError

# Topic to receive camera image from
LEFT_ARM_CAMERA_TOPIC = ""

# List storing the joint angles for the left arm to orient the camera to capture image of the board
LEFT_ARM_CAPTURE_POSE = {
    "shoulder" : 0,
    "elbow" : 0,
    "wrist" : 0

}

# List storing the joint angles for the left arm when the camera is not being used (to avoid collision)
LEFT_ARM_IDLE_POSE = {
    "shoulder" : 0,
    "elbow" : 0,
    "wrist" : 0

}

# captureImage
# Captures an image of the checkerboard in front of Baxter using the camera on the left arm
# First, the camera is moved from the idle position to capture position so that the checkerboard is in frame
# A single camera message is then captured from the left arm image topic
# The arm is returned to idle position and the image is returned
# Returns - numpy array containing the captured image of the checkerboard
def captureImage():
    # Create a publisher for the shoulder, elbow, and wrist
    shoulderPub = rospy.Publisher()
    elbowPub = rospy.Publisher()
    wristPub = rospy.Publisher()

    # Publish the new joint angles
    shoulderPub.publish(LEFT_ARM_CAPTURE_POSE["shoulder"])
    elbowPub.publish(LEFT_ARM_CAPTURE_POSE["elbow"])
    wristPub.publish(LEFT_ARM_CAPTURE_POSE["wrist"])

    #TODO Implement waiting until the desired joint angle is reached

    rosImage = rospy.wait_for_message(LEFT_ARM_CAMERA_TOPIC, Image, timeout=None)

    try:
        bridge = CvBridge()
        image = np.asarray(bridge.imgmsg_to_cv2(data, "bgr8"))
    except CvBridgeError as e:
        print(e)

    # Publish the new joint angles to return to idle pose
    shoulderPub.publish(LEFT_ARM_IDLE_POSE["shoulder"])
    elbowPub.publish(LEFT_ARM_IDLE_POSE["elbow"])
    wristPub.publish(LEFT_ARM_IDLE_POSE["wrist"])

    #TODO Implement waiting until the desired joint angle is reached

    return image

