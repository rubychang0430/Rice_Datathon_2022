#! /bin/bash

awk 'NF > 0' poetry.txt > duplicated.txt
file="duplicated.txt"

if [[ $1=="-h" ]]
then
	echo "Poetry.sh program generates a table that contains Student ID, Favorite poem and first 7 characters of their favorite poem"
fi

echo -n -e "Student_ID\tFavotite poem\t\t\t\tFirst_7_chars_of_poem\n"

while read line
do
	if [[ "${line:0:7}" = "Student" || "${line:0:7}" = "student" ]]
	then
		echo -n -e "$line\t"
	fi
	
	if [ "${line:0:4}" = "Poem" ]
	then
		echo -n -e "${line:6}\t\t"
		echo -n -e "${line:6:7}\n"
	fi
	
	if [ "$line" = "" ]
	then
		echo -n -e "NA\t\t\t\t\t"
		echo -n -e "NA\n"
	fi
done < $file
