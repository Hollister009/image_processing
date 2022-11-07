import cv2 as cv
import numpy as np
from skimage.morphology import skeletonize

# image = np.array([
#     [0, 0, 0, 200, 200, 0, 0, 0],
#     [0, 0, 0, 200, 200, 0, 0, 0],
#     [0, 0, 0, 200, 200, 0, 0, 0],
#     [200, 200, 200, 200, 200, 200, 200, 200],
#     [200, 200, 200, 200, 200, 200, 200, 200],
#     [0, 0, 0, 200, 200, 0, 0, 0],
#     [0, 0, 0, 200, 200, 0, 0, 0],
#     [0, 0, 0, 200, 200, 0, 0, 0]], dtype=np.uint8)

# Load image
image = cv.imread('./resources/horse.png', 0)

# Threshold the image with value 127
ret, image = cv.threshold(image, 127, 255, 0)
# print(image)

original = image.copy()

# Normalize input to have 1s instead of 255s
image = cv.normalize(image, None, alpha=0, beta=1, norm_type=cv.NORM_MINMAX)
skeleton = skeletonize(image) * 1

# Normalize output to have 255s instead of 1s
skeleton = cv.normalize(skeleton, None, alpha=0, beta=255, norm_type=cv.NORM_MINMAX)
skeleton = skeleton.astype(np.uint8)

# Display the final results
cv.imshow('Original', original)
cv.imshow('Skeleton', skeleton)
cv.waitKey(0)
cv.destroyAllWindows()
