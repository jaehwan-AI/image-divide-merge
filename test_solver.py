import argparse
import os

import albumentations as A
import cv2
import numpy as np

from model import AutoEncoder
from puzzle_solver import (fit_knn_model, generate_embedding_from_model,
                           generate_mapping_list, generate_result_image,
                           unscramble_image)


def merge(args):
    fold_name = args.prefix_input
    file_names = os.listdir(fold_name)
    
    model = AutoEncoder()
    raw_embedding_flatten, transformed_embedding_flatten = generate_embedding_from_model(model, raw_image, transformed_image, output_shape_model)

    knn_neighbors = 5
    knn_metric = "cosine"
    knn = fit_knn_model(raw_embedding_flatten, knn_neighbors, knn_metric)

    final_list_map = generate_mapping_list(knn, )
    final_image_np = generate_result_image()
    
    cv2.imwrite('output.jpg', np.array(final_image_np))
    print("Success merged!!")
