import os
import sys
import xml.etree.ElementTree as ET
word_by_pos = {}
flex_pos_cat = {"adj":"Adjective", "cop":"CopulativeVerb", "vd":"DitransitiveVerb", "adp":"adposition", "adv":"Adverb",
                "clf":"Classifier", "conn":"Connective", "det":"Determiner", "existmrkr":"ExistentialMarker",
                "expl":"Expletive", "interj":"Interjection", "n":"Noun", "ptcp":"Participle", "prt":"Particle",
                "prenoun":"Prenoun", "preverb":"Preverb", "pro-form":"Pro-form", "pro":"Pronoun", "q":"QuestionParticle",
                "v":"Verb", "verbprt":"VerbalParticle", "vi":"IntransitiveVerb", "vt":"TransitiveVerb",
                "pro-adv":"Pro-adverb", "pro-adj":"Pro-adjective", "interrog":"InterrogativePro-form",
                "nomprt": "NominalParticle", "nom":"Nominal", "ger":"Gerund", "nprop":"ProperNoun", "subs":"Substantive",
                "art":"Article", "def":"DefiniteArticle", "indf":"IndefiniteArticle", "post":"Postposition",
                "prep":"Preposition", "nclf":"NounClassifier", "coordconn":"CoordinatingConnective",
                "subordconn":"SubordinatingConnective", "correlconn":"CorrelativeConnective", "advlizer":"Adverbializer",
                "comp":"Complementizer","rel":"Relativizer", "dem":"Demonstrative", "quant":"Quantifier", "num":"Numeral",
                "cardnum":"CardinalNumeral", "distrnum":"DistributiveNumeral","multipnum":"MultiplicativeNumeral",
                "ordnum":"OrdinalNumeral", "partnum":"PartitiveNumeral","indfpro":"IndefinitePronoun","pers":"PersonalPronoun",
                "emph":"EmphaticPronoun","poss":"PossessivePronoun","recp":"ReciprocalPronoun","refl":"ReflexivePronoun",
                "relpro":"RelativePronoun"}
#Run as python3 flextext_wordform_extractor.py input_files[any number]
for i in range(1, len(sys.argv)):
    tree = ET.parse(sys.argv[i])
    print("working with file", i)
    root = tree.getroot()
    #Determine the language of the file for naming conventions
    lang = [x.get("lang") for x in root.findall('.//languages/language/[@font="Charis SIL"]')][0]
    try:
        lexd = open('%s/%s.lexd' % (lang, lang), 'w')
    except:
        os.mkdir(lang)
        lexd = open('%s/%s.lexd' % (lang, lang), 'w')
    morphlexd = open('%s/morph_%s.lexd' % (lang, lang), 'w')
    corpus = open('%s/%s_corpus.txt' % (lang, lang), "w")
    #Extract POS information for each word
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
    # Extract phrases in each file to create a corpus
    for phrases in root.findall('.//phrases/phrase'):
        iso_path = './words/word/item/[@lang="' + lang + '"]'
        phrase = ''
        for words in phrases.findall(iso_path):
            phrase = phrase + words.text + " "
        corpus.write(phrase.strip(" ") + "\n")
    corpus.close()
pos_tags = list(set(word_by_pos.values()))
#Convert to standard flex POS tags when possible
for pos in pos_tags:
    i = pos_tags.index(pos)
    pos = pos.replace(".", "").replace(" ", "")
    if flex_pos_cat.get(pos) != None:
        pos_tags[i] = flex_pos_cat.get(pos)
#temporarily default patterns to part of speech until further steps in the project
lexd.write("PATTERNS\n")
[lexd.write(pos_tags[x].replace(".", "").replace(" ", "") + "\n") for x in range(len(pos_tags))]
for pos_tag in pos_tags:
    lexd.write("\nLEXICON " + pos_tag.replace(".", "").replace(" ", "") + "\n")
    for entry in word_by_pos.items():
        if pos_tag in entry:
            lexd.write("<" + pos_tag.replace(".", "").replace(" ", "") + ">:" + entry[0] + "\n")
    lexd.write("\n")