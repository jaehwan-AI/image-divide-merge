# image-divide-merge
---------------------
## Table of Contents

* [Overview](#overview)
* [Contents](#contents)
* [Requirements](#requirements)
* [Quick Start](#quick-start)

## Overview
* trial
    1. 이미지 stitching : 이미지의 공통된 부분을 파노라마 형식으로 연결하는 방법으로 시도하려 했으나 이미지에 공통된 부분이 없어 매끄러운 연결이 되지 않음
    2. puzzle solver model 사용 : 이미지 임베딩 후 KNN model을 통해 유사도로 이미지를 연결하는 방법(https://github.com/Avkash/demoapps/tree/master/PuzzleSolver)
    -> __이미지의 원본을 사용하므로 적절한 방법은 아님__
    3. 이미지 사이의 edge 유사도 비교 : 이미지와 이미지의 edge 간 유사도를 비교해서 일정 threshold를 넘으면 연결하는 방법(SSIM, MSE로 유사도를 결정)
        __1) 처음 불러오는 이미지를 기준으로 4방향에 붙이는 이미지가 총 8개의 경우를 가지고 있으므로 32가지 경우를 하드코딩할 수 있음__
        __2) 매 이미지를 불러와 하드코딩하면서 이미지의 위치를 찾는 것은 해당 measure(SSIM, MSE)로는 한계가 있음 : 2x2 정도의 split은 가능하나 확장성이 떨어진다고 판단됨__

* conclusion
    - 완전 탐색 방법(모든 경우의 수를 고려)으로 하드코딩을 해서 문제를 푸는 것은 해당 문제 해결 방법이 아니라고 판단했습니다.
    - 또한, Random하게 분포되어 있는 이미지의 위치를 찾으며 매끄럽게 연결할 수 있는 적절한 measure를 찾기 못 했습니다.

## Contents
```
.
├── divide_image.py
├── merge_image.py
├── README.md
├── samples
└── test.sh
```


## Requirements
* Python >= 3.8
* opencv-python
    > pip install opencv-python
* opencv-contrib-python
    > pip install opencv-contrib-python
* Numpy
    > pip install numpy
* albumentations
    > pip install albumentations


## Quick Start
* Clone this repository
```bash
$ git clone https://github.com/jaehwan-AI/image-divide-merge.git {fold_name}
```
* Run the demo
```bash
$ sh test.sh {file_name} {col_num} {row_num} {prefix_output}
```
>**divide image**

If you want to implement transform, Input "--transform" at the end of the sentence.
```bash
$ python divide_image.py --file_name {file_name} --col_num {col_num} --row_num {row_num} --prefix_output {prefix_output}
```
>**merge images**
```bash
$ python merge_image.py --prefix_input {prefix_input} --col_num {col_num} --row_num {row_num} --prefix_output {prefix_output}
```
