import sys
import csv
import xml.etree.ElementTree as ET
word_by_pos = {}
corpus = []
#Run as python3 flextext_wordform_extractor.py input_files[any number] out_file.
with open(sys.argv[-1], "w", newline="") as csvfile:
    fieldnames = ['Wordform', 'POS']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    for i in range(1, len(sys.argv)-1):
        tree = ET.parse(sys.argv[i])
        print("working with file", i)
        root = tree.getroot()
        #save information about which language for future use
        lang = [x.get("lang") for x in root.findall('.//languages/language/[@font="Charis SIL"]')][0]
        for word in root.findall('.//phrases/phrase/words/word'):
            for item in word.findall('./item'):
                if item.get("type") == 'txt':
                    surface = item.text
                if word.findall('./item[@type="pos"]') != []:
                    if item.get("type") == 'pos':
                        pos = item.text
                        word_by_pos[surface] = pos
                else:
                    word_by_pos[surface] = "misc"
    #print(len(word_by_pos))
    writer.writeheader()
    for word in word_by_pos.items():
        #print(word)
        writer.writerow({'Wordform':word[0], 'POS':word[1]})
    for phrases in root.findall('.//phrases/phrase'):
        phrase = ''
        #for word in phrase.findall()
        for words in phrases.findall('./words/word/item[@lang={{lang}}]'):
            phrase = phrase + words.text + " "
        corpus.append(phrase.strip(" "))
    #export to a corpus file
    print(corpus)
