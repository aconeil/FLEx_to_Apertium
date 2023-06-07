import sys
import csv
import xml.etree.ElementTree as ET

tree = ET.parse(sys.argv[1])

root = tree.getroot()
forms = []
poss = []
with open(sys.argv[2], "w", newline = "") as csvfile:
	fieldnames = ['Wordform', 'Part_of_Speech']
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	for wordform in root:
		pos = []
		for x in wordform:
			#extract wordform in TL
			if x.tag in 'form':
				forms.append(x.text)
			#extract POS for wordform
			for entry in x:
				if entry.tag == 'category':
					pos.append(entry.text)
		poss.append(pos)
	for i in range(0, len(forms)-1):
		print(poss[i])
		writer.writerow({'Wordform':forms[i], 'Part_of_Speech':poss[i]})
				#while x.tag == 'category':
					#category == x.text
					#print(form, category)
		#forms = [form.text for form in root.iter('form')]
		#poss = [pos.text for pos in root.iter('category')]
	#print(len(poss), len(forms))
	#for i in range(0, len(forms)-1):
	# 	print(poss[i])
		#writer.writerow({'Wordform':forms[i], 'Part_of_Speech':poss[i]})
# 	for form in root.iter('form'):
# 		form = form.text
# 		forms.append(form)
# #		writer.writerow({'Wordform':form.text})
# 	for pos in root.iter('category'):
# 		pos = pos.text
# 		writer.writerow({'Wordform':form, 'Part_of_Speech':pos})