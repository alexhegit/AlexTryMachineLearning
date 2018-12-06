#!/bin/bahs
# get all filename in specified path

path=$1
files=$(ls $path)
oldsuffix="jpg"
newsuffix="jpeg"
for file in $(ls $path | grep .${oldsuffix})
do
   echo "$file from jpg to jpeg"
   name=$(ls $file | cut -d. -f1)
   mv $file ${name}.${newsuffix}
done
