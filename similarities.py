import cv2
import numpy as np
from sklearn.metrics import structural_similarity

SIFT_RATIO = 0.7
MSE_NUMERATOR = 1000.0

def get_image_similarity(img1, img2, algorithm='SIFT'):
    img1 = cv2.imread(img1)
    img2 = cv2.imread(img2)

    similarity = 0.0

    if algorithm == 'SIFT':
        sift = cv2.xfeatures2d.SIFT_create()
        k1, d1 = sift.detectAndCompute(img1, None)
        k2, d2 = sift.detectAndCompute(img2, None)

        bf = cv2.BFMatcher()
        matches = bf.knnMatch(d1, d2, k=2)

        for m, n in matches:
            if m.distance < SIFT_RATIO * n.distance:
                similarity += 1.0
        if similarity == len(matches):
            similarity = 1.0
        elif similarity > 1.0:
            similarity = 1.0 - 1.0/similarity
        elif similarity == 1.0:
            similarity = 0.1
        else:
            similarity = 0.0
    
    elif algorithm == 'SSIM':
        similarity = structural_similarity(img1, img2)
    else:
        err = np.sum((img1.astype("float") - img2.astype("float")) ** 2)
        err /= float(img1.shape[0] * img2.shape[1])

        if err > 0.0:
            similarity = MSE_NUMERATOR / err
        else:
            similarity = 1.0

    return similarity
