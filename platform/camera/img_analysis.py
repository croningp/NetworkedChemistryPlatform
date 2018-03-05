import cv2
import numpy as np

MAX_HUE = 256
HUE_DIVISION = 2

def get_ROI(image):
    """
    Gets the region of interest for an image

    Args:
        image (cv2.Image): Image to crop

    Returns:
        image (cv2.Image): The cropped region of the image
    """
    return image[270:450, 140:480]

def get_average_hue_value(img_path):
    """
    Gets the average hue value from a specific region of interest in an image

    Args:
        img_path (str): Path towards the image

    Returns:
        hue (float): Average hue value of the image
    """
    print('Analysing {0}'.format(img_path))
    image = cv2.imread(img_path)
    ROI = get_ROI(image)
    hsv = cv2.cvtColor(ROI, cv2.COLOR_BGR2HSV_FULL)
    average = hsv[0,0]
    for i in range(len(hsv)):
        for j in range(len(hsv)):
            average = np.vstack([average, hsv[i,j]])

    hsv_mean = np.mean(average, axis=0)

    return int(hsv_mean[0])

def create_bucket():
    """
    Creates a dictionary of hue ranges with their counts set to 0

    Returns:
        buckets (Dict): Dictionary containing hue regions and their counts
    """
    return {x : 0 for x in range(int(MAX_HUE/HUE_DIVISION))}
