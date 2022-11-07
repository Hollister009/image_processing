# Dilate and Erode method
import cv2 as cv
import numpy as np

# Load the image in grayscale
img = cv.imread('../resources/picture.png', 0)
# Threshold the image with threshold value 127
ret, img = cv.threshold(img, 127, 255, 0)
original = img.copy()

# Step 1: Create an empty skeleton
size = np.size(img)
skeleton = np.zeros(img.shape, np.uint8)

# Get a Cross Shaped Kernel
element = cv.getStructuringElement(cv.MORPH_CROSS, (3, 3))

# Repeat steps 2-4
while True:
    # Step 2: Open the image
    opened = cv.morphologyEx(img, cv.MORPH_OPEN, element)
    # Step 3: Subtract open from original image
    temp = cv.subtract(img, opened)
    # Step 4: Erode the original image and refine the skeleton
    eroded = cv.erode(img, element)
    skeleton = cv.bitwise_or(skeleton, temp)
    img = eroded.copy()
    # Step 5: If there are no white pixels left ie.. the image has been completely eroded, quit the loop
    if cv.countNonZero(img) == 0:
        break

# Displaying the final results
cv.imshow('Original', original)
cv.imshow('Skeleton', skeleton)
cv.waitKey(0)
cv.destroyAllWindows()
