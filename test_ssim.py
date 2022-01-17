import os
from itertools import permutations

import albumentations as A
import cv2

from similarities import get_image_similarity


def check_similarity(img1, img2, threshold=0.5):
    
    sim = get_image_similarity(img1, img2)
    if sim > threshold:
        return True
    else:
        return False


fold_name = 'tmp'
file_names = os.listdir(fold_name)
imgs_lst = list(permutations(file_names, len(file_names)))

for imgs in imgs_lst:
    lst = [imgs[i:i+2] for i in range(0, len(imgs), 2)]
    for l in lst:
        for i in range(len(l)):
            print(l[i])


