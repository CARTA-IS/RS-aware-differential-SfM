#!/bin/bash

# https://brownbears.tistory.com/220
# https://m.blog.naver.com/PostView.naver?isHttpsRedirect=true&blogId=qbxlvnf11&logNo=221419256533
# https://stackoverflow.com/questions/16153446/bash-last-index-of

# $1 is first argument -> dir
# echo "./deepmatching $PWD/resize_$1/MAX_0001.JPG $PWD/resize_$1/MAX_0002.JPG -nt 24 -out $PWD/resize_$1/MAX_0001.txt"

file_dir=$PWD/resize_$1
file_list=("$file_dir"/*)
list_length=${#file_list[@]}
echo "$list_length"

for ((i=0; i<$list_length-1; i++)); do
    # echo "${file_list[i]}"
    # echo "${file_list[i+1]}"

    full_name=${file_list[i]##*/}
    name=${full_name%.*}
    output_text=$name".txt"
    # echo "$full_name"
    # echo "$name"
    # echo "$output_text"


    ./deepmatching ${file_list[i]} ${file_list[i+1]} -nt 24 -out $PWD/resize_$1/$output_text
    # exit 0

done


# Calling file path from file directory was hard to bring second argument

# for file in "$file_dir"/*; do
#     # name_array=$(echo $file | tr "/" "\n")
#     # for name in $name_array; do
#     #     echo "$name"
#     # done
#     full_name=${file##*/}
#     name=${full_name%.*}
#     name_int=$((${name#*_}))
#     # next=$name_int+1
#     ext=${full_name##*.}

#     
#     echo "$name_int"
#     # echo "$next"
#     echo "$ext"

# done