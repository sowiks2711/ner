#!/bin/bash 
filename='filepaths.data'
while read line; do
echo ${line#*/*/*/}
done<$filename
