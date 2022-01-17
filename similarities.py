import cv2
import numpy as np
from skimage.metrics import structural_similarity

SIFT_RATIO = 0.7
MSE_NUMERATOR = 1000.0

def get_image_similarity(img1, img2, algorithm='SSIM'):
    similarity = 0.0
    
    if algorithm == 'SSIM':
        similarity = structural_similarity(img1, img2)
    elif algorithm == 'MSE':
        err = np.sum((img1.astype("float") - img2.astype("float")) ** 2)
        err /= float(img1.shape[0] * img2.shape[1])

        if err > 0.0:
            similarity = MSE_NUMERATOR / err
        else:
            similarity = 1.0
    else:
        return 0.0

    return similarity
