import sys
import csv
import xml.etree.ElementTree as ET

#Run as python3 flextext_wordform_extractor.py input_file
tree = ET.parse(sys.argv[1])

root = tree.getroot()
#with open(sys.argv[2], "w", newline = "") as csvfile:
#	fieldnames = ['Wordform', 'Morpheme']
#    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
for form in root.findall('.//phrases/phrase'):
    for gloss in form.findall(".//*[@type='gls']"):
        if 'en' in gloss.get("lang"):
            print("eng_gloss",gloss.text)
        elif 'es' in gloss.get("lang"):
            print("es_gloss",gloss.text)
    for wordform in form.findall('.//word/item'):
        if 'amu-fonipa' in wordform.get("lang"):
             #target language wordform
            print("tl:", wordform.text)
        for hmm in wordform.findall('.//morphemes/morph/item'):
            if 'txt' in hmm.get("type"):
                print("tl_morph!:", hmm.text)
    for morpheme in form.findall('.//morphemes/morph/item'):
        if 'amu-fonipa' in morpheme.get("lang"):
            if 'txt' in morpheme.get("type"):
                #target language morpheme
                print("tl_morph:", morpheme.text)
        elif 'es' in morpheme.get("lang"):
            # morpheme in spanish
            print("es_morph", morpheme.text)
    # for gloss in form:
        # if 'en' in wordform.get("lang"):
        #     print(gloss.text)
        # elif 'es' in wordform.get("lang"):
        #     print(gloss.text)
# for morpheme in root.findall('.//morphemes/morph/item'):
#     if 'amu-fonipa' in morpheme.get("lang") and 'txt' in morpheme.get("type"):
#         print(morpheme.text)
# for wordform in root.findall('.//word/item'):
#     if 'amu-fonipa' in wordform.get("lang"):
#         print("tl:", wordform.text)
#for phrase in root.iter("phrase"):
    # for word_index in phrase.iter("word"):
    #     for child in word_index:
    #         if child.tag == 'morphemes':
    #             print(child.find("item"))
    #             for morpheme in child:
    #                 print(morpheme)
# for words in root.iter("words"):
#     for word in words:
#         print(word.attrib)
#         items = word.findall('item')
#         for item in items:
#             if 'amu-fonipa' in item.get('lang'):
#                 print(item.text)
#             elif 'pos' in item.get('type'):
#                 print(item.text)