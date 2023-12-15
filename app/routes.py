import os
from flask import Flask, render_template, request, redirect
from algorithms.load import load
from algorithms.balance import balance
from util.parse_manifest import parse

app = Flask(__name__)


currentUser = None

TEMP_DIR = 'temp'
currentManifest = None

steps = []

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

@app.route('/steps', methods = ['GET'])
def showSteps():
    return render_template('steps.html', manifestData=currentManifest, steps=steps)


@app.route('/load', methods = ['GET', 'POST'])
def loadRequest():
    global steps
    if request.method == 'GET':
        return render_template('load.html', manifestData=currentManifest)

    load_items = request.form.get('load').split(',')
    unload_items = request.form.get('unload').split(',')

    load_items = [item for item in load_items if item]
    unload_items = [item for item in unload_items if item]

    if unload_items:
        unload_items = [(int(r) - 1, int(c)) for (r, c) in (cell.split('-')[1:] for cell in unload_items)]
    else:
        unload_items = []
        
    steps, newManifest = load(load_items, unload_items, currentManifest)

    #TODO: write new manifest

    return {'steps': steps}


@app.route('/balance', methods = ['GET'])
def balanceRequest():
    global steps
    if not currentManifest:
        return redirect('/')


    steps = balance(currentManifest)


    return redirect('/steps')

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
