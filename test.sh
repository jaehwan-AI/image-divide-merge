#!/usr/bin/env bash

file_name=$1
col_num=$2
row_num=$3
prefix_output=$4

python divide_image.py --file_name=$file_name --col_num=$col_num --row_num=$row_num \
                    --prefix_output=$prefix_output --transform

python merge_image.py --prefix_input=$prefix_output --col_num=$col_num --row_num=$row_num \
                    --prefix_output='output'
