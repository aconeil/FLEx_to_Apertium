# /usr/bin/bash

ls > filenames.txt
input="filenames.txt"
while IFS= read -r line
do
	mv "$line"/data/versionXML.flextext ../"$line".flextext
done < "$input"
