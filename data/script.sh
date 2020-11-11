#!/usr/bin/env bash

if [ ! $RELEASE_DATE ]; then
    echo "You must set the date of the release in yyyy-mm-dd format. Ex. export RELEASE_DATE=2018.02.02"
    exit 1
fi

# cleanup input data
rm -rf input/*
rm -rf output/*
rm -rf /tmp/_days

# download data from server01
scp -r victor@server01.local:/mnt/hdd1/backups/google_drive/last/professional/documentation/training/Lessons/Kubernetes/days /tmp/_days

# copy only pdf data
find /tmp/_days/ -name "*.pdf" -exec cp {} input/ \;

# watermark all pages
python3.7 ../src/pdf-watermark.py \
    --source=$(pwd)/input \
    --destination=$(pwd)/output \
    --watermark=$(pwd)/watermak/${RELEASE_DATE}.pdf

# archive data
tar -cvf ${RELEASE_DATE}.tar.gz output