import os
from flask import *
from flask_navigation import Navigation
import flex_to_apertium
import glob
from xml.etree import ElementTree as ET

secret_key = os.urandom(12)
UPLOAD_FOLDER = 'temp_uploads'
ALLOWED_EXTENSIONS = {'xml', 'flextext', 'XML','FLEXTEXT'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = secret_key
nav= Navigation(app)

nav.Bar('top', [
    nav.Item('Convert Files', 'convert'),
    nav.Item('About', 'about'),
    nav.Item('Apertium for Language Technology', 'learn'),
])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/FLextoApertium', methods=['GET', 'POST'])
def convert():
    if request.method == 'GET':
        return render_template("convert.html")
    if request.method == 'POST':
        #get data from response
        form = request.form
        iso = form['iso']
        print("iso is", iso)
        #privacy = form['privacy']
        files = request.files.getlist("file")
        for file in files:
            if file.filename == "":
                flash("Error: No selected file!")
                return redirect("/FLextoApertium")
            else:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], iso+"_"+str(files.index(file))+file.filename))
        combined_input = open(iso+"_"+'combined.xml', "w+")
        first = None
        for filename in os.listdir('temp_uploads'):
            if iso in filename:
                data = ET.parse(os.path.join(os.getcwd(), 'temp_uploads', filename)).getroot()
                if first is None:
                    first = data
                else:
                    first.extend(data)
        if first is not None:
            combined_input.write(ET.tostring(first, encoding="unicode"))
            #print(ET.tostring(first))
                #for line in open(os.path.join(os.getcwd(), 'temp_uploads', filename)).readlines():
                        #combined_input.write(line)
        #combined_input.close()
        lang = flex_to_apertium.gen_files(iso)
        return render_template("access.html", lang=lang)

@app.route('/FLextoApertium/access', methods=['GET', 'POST'])
def access():
    print("You are in access")
    form = request.form
    lang = form['lang']
    print("Access lang is", lang)
    lexd_file = '%s/%s.lexd' % (lang, lang)
    print(lexd_file)
    return send_file(lexd_file, as_attachment=True)
@app.route('/FLextoApertium/learn', methods=['GET', 'POST'])
def learn():
    return render_template("learn.html")

@app.route('/FLextoApertium/about', methods=['GET', 'POST'])
def about():
    return render_template("about.html")