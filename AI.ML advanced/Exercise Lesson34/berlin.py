import cv2

image = cv2.imread("Berlin.jpg")
print(image.shape)

# Task: Do the following image transformation by using numpy only (you could use cv2 to export image)
# 1. Flip the image horizontally, then export to a new image
image = image[::,::-1]
# 2. Flip the image vertically, then export to a new image
# 3. Rotate the image 90 degrees, then export to a new image
# 4. Rotate the image -90 degrees, then export to a new image
# 5. Resize the image from (1600x900) to (800x450)

cv2.imshow("result", image)
cv2.waitKey(0)