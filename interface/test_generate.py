from flask import Flask, render_template, request, g, session, redirect, url_for
import subprocess
import re

app = Flask(__name__)

@app.route("/", methods=['POST','GET'])
def choose_parts():
	if request.method == 'POST':
		root = request.form['root']
		mode_form = request.form['mode']
		subject_form = request.form['subject']
		trans_form = request.form['trans']
		modes_dict = {"Perfective": "<pfv>", "Imperfective": "<impv>"}
		subject_dict = {"I":"<1sgs>", "We":"<1pls>", "You":"<2sgs>",
					"You all":"<2pls>", "s/he":"<3sgs>", "they":"<3pls>"}
		trans_dict = {"Transitive":"<tr>", "Intransitive":"<intr>"}
		trans = trans_dict[trans_form]
		subject = subject_dict[subject_form]
		mode = modes_dict[mode_form]
		return assemble(root, mode, subject, trans)
	else:
		modes = ["Perfective", "Imperfective"]
		roots = ["pʼíʔi", "ʔámlq", "ʔíkʷtaq", "llq"]
		subjects = ["I", "We", "You", "You all", "s/he", "they"]
		transitivity = ["Transitive", "Intransitive"]
		return render_template('builder.html', modes=modes, roots=roots, subjects=subjects, transitivity=transitivity)
		# subject = request.form['subject']
		# object = request.form['object']
		# transitivity = request.form['transitivity']
		# aspect = request.form['aspect']
		# tense = request.form['tense']

def assemble(root, mode, subject, trans):
	command = subprocess.run(["echo \"^" + root + "<v>" + mode + trans + subject + "$\" | lt-proc -g ../constrained_generator.bin"], shell=True,
							 capture_output=True, text=True)
	result = command.stdout.strip("\n$").split("/")
	return render_template('surface.html', root=root, mode=mode, subject=subject, result=result)
