# image-divide-merge
---------------------
## Table of Contents

* [Contents](#contents)
* [Requirements](#requirements)
* [Quick Start](#quick-start)


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
