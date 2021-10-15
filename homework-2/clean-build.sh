#! /bin/bash

#make a hidden directory in the current directory named .build and avoid print a warning using "-p"
mkdir -p .build

#complie the project.tex 
pdflatex -output-directory=.build $1.tex

#check for file not of type ".tex" and ".pdf" and move them into .build
for file in $1.*
do
	if [[ $file != "$1.tex" && $file != "$1.pdf" ]]
	then
		mv $file .build
	fi
done
