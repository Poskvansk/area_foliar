import cv2
import numpy as np
from matplotlib import pyplot as plt

def show(img):
    plt.imshow(img, cmap='gray', vmin=0, vmax=255); plt.show()

#binariza a imagem
def binarization(img):

    binary = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, binary = cv2.threshold(binary, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    return binary

#preenche pequenos buracos dentro das figuras
def imfill(img):

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
    fill = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

    return fill

# encontra o quadrado na imagem
def find_square(img):

    contours, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
        
        if(cv2.contourArea(contour) > 1000):
            x = approx.ravel()[0]   
            y = approx.ravel()[1]

            if len(approx) == 4:
                x, y, w, h = cv2.boundingRect(contour)

                square = img[y-5:y+h+5, x-5:x+w+5]
                # show(square)

    return square

# encontra a area do pixel
def get_pixel_area(square):

    # area conhecida
    square_area = 25 # cm quadrado

    # transforma array 2-D  em um array unidimensional
    arr = square.flatten()

    # imagem binaria, logo, soma de todos os valores / 255 = total de pixeis
    total_pixels = np.sum(arr)
    total_pixels /= 255

    pixel_area = square_area / total_pixels

    return pixel_area, total_pixels

def get_leaf_area(img, pixel_area, square):


    # transforma array 2-D em um array unidimensional
    arr = img.flatten()

    # imagem binaria, logo, soma de todos os valores / 255 = total de pixeis
    total_white = np.sum(arr)
    total_white /= 255
    
    #subtrai os pixeis do elemento de referencia
    total_white -= square
    
    area = total_white * pixel_area

    return area

def main():


    for i in range(10):

        img = cv2.imread("images/tomate{i}.jpeg".format(i=i+1))
        # plt.imshow(img[:,:,::-1]); plt.show()

        binary = binarization(img)
        # show(binary)
        
        fill = imfill(binary)
        # show(fill)

        square = find_square(fill)
        # show(square)

        pixel_area, total_square = get_pixel_area(square)
        
        leaf_area = get_leaf_area(fill, pixel_area, total_square)
        print(round(leaf_area, 2), " cm²")

main()