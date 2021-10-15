#! /bin/bash

declare -i linenum=0

#if no parameters are given, output 0 and exit
if [[ $# -eq 0 ]]
then
	echo $linenum
	exit 1
fi

#calculate total number of line of all files
function line_count() {
	for file in $1/* $1/.[^.]*
		do
			if [[ -f "$file" ]]
			then
				linenum+=$(wc -l < $file)
			elif [[ -d "$file" ]]
			then
				line_count $file
			fi
		done
}

for file in $*
do
	line_count $file
done

echo "Total numebr of lines of all file is: $linenum"
