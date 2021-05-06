import cv2
import numpy as np

def show(img):

    cv2.imshow("image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def binarization(img):

    binary = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    show(binary)

    ret, binary = cv2.threshold(binary, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    return binary

# def remove_branches(img):
#     return

def imfill(img):

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))

    fill = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel, iterations = 5)

    return fill

def find_square(img):
    return

def get_pixel_area():


    return

def get_leaf_area():

    return

def main():

    img = cv2.imread("images/square.jpg")
    # show(img)
    
    binary = binarization(img)
    # show(binary)
    
    fill = imfill(binary)

    square = find_square(fill)

    # compare = np.hstack((binary, fill))
    # show(compare)

    # calcular área

    
main()