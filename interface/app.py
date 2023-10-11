import os
from flask import *
from flask_navigation import Navigation
import flex_to_apertium
import shutil
import test_analysis
import test_generate
from xml.etree import ElementTree as ET


secret_key = os.urandom(12)
UPLOAD_FOLDER = 'temp_uploads'
APERTIUM_DIR = 'apertium-XYZ'
ALLOWED_EXTENSIONS = {'xml', 'flextext', 'XML','FLEXTEXT'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['APERTIUM_DIR'] = APERTIUM_DIR
app.config['SECRET_KEY'] = secret_key
nav= Navigation(app)

nav.Bar('top', [
    nav.Item('Convert Files', 'convert'),
    nav.Item('About', 'about'),
    nav.Item('Apertium for Language Technology', 'learn'),
    nav.Item('Test Analyzer', 'analyze'),
#    nav.Item('Test Generator', 'generate'),
])

def allowed_file(filename):
    filename=str(filename)
    if filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
        return True
    else:
        return False

def get_files(iso):
    files = request.files.getlist("file")
    for file in files:
        if file.filename == "":
            flash("Error: No selected file!")
            return redirect("/")
        elif allowed_file(file.filename) == False:
            flash("Error: File must be xml or flextext")
            return redirect("/")
        else:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],
                                   iso + "_" + str(files.index(file)) + file.filename))

@app.route('/', methods=['GET', 'POST'])
def convert():
    if request.method == 'GET':
        return render_template("convert.html")
    if request.method == 'POST':
        form = request.form
        iso = form['iso']
        #privacy = form['privacy']
        get_files(iso)
        combined_input = open(iso+"_"+'combined.xml', "w+")
        first = None
        for filename in os.listdir('temp_uploads'):
            data = ET.parse(os.path.join(os.getcwd(), 'temp_uploads', filename)).getroot()
            if first is None:
                first = data
            else:
                first.extend(data)
        if first is not None:
            combined_input.write(ET.tostring(first, encoding="unicode"))
        lang = flex_to_apertium.gen_files(iso)
        os.remove(iso+'_combined.xml')
        folder = '%s/' %(lang)
        shutil.make_archive(iso+"ApertiumRepo", 'zip', folder)
        shutil.rmtree(folder)
        for filename in os.listdir('temp_uploads'):
            os.remove(os.path.join(os.getcwd(), 'temp_uploads', filename))
        return render_template("access.html", iso=iso)

@app.route('/access/<iso>', methods=['GET', 'POST'])
def access(iso):
    if request.method == 'GET':
        return send_file(iso+"ApertiumRepo.zip", as_attachment=True)
    #os.remove(iso+"ApertiumRepo.zip")
@app.route('/learn', methods=['GET', 'POST'])
def learn():
    return render_template("learn.html")
@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template("about.html")

@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    if request.method == 'POST':
        files = request.files.getlist("file")
        print("files: ", files)
        for file in files:
            print(file)
            if file.filename == "":
                flash("Error: No selected file!")
                return redirect("/analyze")
            elif ".lexd" not in file.filename:
                flash("Error: File must be lexd")
                return redirect("/analyze")
            else:
                file.save(os.path.join(app.config['APERTIUM_DIR'], apertium - XYZ.XYZ.lexd))
    return render_template("analyze.html")

@app.route('/generate', methods=['GET', 'POST'])
def generate():
    if request.method == 'POST':
        files = request.files.getlist("file")
        for file in files:
            if file.filename == "":
                flash("Error: No selected file!")
                return redirect("/generate")
            elif ".lexd" not in file.filename:
                flash("Error: File must be lexd")
                return redirect("/generate")
            else:
                file.save(os.path.join(app.config['APERTIUM_DIR'], apertium-XYZ.XYZ.lexd))
    # write code to upload the lexd and twol file
    return render_template("generate.html")
@app.route('/view_analyzer', methods=['GET', 'POST'])
def view_analyzer():
    return render_template("view_analyzer.html")
@app.route('/view_generator', methods=['GET', 'POST'])
def view_generator():
    return render_template("view_generator.html")