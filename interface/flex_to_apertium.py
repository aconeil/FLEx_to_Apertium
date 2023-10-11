import os
import sys
import xml.etree.ElementTree as ET
def gen_files(iso):
    word_by_pos = {}
    morph_patterns = []
    alphabet = []
    morph_by_type = {}
    alterations = {}
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
    # for i in range(1, len(sys.argv)):
    #     combined_input = open('combined.xml', "w+")
    #     for line in open(sys.argv[i]).readlines():
    #         combined_input.write(line)
    # combined_input.close()
    tree = ET.parse(open(iso+"_"+'combined.xml',"r"))
    root = tree.getroot()
    #Determine the language of the file for naming conventions
    lang = [x.get("lang") for x in root.findall('.//languages/language/[@vernacular="true"]')][0]
    print("lang in script is", lang)
    try:
        lexd = open('%s/%s.lexd' % (lang, lang), 'w')
    except:
        os.mkdir(lang)
        lexd = open('%s/%s.lexd' % (lang, lang), 'w')
    morphlexd = open('%s/morph_%s.lexd' % (lang, lang), 'w')
    corpus = open('%s/%s_corpus.txt' % (lang, lang), "w")
    rules = open('%s/%s.twol' % (lang, lang), "w")
    #Extract POS information for each word
    for word in root.findall('.//phrases/phrase/words/word'):
        for item in word.findall('./item'):
            #for wordform in target language, get text
            if item.get("type") == 'txt' and item.get("lang") == lang:
                surface = item.text
                #print(surface)
            #extract any available pos information about the wordform
            else:
                continue
            if word.findall('./item[@type="pos"]') != []:
                if item.get("type") == 'pos':
                    pos = item.text
                    word_by_pos[surface] = pos
            #or else assign miscellaneous POS
            else:
                word_by_pos[surface] = "misc"
        for morphemes in word.findall('./morphemes'):
            entry = ""
            for morph in morphemes:
                morph_type = morph.get("type")
                #assign type to unlabelled morphemes based on flex formatting
                if morph_type == None:
                    if morph.findtext('./item[@type="txt"]')[0] == "-" and morph.findtext('./item[@type="txt"]')[-1] == "-":
                        morph_type = "infix"
                    elif morph.findtext('./item[@type="txt"]')[0] == "-":
                        morph_type = "suffix"
                    elif morph.findtext('./item[@type="txt"]')[-1] == "-":
                        morph_type = "prefix"
                    elif morph.findtext('./item[@type="txt"]')[0] == "*":
                        morph_type = "bound_stem"
                    elif morph.findtext('./item[@type="txt"]')[0] == "=" and morph.findtext('./item[@type="txt"]')[-1] == "=":
                        morph_type = "simulfix"
                    elif morph.findtext('./item[@type="txt"]')[0] == "=":
                        morph_type = "enclitic"
                    elif morph.findtext('./item[@type="txt"]')[-1] == "=":
                        morph_type = "proclitic"
                    elif morph.findtext('./item[@type="txt"]')[0] == "~" and morph.findtext('./item[@type="txt"]')[-1] == "~":
                        morph_type = "suprafix"
                    else:
                        morph_type = "stem"
                entry= entry + morph_type + " "
            if morph_type in morph_by_type.keys():
                morph_by_type[morph_type].append(morph.findtext('./item[@type="txt"]').replace("-","").replace("=",""))
            else:
                morph_by_type[morph_type] = [morph.findtext('./item[@type="txt"]').replace("-","").replace("=",""),]
            #print(morph_type, morph.findtext('./item[@type="txt"]').replace("-","").replace("=",""))
            entry = entry.strip(" ")
            morph_patterns.append(entry)
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
    #find combinations of morpheme patterns
    morph_patterns = list(set(morph_patterns))
    for i in range(len(morph_patterns)):
        pattern = morph_patterns[i].split(" ")
        for j in range(len(pattern)):
            if j == 0:
                prev = pattern[j]
                condensed = prev
            else:
                if pattern[j] == prev:
                    if condensed[-1] == "+":
                        continue
                    else:
                        condensed = condensed + "+"
                        prev = pattern[j]
                        continue
                else:
                    condensed = condensed + " " + pattern[j]
                    prev = pattern[j]
        morph_patterns[i] = condensed
    morph_patterns = list(set(morph_patterns))
    morphlexd.write("PATTERNS\n")
    [morphlexd.write(morph_patterns[x] + "\n") for x in range(len(morph_patterns))]
    for key in morph_by_type:
        morph_by_type[key] = list(set(morph_by_type[key]))
        morphlexd.write(str('\n' + key.upper()+'\n'))
        [morphlexd.write(morph_by_type[key][x] + "\n") for x in range(len(morph_by_type[key]))]
    #gathering alphabet from corpus file
    with open('%s/%s_corpus.txt' % (lang, lang), "r") as file:
        for line in file.readlines():
            for character in line:
                if character not in alphabet:
                    alphabet.append(character.lower())
                else:
                    continue
    alphabet = list(set(alphabet))
    alphabet_cleaned = []
    punc = '''!()||-[]{};:'"\,<>./?+@#$%^&*_~\n'''
    for character in alphabet:
        if character.isalpha() == True:
            alphabet_cleaned.append(character)
    alphabet_cleaned.sort()
    rules.write("Alphabet\n\n")
    [rules.write(alphabet_cleaned[x] + " ") for x in range(len(alphabet_cleaned))]
    rules.write(";")
    #inferring alterations from cf forms in the flex files
    for wrd in root.findall('.//phrases/phrase/words/word'):
        for surf in wrd.findall('./item'):
            surface_word = surf.text
        for forms in wrd.findall('.//morphemes/morph/item'):
            #print(forms)
            surface = ""
            underlying = ""
            if forms.get("type") == 'txt' and forms.text is not None:
                surface = forms.text.replace("\s", "")
            elif forms.get("type") == 'cf' and forms.text is not None:
                underlying = forms.text.replace("\s", "")
            if surface != underlying:
                # find single character substitutions
                if len(surface)==len(underlying):
                    #print(surface, underlying)
                    for i in range(len(surface)):
                        if surface[i] != underlying[i]:
                            print(surface[i], underlying[i])
                # find multi character substitutions
                if len(surface) < len(underlying):
                    print(surface, underlying)
        return lang
#
# # function to return strings padded with 0 for alignment of single character insertions or deletions
# def align(x, y):
#     if len(x)==len(y):
#         return x, y
#     else:
#         # insert null character randomly in x to find best alignment
#         if len(x) == (len(y)-1):
#             align_score = {}
#             for i in range(len(y)):
#                 score = 0
#                 x = x[:i] + "0" + x[i:]
#                 if x[i] == y[i]:
#                     score += 1
#                 align_score[x, y] = score
#             best_score = max(zip(align_score.values(), align_scores.keys()))[1]
#             return best_score
#         # insert null character randomly in y to find best alignment
#         elif (len(x)-1) == len(y):
#             alignment_score = 0
#             align_score = {}
#             for i in range(len(x)):
#                 score = 0
#                 y = y[:i] + "0" + y[i:]
#                 if x[i] == y[i]:
#                     score += 1
#                 align_score[x, y] = score
#             best_score = max(zip(align_score.values(), align_scores.keys()))[1]
#             return best_score
#         #can't handle more than +/- one in a string reliably
#         else:
#             return
