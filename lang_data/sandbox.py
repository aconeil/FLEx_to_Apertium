import sys
import csv
import xml.etree.ElementTree as ET

#Run as python3 flextext_wordform_extractor.py input_file out_file.csv
tree = ET.parse(sys.argv[1])
wordforms = {}
root = tree.getroot()
with open(sys.argv[2], "w", newline = "") as csvfile:
    fieldnames = ['Wordform', 'Morpheme', 'Eng_gloss', 'Span_gloss']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
# for morpheme in root.findall('.//morphemes/morph/item'):
    #This narrows forms to all those found in a phrase
    for form in root.findall('.//phrases/phrase'):
        values = {}
        #find the gloss in a phrase
        for gloss in form.findall(".//*[@type='gls']"):
            if 'en' in gloss.get("lang"):
                values["Eng_gloss"] = gloss.text
                #print("eng_gloss",gloss.text)
            else:
                values["Eng_gloss"] = ""
            if 'es' in gloss.get("lang"):
                values["Span_gloss"] = gloss.text
                #print("es_gloss",gloss.text)
            else:
                values["Span_gloss"] = ""
        #for each word in the phrase
        for entry in form.findall('./words/word'):
            for word in entry.findall('./item'):
                print(word.attrib)
                #extract the target-language wordform, assign to key
                if 'txt' in word.get("type"):
                    wordform = word.text
                    print(word.text)
                for morpheme in entry.findall('./morphemes/morph/item'):
                    if 'amu-fonipa' in morpheme.get("lang") and 'txt' in morpheme.get("type"):
                        # target language morpheme
                        values["Morpheme"] = morpheme.text
                        #print("tl_morph:", morpheme.text)
                    else:
                        values["Morpheme"] = ""
            wordforms[wordform] = values
    for i in wordforms.keys():
        wordforms[i]["Wordform"] = i
        writer.writerow(wordforms[i])
