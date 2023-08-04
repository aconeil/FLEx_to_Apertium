# /usr/bin/bash
# paste this file into the subdirectory of files and run
ls > filenames.txt
input="filenames.txt"
while IFS= read -r line
do
	mv "$line"/data/versionXML.flextext ../"$line".flextext
done < "$input"