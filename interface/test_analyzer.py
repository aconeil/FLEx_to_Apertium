from flask import Flask, render_template, request, g, session, redirect, url_for
import subprocess
import re

# @app.route("/", methods=['POST', 'GET'])
def analyze_form(surface_form):
	print(surface_form)
	subprocess.run(["cd apertium-XYZ/ && make"], shell=True, capture_output=False, text=True)
	subprocess.run(["cd apertium-XYZ/ && lexd apertium-XYZ.XYZ.lexd > generator.att"], shell=True, capture_output=False, text=True)
	subprocess.run(["cd apertium-XYZ/ && lt-comp rl generator.att analyser.bin"], shell=True, capture_output=False, text=True)
	command = subprocess.run(["echo \"" + surface_form + "\" | lt-proc analyser.bin"], shell=True, capture_output=True, text=True)
	result = command.stdout.strip("\n$").split("/")
	dict = {}
	print(command)
	try:
		root = re.findall(r"[^\<^\>]*(?=\<)", str(result[1]))[0]
		print(root)
	#root = re.findall(r"(?=\<)", str(result[1:]))
	except:
		return "This entry doesn't have an analysis yet!"
	#root = re.findall(r"(?<=\>)[^\>\<]+(?=\<)", str(result[1:]))[0]
	for analysis in range(len(result)):
		if analysis == 0:
			continue
		else:
			form_tags = re.findall(r"(?<=\<)[^\>\<]+(?=\>)", str(result[analysis]))
			dict[analysis] = form_tags
	return render_template('analyzer_output.html', root=root, dict=dict, surface_form=surface_form)