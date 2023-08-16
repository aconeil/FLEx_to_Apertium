import flask
from flask_navigation import Navigation

UPLOAD_FOLDER = 'temp_uploads'
ALLOWED_EXTENSIONS = {'xml', 'flextext'}

app = flask.Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
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
    if flask.request.method == 'GET':
        return flask.render_template("convert.html")
    elif flask.request.method == 'POST':
        #get data from response
        form = flask.request.form
        iso = form['iso']
        privacy = form['privacy']
        file = flask.request.files['files']
        if file.filename == '':
            flash('No selected file')
            return flask.redirect("convert.html")
        if file and allowed_file(file.filename):
            filename = flexfiles_%s(file.fil) %iso
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #check apertium github for existing module based on iso code
        #if privacy == "public":
            #commit apertium module to apertium
        #else:
            #download the generated module as a zip file
        return flask.render_template("access.html")

@app.route('/FLextoApertium/access', methods=['GET', 'POST'])

@app.route('/FLextoApertium/learn', methods=['GET', 'POST'])
def learn():
    return flask.render_template("learn.html")

@app.route('/FLextoApertium/about', methods=['GET', 'POST'])
def about():
    return flask.render_template("about.html")