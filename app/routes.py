import os
from flask import Flask, render_template, request
from algorithms.load import load
from algorithms.balance import balance
from util.parse_manifest import parse

app = Flask(__name__)


currentUser = None

TEMP_DIR = 'temp'
currentManifest = None

loadStatus = False
balanceStatus = False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods = ['POST'])
def login():
    name = request.form.get('name')

    currentUser = name

    # Log in log file later

    return {'Current user': currentUser}

@app.route('/comment', methods = ['POST'])
def comment():
    pass

@app.route('/load', methods = ['GET', 'POST'])
def loadRequest():
    if request.method == 'GET':
        loadStatus = True
        return render_template('steps.html', manifestData=currentManifest, load=loadStatus)

    load_items = request.form.get('load').split(',')
    unload_items = request.form.get('unload').split(',')

    load_items = [item for item in load_items if item]
    unload_items = [(int(r), int(c)) for (r, c) in (cell.split('-')[1:] for cell in unload_items)]

    # TODO
    # steps = load(load_items, unload_items, currentManifest)

    # return blank for now
    return render_template('steps.html', manifestData=currentManifest, load=True)

@app.route('/balance', methods = ['GET', 'POST'])
def balanceRequest():
    if request.method == 'GET':
        return render_template('steps.html')
    
    manifest = request.form.get('manifest')

    steps = balance(manifest)

    return steps

@app.route('/manifest', methods = ['POST'])
def manifest():
    global currentManifest
    if 'file' in request.files:
        file = request.files['file']

        file_path = os.path.join(os.path.dirname(__file__), TEMP_DIR, file.filename)
        file.save(file_path)

        parsed = parse(file_path)

        currentManifest = parsed

        os.remove(file_path)

        return {'Success': 'Uploaded manifest', 'Manifest': currentManifest}
    else:
        return {'Error': 'Failed to upload manifest'}

@app.route('/complete', methods = ['POST'])
def complete():
    pass

if __name__ == "__main__": 
    app.run()
