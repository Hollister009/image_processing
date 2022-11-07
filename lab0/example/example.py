import cv2 as cv


def color_at(img, x, y):
    return img[y][x]


def image_line(img, x1, y1, x2, y2, color):
    cv.line(img, (x1, y1), (x2, y2), color)
    return 0


def neighbours(x, y, image):
    # P2, P3, ..., P9
    points = [[0, -1], [1, -1], [1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1]]
    i = image
    # print((x,y))
    return [i[y + py][x + px] for px, py in points]

# def neighbours(x, y, image):
#     '''Return 8-neighbours of point p1 of picture, in order'''
#     i = image
#     x1, y1, x_1, y_1 = x+1, y-1, x-1, y+1
#     #print ((x,y))
#     return [i[y1][x],  i[y1][x1],   i[y][x1],  i[y_1][x1],  # P2,P3,P4,P5
#             i[y_1][x], i[y_1][x_1], i[y][x_1], i[y1][x_1]]


image = cv.imread('./resources/horse.png', 0)
# Threshold the image with value 127
ret, image = cv.threshold(image, 127, 255, 0)
skeleton = image.copy()

# Get dimensions of the image
height, width = image.shape
# print('Image height {}'.format(height))
# print('Image width: {}'.format(width))


is_open = False
start = 0

# for y in range(height):
#     for x in range(width):
for y in range(1, len(image) - 1):
    for x in range(1, len(image[0]) - 1):
        print(neighbours(x, y, image))

        if not is_open:
            if color_at(skeleton, x, y) == 255:
                is_open = True
                start = x
        elif color_at(skeleton, x, y) == 0:
            is_open = False
            x0 = x - 1
            c = round((start + x0) / 2)
            image_line(skeleton, start, y, c - 1, y, 0)
            image_line(skeleton, c + 1, y, x0, y, 0)

is_open = False
start = 0

for y in range(1, len(image) - 1):
    for x in range(1, len(image[0]) - 1):
        if not is_open:
            if color_at(image, x, y) == 255:
                is_open = True
                start = y
        elif color_at(image, x, y) == 0:
            is_open = False
            y0 = y - 1
            c = round((start + y0) / 2)
            skeleton[c, x] = 255

# Displaying the final results
cv.imshow('Original', image)
cv.imshow('Skeleton', skeleton)
cv.waitKey(0)
cv.destroyAllWindows()
