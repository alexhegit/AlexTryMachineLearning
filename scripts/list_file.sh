#!/bin/bahs
# get all filename in specified path

path=$1
files=$(ls $path)
i=1
for filename in $files
do
   echo "$filename $i" >> filename.txt
   let i++
done
