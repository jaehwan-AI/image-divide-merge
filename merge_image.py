import argparse
import json
import os

import albumentations as A
import cv2
import numpy as np


def img_tile(img_list):
    return cv2.vconcat([cv2.hconcat(img) for img in img_list])


def merge(args):
    fold_name = args.prefix_input
    json_object = json.load(open(f'{fold_name}/state.json', 'r'))

    imgs = []
    for i in range(args.col_num * args.row_num):
        file_path = 'test_'+str(json_object[i]['idx'])+'.jpg'
        img = cv2.imread(os.path.join(fold_name, file_path))

        if json_object[i]['r'] == True:
            img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        if json_object[i]['hf'] == True:
            img = A.HorizontalFlip(p=1.0)(image=img)['image']
        if json_object[i]['vf'] == True:
            img = A.VerticalFlip(p=1.0)(image=img)['image']

        imgs.append(img)
    lst = [imgs[i:i+args.col_num] for i in range(0, len(imgs), args.col_num)]
    img_tiles = img_tile(lst)
    
    cv2.imwrite('output.jpg', np.array(img_tiles))
    print("Success merged!!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Divide to Image")
    
    parser.add_argument('--prefix_input', type=str, default='tmp')
    parser.add_argument('--col_num', type=int, default=3, help='number of columns')
    parser.add_argument('--row_num', type=int, default=4, help='number of rows')
    parser.add_argument('--prefix_output', type=str, default='output')
    
    args = parser.parse_args()

    merge(args)
