#!/usr/bin/env bash

# cleanup input data
rm -rf input/*
rm -rf output/*
rm -rf /tmp/_days

# download data from server01
scp -r victor@server01.local:_days /tmp/

# copy only pdf data
find /tmp/_days/ -name "*.pdf" -exec cp {} input/ \;

# watermark all pages
python3.7 ../src/pdf-watermark.py \
    --source=$(pwd)/input \
    --destination=$(pwd)/output \
    --watermark=$(pwd)/watermak/2020.01.31.pdf

# archive data
tar -cvf archive.tar.gz output