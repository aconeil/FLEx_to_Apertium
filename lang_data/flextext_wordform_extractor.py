import sys
import csv
import xml.etree.ElementTree as ET
#This program extracts the surface wordforms in any number of flextext files
#Run as python3 flextext_wordform_extractor.py input_files[any number] out_file.csv

with open(sys.argv[-1], "w", newline="") as csvfile:
    fieldnames = ['Wordform', 'POS']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    for i in range(1, len(sys.argv)-1):
        tree = ET.parse(sys.argv[i])
        print("working with file", i)
        root = tree.getroot()
        wordforms = []
        word_by_pos = {}
        lang = [x.get("lang") for x in root.findall('.//languages/language/[@font="Charis SIL"]')][0]
    # for morpheme in root.findall('.//morphemes/morph/item'):
        #This narrows forms to all those found in each phrase
        for word in root.findall('.//phrases/phrase/words/word/item'):
            # extract the target-language wordform, assign to key
            if 'txt' in word.get("type"):
                if word.text not in wordforms:
                    wordforms.append(word.text)
            else:
                continue
        for form in wordforms:
            writer.writerow({'Wordform': form})