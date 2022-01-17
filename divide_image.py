import argparse
# import json
import os
import random
import re
from glob import glob
from pathlib import Path

import albumentations as A
import cv2
import numpy as np


def resize_image(image, row, col):
    width, height = image.shape[1], image.shape[0]
    while width % col != 0:
        width -= 1
    while height % row != 0:
        height -= 1
    return width//col, height//row


def increment_path(path, exist_ok=False):
    path = Path(path)
    if (path.exists() and exist_ok) or (not path.exists()):
        return str(path)
    else:
        dirs = glob(f"{path}*")
        matches = [re.search(rf"%s(\d+)" % path.stem, d) for d in dirs]
        i = [int(m.groups()[0]) for m in matches if m]
        n = max(i) + 1 if i else 2
        return f"{path}{n}"


def createDirectory(save_dir):
    try:
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
    except OSError:
        print("Error: Failed to create the directory.")


def divide_transform(args):
    save_dir = increment_path(os.path.join(args.prefix_output))
    createDirectory(save_dir)
    json_object = []

    img = cv2.imread(args.file_name)

    if img.shape[0] % args.row_num != 0 or img.shape[1] % args.col_num != 0:
        width, height = resize_image(img, args.row_num, args.col_num)
    else:
        width, height = img.shape[1]//args.col_num, img.shape[0]//args.row_num

    for i in range(args.row_num):
        for j in range(args.col_num):
            image = img[i*height:(i+1)*height, j*width:(j+1)*width, :]
            # vf, hf, r = False, False, False
            if args.transform:
                if random.random() < 0.5:
                    image = A.VerticalFlip(p=1.0)(image=image)['image']
                    # vf = True
                if random.random() < 0.5:
                    image = A.HorizontalFlip(p=1.0)(image=image)['image']
                    # hf = True
                if random.random() < 0.5:
                    image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
                    # r = True
            
            file_name = int(random.random()*65536)
            cv2.imwrite(f'{save_dir}/test_{file_name}.jpg', np.array(image))

            # state = {'idx': file_name, 'vf': vf, 'hf': hf, 'r': r}
            # json_object.append(state)

    # with open(f'{save_dir}/state.json', 'w', encoding='utf-8') as f:
    #     json.dump(json_object, f, indent='\t')

    print("Success divided!!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Divide to Image")
    
    parser.add_argument('--file_name', type=str, default='samples/xp.jpg', help='input file name(path)')
    parser.add_argument('--col_num', type=int, default=3, help='number of columns')
    parser.add_argument('--row_num', type=int, default=4, help='number of rows')
    parser.add_argument('--prefix_output', type=str, default='tmp')
    parser.add_argument('--transform', action='store_true', help='transform implement or not')
    
    args = parser.parse_args()

    divide_transform(args)
