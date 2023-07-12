import sys
import xml.etree.ElementTree as ET
word_by_pos = {}
#Run as python3 flextext_wordform_extractor.py input_files[any number]
for i in range(1, len(sys.argv)):
    tree = ET.parse(sys.argv[i])
    print("working with file", i)
    root = tree.getroot()
    #save information about which language for specifying language
    lang = [x.get("lang") for x in root.findall('.//languages/language/[@font="Charis SIL"]')][0]
    lexd = open('%s.lexd' % lang, 'w')
    morphlexd = open('morph_%s.lexd' % lang, 'w')
    corpus = open('%s_corpus.txt' % lang, "w")
    #Loop through the words in each phrase
    for word in root.findall('.//phrases/phrase/words/word'):
        for item in word.findall('./item'):
            #for wordform in target language, get text
            if item.get("type") == 'txt' and item.get("lang") == lang:
                surface = item.text
            #extract any available pos information about the wordform
            if word.findall('./item[@type="pos"]') != []:
                if item.get("type") == 'pos':
                    pos = item.text
                    word_by_pos[surface] = pos
            #or else assign miscellaneous POS
            else:
                word_by_pos[surface] = "misc"
pos_tags = list(set(word_by_pos.values()))
#temporarily default patterns to part of speech until further steps in the project
lexd.write("PATTERNS\n")
[lexd.write(pos_tags[x].replace(".", "").replace(" ", "") + "\n") for x in range(len(pos_tags))]
for pos_tag in pos_tags:
    lexd.write("\nLEXICON " + pos_tag.replace(".", "").replace(" ", "") + "\n")
    for entry in word_by_pos.items():
        if pos_tag in entry:
            lexd.write("<" + pos_tag.replace(".", "").replace(" ", "") + ">:" + entry[0] + "\n")
    lexd.write("\n")
#this loop extracts all phrases to a corpus file
for phrases in root.findall('.//phrases/phrase'):
    iso_path = './words/word/item/[@lang="' + lang + '"]'
    phrase = ''
    #for word in phrase.findall()
    for words in phrases.findall(iso_path):
        phrase = phrase + words.text + " "
    corpus.write(phrase.strip(" ") +"\n")
corpus.close()
