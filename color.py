import cv2
import numpy as np
import os
def is_white(color, threshold_range=(180, 255)):
    # Check if the color is white based on a threshold range
    r, g, b = color
    return all(channel >= threshold_range[0] and channel <= threshold_range[1] for channel in (r, g, b))

def is_dark(color, threshold_range=(0, 120)):
    # Check if the color is dark based on a threshold range
    r, g, b = color
    return all(channel >= threshold_range[0] and channel <= threshold_range[1] for channel in (r, g, b))


def create_colored_image(width, height, r, g, b, filename):
    # Create an array filled with the specified RGB color
    image = np.zeros((height, width, 3), np.uint8)
    image[:] = (b, g, r)  # Note: OpenCV uses BGR format


    # Save the image
    cv2.imwrite(filename, image)



def get_dominant_colors(image, brightness, width, height, num_colors=10, threshold=200):   

    # Read the image
    img = cv2.imread(image)
    #Resize Image
    img = cv2.resize(img, (width, height))
    # Convert the image from BGR to RGB color space
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Reshape the image to a 1D array of pixels
    pixels = img.reshape(-1, 3)

    # Convert the pixel values to float32
    pixels = pixels.astype(np.float32)

    # Perform k-means clustering to find the dominant colors
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, 0.1)
    _, labels, centers = cv2.kmeans(pixels, num_colors, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    # Convert the center colors to uint8
    centers = centers.astype(np.uint8)

    # Filter out white, dark, and vibrant colors if there are multiple dominant colors
    if len(centers) >= 1:
        print("filtering")
        centers = [center.tolist() for center in centers if not is_white(center, threshold_range=(180, 255)) and not is_dark(center, threshold_range=(0, 120))]
        k = 0
        filtered_centers = []
        for i in centers:
            data = str(i).strip("[]").replace(",", "")
            values = data.split()
            values = [int(value) for value in values]  # Convert values to integers
            greyThreshold = 50
            print(centers[k])
            if brightness == 1:
                if abs(values[0] - values[1]) <= greyThreshold and abs(values[0] - values[2]) <= greyThreshold and abs(values[1] - values[2]) <= greyThreshold and abs(values[0] - values[2]) <= greyThreshold:
                    # Color is grayscale, exclude it
                    del centers[k]
                else:     
                    highest = 0
                    for l in values:
                        if highest <= l:
                            highest = l
                    coeficient = 255 - highest
                    new_center = [values[0] + coeficient, values[1] + coeficient, values[2] + coeficient]
                    #new_center = [255 - (values[0] + coeficient), 255 - (values[1] + coeficient), 255 - (values[2] + coeficient)]
                    filtered_centers .append(new_center)
            k += 1
        if brightness == 1:
            centers = filtered_centers 

    if not centers:
        centers = [[255, 255, 255]]  # Default white color
        print("default")

    print("---------------------------------------------")
    for i in centers:
        create_colored_image(100, 100, i[0], i[1], i[2], "cache/"+str(i)+".png")
        print(i)

    return centers