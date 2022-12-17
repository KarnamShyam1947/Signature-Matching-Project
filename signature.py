import cv2
import os
from skimage.metrics import structural_similarity as ssim


def match(path1, path2):
    # read the images
    img1 = cv2.imread(path1)
    img2 = cv2.imread(path2)
    # turn images to grayscale
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    # resize images for comparison
    img1 = cv2.resize(img1, (300, 300))
    img2 = cv2.resize(img2, (300, 300))
    # display both images
    cv2.imshow("One", img1)
    cv2.imshow("Two", img2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    similarity_value = "{:.2f}".format(ssim(img1, img2)*100)
    # print("answer is ", float(similarity_value),
    #       "type=", type(similarity_value))
    return float(similarity_value)


if __name__ == '__main__' : 
    path1 = os.getcwd()+'\\static\\uploads\\test_img1.png'
    path2 = os.getcwd()+'\\static\\uploads\\test_img2.png'
    print(match(path1, path2))
