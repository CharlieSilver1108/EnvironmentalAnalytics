# This is a template. 
# You should modify the functions below to match
# the signatures determined by the project specification
import numpy as np
from skimage import io, color, util


def convert_to_binary(IMG):
    mapImage = color.rgba2rgb(IMG)
    mapImage = color.rgb2gray(mapImage)
    mapImage = util.img_as_bool(mapImage)
    mapImage = util.img_as_ubyte(mapImage)
    return(mapImage)

def find_red_pixels(map_filename, upper_threshold=100, lower_threshold=50):
    """Returns a 2D numpy array of each red pixel and writes it to a file named 'map-red-pixels.jpg"""
    mapImage = io.imread(map_filename)
    lineNumber = 0
    for line in mapImage:
        columnNumber = 0
        for pixel in line:
            if ((pixel[0] > upper_threshold) and (pixel[1] < lower_threshold) and (pixel[2] < lower_threshold)):
                mapImage[lineNumber, columnNumber] = [255, 255, 255, 255]
            else:
                mapImage[lineNumber, columnNumber] = [0, 0 , 0, 255]
            columnNumber += 1
        lineNumber += 1
    mapImage = convert_to_binary(mapImage)
    io.imsave('data/map-red-pixels.jpg', mapImage)

def find_cyan_pixels(mapFilename, upper_threshold=100, lower_threshold=50):
    """Returns a 2D numpy array of each cyan pixel and writes it to a file named 'map-cyan-pixels.jpg"""
    mapImage = io.imread(mapFilename)
    lineNumber = 0
    for line in mapImage:
        columnNumber = 0
        for pixel in line:
            if ((pixel[0] < lower_threshold) and (pixel[1] > upper_threshold) and (pixel[2] > upper_threshold)):
                mapImage[lineNumber, columnNumber] = [255, 255, 255, 255]
            else:
                mapImage[lineNumber, columnNumber] = [0, 0 , 0, 255]
            columnNumber += 1
        lineNumber += 1
    mapImage = convert_to_binary(mapImage)
    io.imsave('data/map-cyan-pixels.jpg', mapImage)


def detect_connected_components(IMG):
    """Returns a 2D numpy array and write the number of pixels inside each connected component into a text file 'cc-output-2a.txt'"""
    try:
        mapImage = io.imread(IMG)
    except:
        print("Image does not exist")
        return(0)
    dimensions = mapImage.shape
    width = dimensions[0]
    height = dimensions[1]
    MARK = np.zeros((width,height), dtype=int)
    Q = np.ndarray((0,2), dtype=int)

    pixel_id = 0
    neighbours = lambda x, y : [(x2, y2) for x2 in range(x-1, x+2) for y2 in range(y-1, y+2) if (-1 < x <= (width -1) and (-1 < y <= (height -1)) and (x != x2 or y != y2) and (0 <= x2 <= (width -1)) and (0 <= y2 <= (height -1)))]


    for x in range(0, width):
        for y in range(0, height):
            if (mapImage[x,y] > 200) and (MARK[x,y] == 0):
                pixel_id += 1
                MARK[x,y] = pixel_id
                Q = np.append(Q, [[x,y]], axis=0)
                while len(Q) > 0:
                    currentPixel, Q = Q[-1], Q[:-1]
                    currentX, currentY = currentPixel[0], currentPixel[1]
                    for neighbour in neighbours(currentX, currentY):
                        i,j = neighbour[0],neighbour[1]
                        try:
                            if (mapImage[i,j] > 200) and (MARK[i,j] == 0):
                                MARK[i,j] = pixel_id
                                Q = np.append(Q, [[i,j]], axis=0)
                        except:
                            continue

    components = get_components(MARK)
    with open("data/cc-output-2a.txt", "w") as file:
        for key in components:
            file.writelines(f"Connected component {key}, number of pixels = {components[key]}\n")
        file.writelines(f"Total number of connected components = {len(components)}")

    return(MARK)

def get_components(MARK):
    components = {}
    for row in MARK:
        for pixel in row:
            if pixel != 0:
                if pixel not in components:
                    components[pixel] = 1
                else:
                    components[pixel] += 1
    return(components)


def detect_connected_components_sorted(MARK):
    """Writes all conneceted components in decreasing order into a text file 'cc-output-2b.txt' and writes the two largest into 'cc-top-2.txt'"""
    components = get_components(MARK)
    componentsArray = convert_to_array(components)
    componentsSorted = bubble_sort(componentsArray)
    with open("data/cc-output-2b.txt", "w") as file:
        for component in componentsSorted:
            file.writelines("Connected component " + str(component[0]) + ", number of pixels = " + str(component[1]) + "\n")
        file.writelines("Total number of connected components = " + str(len(componentsSorted)))


def convert_to_array(components):
    componentsArray = []
    for key in components:
        numberOfPixels = components[key]
        componentsArray.append([key, numberOfPixels])
    return(componentsArray)
    

def bubble_sort(array):
    n = len(array)

    for i in range(n):
        sorted = True

        for j in range(n - i - 1):
            if array[j][1] < array[j + 1][1]:
                array[j], array[j + 1] = array[j + 1], array[j]
                sorted = False

        if sorted:
            break

    return array
