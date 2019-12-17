#!/bin/sh


for file in $1/*; do
  cat $file | sed -e 's/<[^>]*>//g' | tee "$2${file##*/}"
done
