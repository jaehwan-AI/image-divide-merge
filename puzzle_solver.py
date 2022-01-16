# https://github.com/Avkash/demoapps/tree/master/PuzzleSolver
import numpy as np
from sklearn.neighbors import NearestNeighbors


def unscramble_image(im, blk_size, row, col, input_image_blocks, key_map, sortMap=False):
    print("input image blocks shape : ", input_image_blocks.shape)

    img_final = np.zeros((im.shape[0], im.shape[1], 3), dtype=np.uint8)
    print("img_shuff.shape : ", img_final.shape)

    if (sortMap):
        key_map_sorted = {k: v for k, v in sorted(key_map.items(), key=lambda x: x[1])}
        key_map_sorted_update = list(key_map_sorted.keys())
    else:
        key_map_sorted_update = key_map
    print(key_map_sorted_update)

    for i in range(0, row):
        for j in range(0, col):
            x, y = i*blk_size, j*blk_size
            img_final[x:x+blk_size, y:y+blk_size] = input_image_blocks[key_map_sorted_update[i*row+j]]
    return img_final


def generate_embedding_from_model(model, X, Y, output_shape_model):
    raw_embedding = model.predict(X)
    transformed_embedding = model.predict(Y)

    raw_embedding_flatten = raw_embedding.reshape((-1, np.prod(output_shape_model)))
    transformed_embedding_flatten = transformed_embedding.reshape((-1, np.prod(output_shape_model)))

    return raw_embedding_flatten, transformed_embedding_flatten


def fit_knn_model(image_flatten, knn_neighbors, knn_metric):
    knn = NearestNeighbors(n_neighbors=knn_neighbors, metric=knn_metric)
    knn.fit(image_flatten)
    return knn


def generate_mapping_list(knn, image_flatten):
    final_list_map = {}
    for i, embedding_flatten in enumerate(image_flatten):
        _, indices = knn.kneighbors([embedding_flatten])
        final_list_map[i] = indices[0][0]
    return final_list_map


def generate_result_image(images, img_size, row, col, img_blks_size, final_list_map):
    final_image = unscramble_image(images, img_size, row, col, img_blks_size, final_list_map)
    return final_image

