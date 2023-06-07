import xml.etree.ElementTree as ET
import csv

tree = ET.parse("test_majang.xml")

root = tree.getroot()
with open("maj_wordforms.csv", "w", newline = "") as csvfile:
	fieldnames = ['Wordform', 'Part_of_Speech']
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	for form in root.iter('form'):
		form = form.text
		writer.writerow({'Wordform':form.text})
	for pos in root.iter('category'):
		pos = pos.text
	writer.writerow({'Wordform':form, 'Part_of_Speech':pos})

