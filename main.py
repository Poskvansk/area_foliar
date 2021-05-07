import cv2
import numpy as np

import time



def show(img):

    cv2.imshow("image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def binarization(img):

    binary = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, binary = cv2.threshold(binary, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    return binary

# def remove_branches(img):
#     return

def imfill(img):

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))

    fill = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel, iterations = 5)

    return fill

def fill_holes(img):
    
    negative = cv2.bitwise_not(img)
    aux = negative.copy()

    cv2.floodFill(aux, None, (0,0), 0)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
    aux = cv2.morphologyEx(aux, cv2.MORPH_DILATE, kernel, iterations = 3)
    # show(aux)

    # negativo + aux = imagem com buracos preenchidos
    filled = cv2.bitwise_or(img, aux)

    # fechamento para quaisquer pequenos buracos que tiverem sobrado
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4,4))
    filled = cv2.morphologyEx(filled, cv2.MORPH_CLOSE, kernel, iterations=3)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
    filled = cv2.morphologyEx(filled, cv2.MORPH_OPEN, kernel, iterations=3)

    # comp = np.hstack((img, filled))
    # show(comp)

    return filled

def find_square(img):

    contours, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
        
        if(cv2.contourArea(contour) > 1000):
            x = approx.ravel()[0]
            y = approx.ravel()[1]

            if len(approx) == 4:
                # cv2.drawContours(draw, [approx], 0, (0,0,255), 3)
                x,y,w,h = cv2.boundingRect(contour)
                # print(x, y, w, h)

                ROI = img[y-5:y+h+5, x-5:x+w+5]
                # show(ROI)

    return ROI

def get_pixel_area(square):

    square_area = 81

    arr = square.flatten()

    total_pixels = np.sum(arr)
    total_pixels /= 255
    # print(total_pixels)

    pixel_area = square_area / total_pixels
    # print(pixel_area)

    return pixel_area

def get_leaf_area(img, pixel_area):

    arr = img.flatten()
    total_white = np.sum(arr)

    area = total_white * pixel_area

    return area

def main():

    img = cv2.imread("images/square.jpg")
    # show(img)
    
    binary = binarization(img)
    # show(binary)
    
    # fill = imfill(binary)
    fill = fill_holes(binary)

    square = find_square(binary)
    # show(square)

    pixel_area = get_pixel_area(square)
    # print(pixel_area)

    leaf_area = get_leaf_area(fill, pixel_area)
    print(leaf_area)

    # compare = np.hstack((fill, test))
    # show(compare)
    
main()